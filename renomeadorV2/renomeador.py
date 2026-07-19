import re
import os
import LeitorPDF
import banco

# Armazena o histórico de renomeações para permitir desfazer
historico_renomeacoes = []

                        

def renomear(console_log=None):
    """
    Renomeia os arquivos PDF de acordo com os padrões de OS
    
    Args:
        console_log: Função para escrever no console (opcional)
        
    Returns:
        Lista de tuplas (nome_antigo, nome_novo) dos arquivos renomeados
    """
    global historico_renomeacoes
    historico_renomeacoes = []  # Limpa histórico anterior
    

    
    def log(msg, nivel="INFO"):
        """Função auxiliar para logar mensagens"""
        if console_log:
            console_log(msg, nivel)
        else:
            print(f"[{nivel}] {msg}")
            
    def mover_arquivo(caminho_atual_os, tipo_OS, pasta,nome_OS):
        verificar_tipo = re.search("PREVENTIVA", tipo_OS)
        
        if verificar_tipo:
            pasta_destino = os.path.join(pasta, "PREVENTIVAS")       
    
        else:       
            pasta_destino = os.path.join(pasta, tipo_OS)   
                
        os.makedirs(pasta_destino,exist_ok=True)
        caminho_atualizado = os.path.join(pasta_destino, nome_OS)
        
        try:
            os.rename(caminho_atual_os, caminho_atualizado)
            log(f"arquivo {nome_OS} movido com sucesso para {pasta_destino}", "SUCCESS")
            return caminho_atualizado
            
        except Exception as e:
            return None
    
        
            
    def mudar_nome(caminho_arquivo_antigo, caminho_arquivo_novo, antigo_nome, novo_nome ):
    
        try:
            os.rename(caminho_arquivo_antigo, caminho_arquivo_novo)
            historico_renomeacoes.append((antigo_nome, novo_nome))
            banco.data.registrar_historico(novo_nome, antigo_nome, "Renomeação automática")
            return caminho_arquivo_novo
            
                            
        except FileNotFoundError:
            log(f"Erro: Arquivo '{antigo_nome}' não foi encontrado", "ERROR")
            return None

        except PermissionError:
            log(f"Erro: Sem permissão para renomear '{antigo_nome}'", "ERROR")
            return None

        except FileExistsError:
            log(f"Erro: Arquivo '{novo_nome}' já existe", "ERROR")
            return None

        except OSError as erro:
            log(f"Erro inesperado ao renomear '{antigo_nome}': {erro}", "ERROR")
            return None
        
    arquivos = LeitorPDF.extrair_texto()
    

    if arquivos == "operação foi cancelada pelo usuário (não foi selecionada nenhuma pasta)":
        return "operação foi cancelada pelo usuário (não foi selecionada nenhuma pasta)"
    
    if not arquivos:
        log("Nenhum arquivo PDF foi encontrado na pasta selecionada", "WARNING")
        return []
    
    codigo = re.compile(r'\b\d{8}(?=\s)')
    ativos_list = banco.data.verificar_ativos()
    tipos_OS_list = banco.data.verificar_tipo_OS()
    
    if not ativos_list:
        log("Nenhum ativo cadastrado no sistema", "WARNING")
        return []
    
    tipos_OS = re.compile("|".join(tipos_OS_list))
    ativosNT = "|".join(ativos_list)
    ativos = re.compile(rf"\b({ativosNT})\-?[A-Z0-9]*\d[A-Z0-9]*\b")
    
    arquivos_processados = 0
    
    for antigo_nome in arquivos:
              
        if antigo_nome.endswith(".pdf"):
            codigoPDF = re.search(codigo, arquivos[antigo_nome])
            tipo_OS = re.search(tipos_OS,arquivos[antigo_nome] )
            
            if codigoPDF and tipo_OS:

                
                ativoPDF = re.search(ativos, arquivos[antigo_nome])
                
                if ativoPDF:
                    #estrutura de OS: codigo + tipo + ativo
                    novo_nome = (f'OS {codigoPDF.group()} {tipo_OS.group()} - {ativoPDF.group()}.pdf')
                    
                    caminho_arquivo_antigo = os.path.join(LeitorPDF.caminho_pasta[0], antigo_nome)
                    caminho_arquivo_novo = os.path.join(LeitorPDF.caminho_pasta[0], novo_nome)
                    
                    if os.path.exists(caminho_arquivo_novo):
                        log(f"Arquivo '{novo_nome}' já existe, pulando...", "WARNING")
                        continue
                    
                    caminho_atual_OS = mudar_nome(caminho_arquivo_antigo, caminho_arquivo_novo, antigo_nome, novo_nome )
                    
                    log(f"✓ '{antigo_nome}' → '{novo_nome}'", "SUCCESS")
                    arquivos_processados += 1
                    
                    #mudar arquivo de diretorio
                    
                    if caminho_atual_OS is not None:
                        
                        destino_final = mover_arquivo(caminho_atual_OS, tipo_OS.group(), LeitorPDF.caminho_pasta[0], novo_nome)
                        if destino_final is not None:
                            log(f"arquivo {novo_nome} movido para {destino_final}")
                        else:
                            log(f"erro ao move arquivo {novo_nome}")
                        
                else: #renomear mesmo sem ativo com a estrutura: codigo + tipo
                    novo_nome = (f'OS {codigoPDF.group()} {tipo_OS.group()}.pdf')
                    
                    caminho_arquivo_antigo = os.path.join(LeitorPDF.caminho_pasta[0], antigo_nome)
                    caminho_arquivo_novo = os.path.join(LeitorPDF.caminho_pasta[0], novo_nome)
                    
                    if os.path.exists(caminho_arquivo_novo):
                        log(f"Arquivo '{novo_nome}' já existe, pulando...", "WARNING")
                        continue
                    
                    
                    log(f"✓ '{antigo_nome}' → '{novo_nome}'", "SUCCESS")
                    arquivos_processados += 1        
                    caminho_atual_OS = mudar_nome(caminho_arquivo_antigo, caminho_arquivo_novo, antigo_nome, novo_nome )
                    
                    
                    destino_final = mover_arquivo(caminho_atual_OS, tipo_OS.group(), LeitorPDF.caminho_pasta[0], novo_nome)
                    if destino_final is not None:
                        log(f"arquivo {novo_nome} movido para {destino_final}")
                    else:
                        log(f"erro ao move arquivo {novo_nome}")
                

                        
            elif codigoPDF:
                    
                ativoPDF = re.search(ativos, arquivos[antigo_nome])
                
                if ativoPDF:
                    #estrutura de codigo OS + ativo, ou seja provavelmente preventiva
                    novo_nome = (f'OS {codigoPDF.group()} {ativoPDF.group()}.pdf')
                        
                    caminho_arquivo_antigo = os.path.join(LeitorPDF.caminho_pasta[0], antigo_nome)
                    caminho_arquivo_novo = os.path.join(LeitorPDF.caminho_pasta[0], novo_nome)
                        
                    if os.path.exists(caminho_arquivo_novo):
                        log(f"Arquivo '{novo_nome}' já existe, pulando...", "WARNING")
                        continue
                    
                    
                    log(f"✓ '{antigo_nome}' → '{novo_nome}'", "SUCCESS")
                    arquivos_processados += 1
                    caminho_atual_OS = mudar_nome(caminho_arquivo_antigo, caminho_arquivo_novo, antigo_nome, novo_nome )
                    
                    
                    destino_final = mover_arquivo(caminho_atual_OS, "PREVENTIVA", LeitorPDF.caminho_pasta[0], novo_nome)
                    if destino_final is not None:
                        log(f"arquivo {novo_nome} movido para {destino_final}")
                    else:
                        log(f"erro ao move arquivo {novo_nome}")
                    
                else:  
                    #colocar lógica para renomear mesmo sem codigo de ativo                      
                    log(f"Aviso: Não encontrado ativo para OS {codigoPDF.group()}", "WARNING")  
                    
                    novo_nome = (f'OS {codigoPDF.group()}.pdf')
                    
                    caminho_arquivo_antigo = os.path.join(LeitorPDF.caminho_pasta[0], antigo_nome)
                    caminho_arquivo_novo = os.path.join(LeitorPDF.caminho_pasta[0], novo_nome)
                    
                    if os.path.exists(caminho_arquivo_novo):
                        log(f"Arquivo '{novo_nome}' já existe, pulando...", "WARNING")
                        continue
                    
                    mudar_nome(caminho_arquivo_antigo, caminho_arquivo_novo, antigo_nome, novo_nome )  
                    
                    log(f"✓ '{antigo_nome}' → '{novo_nome}'", "SUCCESS")
                    arquivos_processados += 1
                                         
                    continue
            else:
                log(f"Aviso: Não encontrado código de OS em '{antigo_nome}'", "WARNING")
                continue
        else:
            log(f"Pulando: '{antigo_nome}' não é um arquivo PDF", "WARNING")
            continue
        
    log(f"Processo finalizado: {arquivos_processados} arquivo(s) renomeado(s)", "SUCCESS")
    return historico_renomeacoes


def desfazer_acao(console_log=None):
    """
    Desfaz a última ação de renomeação, retornando os arquivos aos nomes antigos
    
    Args:
        console_log: Função para escrever no console (opcional)
        
    Returns:
        Lista de tuplas (nome_novo, nome_antigo) dos arquivos desfeitos
    """
    global historico_renomeacoes
    
    def log(msg, nivel="INFO"):
        """Função auxiliar para logar mensagens"""
        if console_log:
            console_log(msg, nivel)
        else:
            print(f"[{nivel}] {msg}")
    
    if not historico_renomeacoes:
        log("Nenhuma ação para desfazer", "WARNING")
        return []
    
    # Obtém a pasta do último arquivo renomeado
    if not LeitorPDF.caminho_pasta:
        log("Erro: Nenhuma pasta foi selecionada anteriormente", "ERROR")
        return []
    
    pasta = LeitorPDF.caminho_pasta[0]
    desfeitos = []
    
    # Reverte as renomeações em ordem inversa
    for nome_antigo, nome_novo in reversed(historico_renomeacoes):
        caminho_antigo = os.path.join(pasta, nome_antigo)
        caminho_novo = os.path.join(pasta, nome_novo)
        
        try:
            if os.path.exists(caminho_novo):
                os.rename(caminho_novo, caminho_antigo)
                desfeitos.append((nome_novo, nome_antigo))
                log(f"✓ Desfeito: '{nome_novo}' → '{nome_antigo}'", "SUCCESS")
            else:
                log(f"Aviso: Arquivo '{nome_novo}' não encontrado", "WARNING")
        
        except FileNotFoundError:
            log(f"Erro: Arquivo '{nome_novo}' não foi encontrado", "ERROR")
        
        except PermissionError:
            log(f"Erro: Sem permissão para renomear '{nome_novo}'", "ERROR")
        
        except OSError as erro:
            log(f"Erro ao desfazer renomeação: {erro}", "ERROR")
    
    # Limpa o histórico após desfazer
    historico_renomeacoes = []
    log(f"Desfazer concluído: {len(desfeitos)} arquivo(s) revertido(s)", "SUCCESS")
    
    return desfeitos
