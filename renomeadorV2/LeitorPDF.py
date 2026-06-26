import pymupdf
from tkinter import Tk, filedialog
import os

caminho_pasta = {}
def extrair_texto():
    root = Tk()
    root.withdraw()
    pdfs = {}
    PDFref = []

    pasta = filedialog.askdirectory(
    title="Selecione a pasta",

)
    if pasta == "":
        return print("operação cancelada")
        
    caminho_pasta["pasta"] = pasta
    for PDF in os.listdir(pasta):

        if PDF.lower().endswith('.pdf'):
            caminho = os.path.join(pasta, PDF)
            arquivo = pymupdf.open(caminho) 
        
            for contador, pagina in enumerate(arquivo):
                texto = pagina.get_text()
                PDFref.append(texto)
            pdfs[f'PDF{contador}'] = PDFref
            return print(pdfs)

        return print("nenhum PDF encontrado na pasta")
    
extrair_texto()
