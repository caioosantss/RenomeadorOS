import re
import os
from LeitorPDF import extrair_texto
from LeitorPDF import caminho_pasta
import banco


def renomear():

    codigo = re.compile(r'\b(?!3)\d{8}(?=\s)')
    arquivos = extrair_texto()
    ativos = banco.data.verificar_ativos()

renomear()