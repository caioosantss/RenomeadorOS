import re
import tkinter as tk
from tkinter import filedialog
import pathlib
from pathlib import Path
from pypdf import PdfReader
import zipfile 


# =========================
# 1. SELEÇÃO DA PASTA
# =========================
root = tk.Tk()
root.withdraw()
pasta_selecionada = filedialog.askdirectory(title="Selecione a pasta com os PDFs")

if not pasta_selecionada:
    print("Nenhuma pasta selecionada.")
    exit()

diretorio = Path(pasta_selecionada)

#trata os arquivos

# =========================
# 2. REGEX
# =========================
# Captura 8 dígitos, garantindo que o próximo caractere seja um espaço ou quebra de linha,
# mas sem incluir esse caractere no nome do arquivo.
regex_os = re.compile(r'\b(?!3)\d{8}(?=\s)')

regex_ativos = re.compile(
    r'\b(UE|UC|IF|BAG|BAC|UR|QE|DE|SP|ST|CH|FC|CR|UEVRF|UCVRF|QDE|INV|UV|PR|PC|RACK|QDEG|QDFC|BAGPR)\-?[A-Z0-9]*\d[A-Z0-9]*\b'
)

regex_tipo = re.compile(
    r'\b(REQUISIÇÃO|RECEBIMENTO|ESTOQUE MÍNIMO|PREVENTIVA GERAL|CORRETIVA|QDE| VISTORIA)\b',
    re.IGNORECASE
)

# =========================
# 3. FASE 1 — RENOMEAR PDFs
# =========================

for arquivo_zip in diretorio.glob("*.zip"):
    try:
        with zipfile.ZipFile(arquivo_zip, 'r') as zipf:
            zipf.extractall(path=diretorio)
            print("arquivo zip extraído")   
                               
        arquivo_zip.unlink()           
        print("arquivo zip apagado")
            
    except:
        print("erro ao extrair")    
    

for caminho_arquivo in diretorio.glob("*.pdf"):
    try:
        leitor = PdfReader(caminho_arquivo)
        texto = "".join([pagina.extract_text() or "" for pagina in leitor.pages])

        match_os = regex_os.search(texto)

        # 1. Verifica se encontrou algo
        if not match_os:
            print(f"OS não encontrada: {caminho_arquivo.name}")
            continue
            
        # 2. Verifica se a OS encontrada é a proibida (bloqueio de segurança)
        os_num = match_os.group().strip()
        if os_num == "25585020":
            print(f"OS proibida ignorada: {os_num} em {caminho_arquivo.name}")
            continue

        # 3. Monta o nome base
        novo_nome = f"OS {os_num}"

        # 4. Busca complementos
        match_tipo = regex_tipo.search(texto)
        match_ativos = regex_ativos.search(texto)

        if match_tipo:
            novo_nome += f" {match_tipo.group().upper().strip()}"
        elif match_ativos:
            novo_nome += f" {match_ativos.group().strip()}"
        
        # Garante que não haja caracteres inválidos no nome final
        novo_nome = re.sub(r'[<>:"/\\|?*]', '', novo_nome) + ".pdf"
        
        caminho_novo = caminho_arquivo.with_name(novo_nome)
        
        if caminho_arquivo != caminho_novo:
            caminho_arquivo.rename(caminho_novo)
            print(f"Renomeado: {novo_nome}")

    except Exception as e:
        print(f"Erro ao processar {caminho_arquivo.name}: {e}")

# =========================
# 4. FASE 2 — MOVER POR TIPO
# =========================
tipos = ["REQUISIÇÃO", "ESTOQUE MÍNIMO", "CORRETIVA", "QDECAG", "RECEBIMENTO", "QUADRO ELÉTRICO"]

for caminho_arquivo in diretorio.glob("*.pdf"):
          
    for tipo in tipos:
        
        if tipo in caminho_arquivo.name.upper():
            pasta_destino = diretorio / tipo
            pasta_destino.mkdir(exist_ok=True)
            
            
            try:
                caminho_arquivo.rename(pasta_destino / caminho_arquivo.name)
                print(f"Movido para {tipo}: {caminho_arquivo.name}")
            except Exception as e:
                print(f"Erro ao mover {caminho_arquivo.name}: {e}")
            break
        
    pasta_preventivas = diretorio / "PREVENTIVAS"
    pasta_preventivas.mkdir(exist_ok=True)
            
    if caminho_arquivo in diretorio.glob("*.pdf"):
        caminho_arquivo.rename( pasta_preventivas / caminho_arquivo.name)
        print(f"movida para pasta de preventivas")

print("\nProcesso finalizado.")
