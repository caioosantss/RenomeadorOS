import pymupdf
from tkinter import Tk, filedialog
import os

root = Tk()
root.withdraw()

pasta = filedialog.askdirectory(
    title="Selecione a pasta",
)

for PDF in os.listdir(pasta):
    caminho = os.path.join(pasta, PDF)
    print(caminho)