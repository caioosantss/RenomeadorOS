import re
import os
import LeitorPDF
import banco

def renomear():
   
    arquivos = LeitorPDF.extrair_texto()
    
    if arquivos:
        codigo = re.compile(r'\b\d{8}(?=\s)')
        ativosNT = "|".join(banco.data.verificar_ativos())
        ativos = re.compile(rf"\b({ativosNT})\-?[A-Z0-9]*\d[A-Z0-9]*\b")
        
        
        for antigo_nome in arquivos:
            
            if antigo_nome.endswith(".pdf"):
                codigoPDF = re.search(codigo, arquivos[antigo_nome])
            
                if codigoPDF:
                    ativoPDF = re.search(ativos, arquivos[antigo_nome])
                
                    if ativoPDF:
                        novo_nome = (f'OS {codigoPDF.group()} {ativoPDF.group()}.pdf')
                        
                        if os.path.exists(LeitorPDF.caminho_pasta[0], novo_nome):
                            print("arquivo ja existe")
                            continue
                        
                        try:
                            os.rename(os.path.join(LeitorPDF.caminho_pasta[0], antigo_nome), os.path.join(LeitorPDF.caminho_pasta[0], novo_nome))
                            
                        except FileNotFoundError:
                            print(f"O arquivo {antigo_nome} não foi encontrado.")

                        except PermissionError:
                            print(f"Sem permissão para renomear o arquivo{antigo_nome}")

                        except FileExistsError:
                            print(f"Já existe um arquivo com esse nome{novo_nome}")

                        except OSError as erro:
                            print(f"Erro inesperado: {erro}")
                            
                    else:
                        print(f"não encontrado ativo da OS {codigoPDF.group()}")
                        continue
                else:
                    print("não encotrado código")
                    continue
    else:
        print("nenhum texto foi extraído")
        return

