import os
import pymupdf
from tkinter import Tk, filedialog
import zipfile
import rarfile

caminho_pasta = str

print(caminho_pasta)

def descompactar_arquivo(arquivo, pasta):
    """
    Descompacta arquivos .zip ou .rar na pasta especificada.
    
    Args:
        arquivo (str): Nome do arquivo a descompactar
        pasta (str): Caminho da pasta contendo o arquivo
        
    Returns:
        str: Mensagem de sucesso ou erro
    """
    rarfile.UNRAR_TOOL = r"C:\Program Files\WinRAR\UnRAR.exe"
    
    caminho_completo = os.path.join(pasta, arquivo)
    extensao = arquivo.lower()
    
    try:
        if extensao.endswith(".zip"):
            with zipfile.ZipFile(caminho_completo, "r") as zip_ref:
                zip_ref.extractall(pasta)
            return "PDF descompactados"
            
        elif extensao.endswith(".rar"):
            with rarfile.RarFile(caminho_completo, "r") as rar_ref:
                rar_ref.extractall(pasta)
            return "PDF descompactados"
            
        else:
            return "Formato de arquivo não suportado"
            
    except zipfile.BadZipFile:
        return "Não há arquivos zip válidos na pasta selecionada"
    except rarfile.BadRarFile:
        return "Não há arquivos rar válidos na pasta selecionada"
    except Exception as e:
        return f"Erro ao descompactar: {str(e)}"
                
def extrair_texto() -> dict[str, str]:
    root = Tk()
    root.withdraw()

    pasta = filedialog.askdirectory(title="Selecione a pasta com os PDFs")

    if not pasta:
        status = "operação foi cancelada pelo usuário (não foi selecionada nenhuma pasta)"
        return status
    
    global caminho_pasta
    caminho_pasta = pasta
    print(caminho_pasta)
    pdfs: dict[str, str] = {}

    for arquivo_compactado in (os.listdir(pasta)):
        
        
        if not os.path.isfile(arquivo_compactado):
            descompactar_arquivo(arquivo_compactado, pasta)

        
    for nome_pdf in (os.listdir(pasta)): 
        if nome_pdf.lower().endswith(".pdf"):
            caminho = os.path.join(pasta, nome_pdf)

            try:
                arquivo = pymupdf.open(caminho)
                texto = "".join(pagina.get_text() for pagina in arquivo)
                arquivo.close()

                pdfs[nome_pdf] = texto
                
            except Exception as e:
                print(f"Erro ao ler '{nome_pdf}': {e}")
                
            
    if not pdfs:
        print("Nenhum PDF encontrado na pasta.")

    return pdfs


