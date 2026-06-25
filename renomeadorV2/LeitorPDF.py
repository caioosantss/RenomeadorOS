import pymupdf
from tkinter import Tk, filedialog
import os


caminho_pasta = {}
def extrair_texto():
    root = Tk()
    root.withdraw()
    dados = []

    pasta = filedialog.askdirectory(
    title="Selecione a pasta",
)
    caminho_pasta["pasta"] = pasta
    for PDF in os.listdir(pasta):
        if PDF.lower().endswith('.pdf'):
            caminho = os.path.join(pasta, PDF)
            arquivo = pymupdf.open(caminho) 
        
        for pagina in arquivo:
            texto = pagina.get_text()
            dados.append(texto)
    return dados
        
