import pymupdf
from tkinter import Tk, filedialog
import os

def extrair_texto():
    root = Tk()
    root.withdraw()

    pasta = filedialog.askdirectory(
    title="Selecione a pasta",
)

    for PDF in os.listdir(pasta):
        caminho = os.path.join(pasta, PDF)
        texto = open(pasta) 
        print(texto)
        
extrair_texto()