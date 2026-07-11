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
    
    arquivos = LeitorPDF.extrair_texto()

    if arquivos == "operação foi cancelada pelo usuário":
        return "operação foi cancelada pelo usuário"
    
    if not arquivos:
        log("Nenhum arquivo PDF foi encontrado na pasta selecionada", "WARNING")
        return []
    
    codigo = re.compile(r'\b\d{8}(?=\s)')
    ativos_list = banco.data.verificar_ativos()
    
    if not ativos_list:
        log("Nenhum ativo cadastrado no sistema", "WARNING")
        return []
    
    ativosNT = "|".join(ativos_list)
    ativos = re.compile(rf"\b({ativosNT})\-?[A-Z0-9]*\d[A-Z0-9]*\b")
    
    arquivos_processados = 0
    
    for antigo_nome in arquivos:
        
        if antigo_nome.endswith(".pdf"):
            codigoPDF = re.search(codigo, arquivos[antigo_nome])
        
            if codigoPDF:
                ativoPDF = re.search(ativos, arquivos[antigo_nome])
            
                if ativoPDF:
                    novo_nome = (f'OS {codigoPDF.group()} {ativoPDF.group()}.pdf')
                    
                    caminho_arquivo_antigo = os.path.join(LeitorPDF.caminho_pasta[0], antigo_nome)
                    caminho_arquivo_novo = os.path.join(LeitorPDF.caminho_pasta[0], novo_nome)
                    
                    if os.path.exists(caminho_arquivo_novo):
                        log(f"Arquivo '{novo_nome}' já existe, pulando...", "WARNING")
                        continue
                    
                    try:
                        os.rename(caminho_arquivo_antigo, caminho_arquivo_novo)
                        
                        # Registra no histórico
                        historico_renomeacoes.append((antigo_nome, novo_nome))
                        banco.data.registrar_historico(novo_nome, antigo_nome, "Renomeação automática")
                        
                        log(f"✓ '{antigo_nome}' → '{novo_nome}'", "SUCCESS")
                        arquivos_processados += 1
                        
                    except FileNotFoundError:
                        log(f"Erro: Arquivo '{antigo_nome}' não foi encontrado", "ERROR")

                    except PermissionError:
                        log(f"Erro: Sem permissão para renomear '{antigo_nome}'", "ERROR")

                    except FileExistsError:
                        log(f"Erro: Arquivo '{novo_nome}' já existe", "ERROR")

                    except OSError as erro:
                        log(f"Erro inesperado ao renomear '{antigo_nome}': {erro}", "ERROR")
                        
                else:
                    log(f"Aviso: Não encontrado ativo para OS {codigoPDF.group()}", "WARNING")
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
