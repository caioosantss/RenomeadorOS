import re
import os
import LeitorPDF
import banco


def renomear():

    codigo = re.compile(r'\b(?!3)\d{8}(?=\s)')
    arquivos = LeitorPDF.extrair_texto()
    ativos = banco.data.verificar_ativos()


print(renomear())