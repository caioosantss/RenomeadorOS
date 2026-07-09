import os
import pymupdf
from tkinter import Tk, filedialog
import zipfile

caminho_pasta = []

def verificar_zip(pasta):
    
    arquivos = os.listdir(pasta)

    if arquivos:
        arquivo = arquivos[0]
      
        with zipfile.ZipFile(os.path.join(pasta,arquivo), "r") as zip_ref:
            if arquivo.endswith(".zip") or arquivo.endswith("rar"):                
                zip_ref.extractall(pasta)
                return "PDF descopactados"
            else:
                return None
    else:
        return None
                
def extrair_texto() -> dict[str, str]:
    root = Tk()
    root.withdraw()

    pasta = filedialog.askdirectory(title="Selecione a pasta com os PDFs")

    if not pasta:
        print("Operação cancelada.")
        return {}
    caminho_pasta.append(pasta)
    pdfs: dict[str, str] = {}
    
    verificar_zip(pasta)
        
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


