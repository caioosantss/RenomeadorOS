import re
import os
import LeitorPDF
import banco


def renomear():
   
    arquivos = LeitorPDF.extrair_texto()
    
    if arquivos:
        codigo = re.compile(r'\b(?!3)\d{8}(?=\s)')
        ativosNT = "|".join(banco.data.verificar_ativos())
        ativos = re.compile(rf"\b({ativosNT})\-?[A-Z0-9]*\d[A-Z0-9]*\b")
        
        
    for contador in range(1, len(arquivos) + 1):
        codigoPDF = re.search(codigo, arquivos[f"PDF{contador}"])
        
        if codigoPDF:
            ativoPDF = re.search(ativos, arquivos[f'PDF{contador}'])
            return print(ativoPDF.group())
                    
renomear()