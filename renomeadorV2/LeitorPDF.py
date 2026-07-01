import os
import pymupdf
from tkinter import Tk, filedialog

caminho_pasta = []

def extrair_texto() -> dict[str, str]:
    root = Tk()
    root.withdraw()

    pasta = filedialog.askdirectory(title="Selecione a pasta com os PDFs")

    if not pasta:
        print("Operação cancelada.")
        return {}
    caminho_pasta.append(pasta)
    pdfs: dict[str, str] = {}
    

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

