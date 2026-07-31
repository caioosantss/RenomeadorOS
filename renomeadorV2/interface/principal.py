import customtkinter as ctk
from PIL import Image
import os
from datetime import datetime
from .servicos import ServicoInterface
import sys

# ============================
# CONFIGURAÇÃO GERAL
# ============================
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

AZUL_ESCURO  = "#1a3a5c"
AZUL_MEDIO   = "#1e4d7b"
AZUL_BOTAO   = "#1f5fa6"
AZUL_CONSOLE = "#0f2035"
AZUL_PAINEL  = "#132840"
BRANCO       = "#ffffff"
CINZA_BORDA  = "#d0d7de"
CINZA_HEADER = "#f4f6f8"
CINZA_TEXTO  = "#8a9bb0"
TEXTO_CLARO  = "#ffffff"
TEXTO_ESCURO = "#1a1a2e"
VERDE_LOG    = "#4fc97e"
AMARELO      = "#f0a500"

if getattr(sys, 'frozen', False):
    SCRIPT_DIR = sys._MEIPASS
    PARENT_DIR = sys._MEIPASS
else:
    SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
    PARENT_DIR = os.path.dirname(SCRIPT_DIR)

def fechar_app():
        """Fecha a aplicação"""
        app.quit()
        app.destroy()
        sys.exit(0)

def carregar_imagem(nome_arquivo, tamanho):
    """Carrega uma imagem do diretório assets"""
    caminho = os.path.join(PARENT_DIR, nome_arquivo)
    if os.path.exists(caminho):
        return ctk.CTkImage(Image.open(caminho), size=tamanho)
    return None

def hora_atual():
    """Retorna a hora atual formatada"""
    return datetime.now().strftime("%H:%M:%S")


# ============================
# JANELA PRINCIPAL
# ============================
app = ctk.CTk()
app.title("Renomeador de Ordens de Servico")
app.geometry("1024x600")
app.resizable(False, False)
app.configure(fg_color=BRANCO)

# ============================
# CONSOLE E FUNÇÕES
# ============================
console_text = None  # Será inicializado depois

def console_log(msg, nivel="INFO"):
    """Escreve uma mensagem no console"""
    global console_text
    if console_text:
        console_text.configure(state="normal")
        console_text.insert("end", f"[{hora_atual()}] [{nivel}]  {msg}\n")
        console_text.see("end")
        console_text.configure(state="disabled")

def limpar_console():
    """Limpa o console"""
    global console_text
    if console_text:
        console_text.configure(state="normal")
        console_text.delete("1.0", "end")
        console_text.configure(state="disabled")

# Inicializa serviços
servicos = ServicoInterface(console_log)

# ============================
# JANELAS SECUNDÁRIAS
# ============================
def abrir_historico():
    """Abre janela de histórico de operações"""
    win = ctk.CTkToplevel(app)
    win.title("Histórico de Operações")
    win.geometry("640x440")
    win.resizable(False, False)
    win.configure(fg_color=BRANCO)
    win.grab_set()

    ctk.CTkLabel(
        win, text="HISTÓRICO DE OPERAÇÕES",
        font=ctk.CTkFont(size=16, weight="bold"),
        text_color=AZUL_ESCURO
    ).pack(pady=(20, 12))

    frame = ctk.CTkScrollableFrame(win, fg_color=AZUL_CONSOLE, corner_radius=10)
    frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))

    # Busca histórico do banco de dados
    historico = servicos.consultar_historico()
    
    if historico:
        for registro in historico:
            # registro: (id, novo_nome, nome_antigo, horario, alteracoes)
            texto = f"[{registro[3]}]  {registro[4]} | {registro[1]} ← {registro[2]}"
            ctk.CTkLabel(
                frame, text=texto,
                font=ctk.CTkFont(family="Courier", size=11),
                text_color=VERDE_LOG, anchor="w"
            ).pack(fill="x", padx=12, pady=4)
    else:
        ctk.CTkLabel(
            frame, text="Nenhum histórico disponível",
            font=ctk.CTkFont(size=12),
            text_color=CINZA_TEXTO, anchor="w"
        ).pack(fill="x", padx=12, pady=20)


def abrir_consultar_ativos():
    """Abre janela para consultar ativos"""
    win = ctk.CTkToplevel(app)
    win.title("Consultar Ativos")
    win.geometry("640x440")
    win.resizable(False, False)
    win.configure(fg_color=BRANCO)
    win.grab_set()

    ctk.CTkLabel(
        win, text="CONSULTAR ATIVOS",
        font=ctk.CTkFont(size=16, weight="bold"),
        text_color=AZUL_ESCURO
    ).pack(pady=(20, 12))


    frame = ctk.CTkScrollableFrame(win, fg_color=AZUL_PAINEL, corner_radius=10)
    frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))

    # Busca ativos do banco de dados
    ativos = servicos.consultar_ativos()

    descricaos = servicos.consultar_descricao()

    if ativos:
        ctk.CTkLabel(
            frame,
            text="Ativo",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color=BRANCO
        ).grid(row=0, column=0, sticky="w", padx=(12, 30), pady=(10, 5))

        ctk.CTkLabel(
            frame,
            text="Descrição",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color=BRANCO
        ).grid(row=0, column=1, sticky="w", padx=12, pady=(10, 5))

        # 'linha' controla o índice da linha no grid, pois a linha 0 foi
        # reservada para os títulos das colunas.
        for linha, (ativo, descricao) in enumerate(zip(ativos, descricaos), start=1):
            ctk.CTkLabel(
                frame,
                text=f"  {ativo}",
                font=ctk.CTkFont(size=12),
                text_color=VERDE_LOG,
                anchor="w"
            ).grid(row=linha, column=0, sticky="w", padx=(12, 30), pady=5)

            ctk.CTkLabel(
                frame,
                text=f"  {descricao}",
                font=ctk.CTkFont(size=12),
                text_color=VERDE_LOG,
                anchor="w"
            ).grid(row=linha, column=1, sticky="w", padx=12, pady=5)

            def criar_comando_excluir(a=ativo):
                if servicos.excluir_ativos:
                    servicos.excluir_ativos(a)
                    win.destroy() 
                    abrir_consultar_ativos() 

            ctk.CTkButton(
                frame, 
                text="excluir", 
                width=60, 
                height=22,
                fg_color="transparent",      
                command=criar_comando_excluir
            ).grid(row=linha, column=2, sticky="w", padx=25, pady=5)

    else:
        ctk.CTkLabel(
            frame,
            text="Nenhum ativo cadastrado",
            font=ctk.CTkFont(size=12),
            text_color=CINZA_TEXTO,
            anchor="w"
        ).grid(row=0, column=0, sticky="w", padx=12, pady=20)

def abrir_cadastrar_ativos():
    """Abre janela para cadastrar novo ativo"""
    win = ctk.CTkToplevel(app)
    win.title("Cadastrar Ativo")
    win.geometry("500x320")
    win.resizable(False, False)
    win.configure(fg_color=BRANCO)
    win.grab_set()

    ctk.CTkLabel(
        win, text="CADASTRAR ATIVO",
        font=ctk.CTkFont(size=16, weight="bold"),
        text_color=AZUL_ESCURO
    ).pack(pady=(20, 16))

    form = ctk.CTkFrame(win, fg_color=AZUL_ESCURO, corner_radius=12)
    form.pack(fill="both", expand=True, padx=20, pady=(0, 20))

    # Campos do formulário
    ctk.CTkLabel(
        form, text="Codigo do Ativo",
        font=ctk.CTkFont(size=12, weight="bold"),
        text_color=TEXTO_CLARO, anchor="w"
    ).pack(fill="x", padx=16, pady=(14, 2))

    entry_codigo = ctk.CTkEntry(
        form, placeholder_text="Digite o código...",
        height=36, corner_radius=8,
        fg_color=BRANCO, text_color=TEXTO_ESCURO,
        border_color=AZUL_BOTAO, border_width=1
    )
    entry_codigo.pack(fill="x", padx=16)

    ctk.CTkLabel(
        form, text="Descricao",
        font=ctk.CTkFont(size=12, weight="bold"),
        text_color=TEXTO_CLARO, anchor="w"
    ).pack(fill="x", padx=16, pady=(14, 2))

    entry_descricao = ctk.CTkEntry(
        form, placeholder_text="Digite a descrição...",
        height=36, corner_radius=8,
        fg_color=BRANCO, text_color=TEXTO_ESCURO,
        border_color=AZUL_BOTAO, border_width=1
    )
    entry_descricao.pack(fill="x", padx=16)

    def salvar_ativo():
        """Salva o ativo no banco de dados"""
        codigo = entry_codigo.get()
        descricao = entry_descricao.get()
        
        if servicos.cadastrar_ativo(codigo, descricao):
            entry_codigo.delete(0, "end")
            entry_descricao.delete(0, "end")

    ctk.CTkButton(
        form, text="Salvar Ativo",
        height=40, corner_radius=8,
        fg_color=AZUL_BOTAO, hover_color="#174a82",
        font=ctk.CTkFont(size=13, weight="bold"),
        command=salvar_ativo
    ).pack(padx=16, pady=20, fill="x")

#  tipos de OS

def abrir_consultar_tipos_OS():
    """Abre janela para tipos de OS"""
    win = ctk.CTkToplevel(app)
    win.title("Consultar tipos de OS")
    win.geometry("640x440")
    win.resizable(False, False)
    win.configure(fg_color=BRANCO)
    win.grab_set()

    ctk.CTkLabel(
        win, text="CONSULTAR TIPOS DE OS",
        font=ctk.CTkFont(size=16, weight="bold"),
        text_color=AZUL_ESCURO
    ).pack(pady=(20, 12))



    frame = ctk.CTkScrollableFrame(win, fg_color=AZUL_PAINEL, corner_radius=10)
    frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))

    # Busca ativos do banco de dados
    tipos_OS = servicos.consultar_tipo_OS()


    if tipos_OS:
        ctk.CTkLabel(
            frame,
            text="TIPOS DE OS",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color=BRANCO
        ).grid(row=0, column=0, sticky="w", padx=(12, 30), pady=(10, 5))


        # 'linha' controla o índice da linha no grid, pois a linha 0 foi
        # reservada para os títulos das colunas.
        for linha, (tipo,) in enumerate(zip(tipos_OS), start=1):
            ctk.CTkLabel(
                frame,
                text=f"  {tipo}",
                font=ctk.CTkFont(size=12),
                text_color=VERDE_LOG,
                anchor="w"
            ).grid(row=linha, column=0, sticky="w", padx=(12, 30), pady=5)

            def criar_comando_excluir(t=tipo):
                if servicos.excluir_tipos_OS:
                    servicos.excluir_tipos_OS(t)
                    win.destroy() 
                    abrir_consultar_tipos_OS() 

            ctk.CTkButton(
                frame, 
                text="excluir", 
                width=60, 
                height=22,
                fg_color="transparent",      
                command=criar_comando_excluir
            ).grid(row=linha, column=2, sticky="w", padx=25, pady=5)


    else:
        ctk.CTkLabel(
            frame,
            text="Nenhum tipo de OS cadastrado",
            font=ctk.CTkFont(size=12),
            text_color=CINZA_TEXTO,
            anchor="w"
        ).grid(row=0, column=0, sticky="w", padx=12, pady=20)


def abrir_cadastrar_tipos_OS():
    """Abre janela para cadastrar novo tipo de OS"""
    win = ctk.CTkToplevel(app)
    win.title("Cadastrar tipo de OS")
    win.geometry("500x320")
    win.resizable(False, False)
    win.configure(fg_color=BRANCO)
    win.grab_set()

    ctk.CTkLabel(
        win, text="CADASTRAR TIPO OS",
        font=ctk.CTkFont(size=16, weight="bold"),
        text_color=AZUL_ESCURO
    ).pack(pady=(20, 16))

    form = ctk.CTkFrame(win, fg_color=AZUL_ESCURO, corner_radius=12)
    form.pack(fill="both", expand=True, padx=20, pady=(0, 20))

    # Campos do formulário
    ctk.CTkLabel(
        form, text="tipo de OS",
        font=ctk.CTkFont(size=12, weight="bold"),
        text_color=TEXTO_CLARO, anchor="w"
    ).pack(fill="x", padx=16, pady=(14, 2))

    entry_codigo = ctk.CTkEntry(
        form, placeholder_text="Digite o código...",
        height=36, corner_radius=8,
        fg_color=BRANCO, text_color=TEXTO_ESCURO,
        border_color=AZUL_BOTAO, border_width=1
    )
    entry_codigo.pack(fill="x", padx=16)


    def salvar_tipo():
        """Salva o tipo no banco de dados"""
        tipo = entry_codigo.get()
        
        if servicos.cadastrar_tipo_OS(tipo):
            entry_codigo.delete(0, "end")

    ctk.CTkButton(
        form, text="Salvar tipo de OS",
        height=40, corner_radius=8,
        fg_color=AZUL_BOTAO, hover_color="#174a82",
        font=ctk.CTkFont(size=13, weight="bold"),
        command=salvar_tipo
    ).pack(padx=16, pady=20, fill="x")

# ============================
# HEADER
# ============================
header = ctk.CTkFrame(app, fg_color=CINZA_HEADER, height=82, corner_radius=0)
header.pack(fill="x")
header.pack_propagate(False)

#caso queira que a logo de sua organização apareça, coloque o arquivo .png na pasta assets e modifique a linha abaixo
logo_img = carregar_imagem("assets/logo.png", (175, 64))
if logo_img:
    ctk.CTkLabel(header, image=logo_img, text="").place(x=16, y=9)
else:
    ctk.CTkLabel(
        header, text="", font=ctk.CTkFont(size=22, weight="bold"),
        text_color=AZUL_ESCURO
    ).place(x=16, y=24)

titulo_frame = ctk.CTkFrame(header, fg_color="transparent")
titulo_frame.place(relx=0.5, rely=0.5, anchor="center")

ctk.CTkLabel(
    titulo_frame,
    text="RENOMEADOR DE ORDENS DE SERVICO",
    font=ctk.CTkFont(size=20, weight="bold"),
    text_color=AZUL_ESCURO
).pack()

ctk.CTkLabel(
    titulo_frame,
    text="Sistema para renomeacao e gerenciamento de Ordens de Servico",
    font=ctk.CTkFont(size=11),
    text_color=CINZA_TEXTO
).pack()

ctk.CTkFrame(app, height=1, fg_color=CINZA_BORDA, corner_radius=0).pack(fill="x")

# ============================
# CORPO
# ============================
body = ctk.CTkFrame(app, fg_color=BRANCO, corner_radius=0)
body.pack(fill="both", expand=True)

# ============================
# CENTRO
# ============================
center = ctk.CTkFrame(body, fg_color=BRANCO, corner_radius=0)
center.pack(side="left", fill="both", expand=True, padx=(14, 8), pady=14)

# Painel superior — ação principal
action_panel = ctk.CTkFrame(center, fg_color=AZUL_PAINEL, corner_radius=14)
action_panel.pack(fill="x", pady=(0, 12))

# Ícone circular
icon_circle = ctk.CTkFrame(action_panel, fg_color=AZUL_PAINEL,
                            width=90, height=90, corner_radius=45)
icon_circle.pack(side="left", padx=24, pady=20)
icon_circle.pack_propagate(False)
ctk.CTkLabel(
    icon_circle, text="",
    font=ctk.CTkFont(size=22, weight="bold"),
).place(relx=0.5, rely=0.5, anchor="center")

# Texto + botão
action_info = ctk.CTkFrame(action_panel, fg_color="transparent")
action_info.pack(side="left", fill="both", expand=True, pady=20)

ctk.CTkLabel(
    action_info, text="RENOMEAR OS",
    font=ctk.CTkFont(size=20, weight="bold"),
    text_color=TEXTO_CLARO, anchor="w"
).pack(anchor="w")

ctk.CTkLabel(
    action_info,
    text="Inicie o processo de renomeacao de Ordens de Servico.",
    font=ctk.CTkFont(size=12),
    text_color=CINZA_TEXTO, anchor="w"
).pack(anchor="w", pady=(2, 12))

ctk.CTkButton(
    action_info,
    text="  RENOMEAR OS",
    font=ctk.CTkFont(size=14, weight="bold"),
    height=42, width=220,
    corner_radius=10,
    fg_color=AZUL_BOTAO,
    hover_color=AZUL_MEDIO,
    text_color=TEXTO_CLARO,
    anchor="w",
    command=servicos.renomear_os
).pack(anchor="w")

# Console
console_frame = ctk.CTkFrame(center, fg_color=AZUL_PAINEL, corner_radius=14,
                              border_color=AZUL_MEDIO, border_width=1)
console_frame.pack(fill="both", expand=True)

console_header = ctk.CTkFrame(console_frame, fg_color="transparent")
console_header.pack(fill="x", padx=14, pady=(10, 2))

ctk.CTkLabel(
    console_header, text="CONSOLE DE SAIDA",
    font=ctk.CTkFont(size=10, weight="bold"),
    text_color=AZUL_BOTAO
).pack(side="left")

ctk.CTkButton(
    console_header, text="  Limpar console",
    font=ctk.CTkFont(size=11),
    height=28, width=130,
    corner_radius=8,
    fg_color=AZUL_MEDIO,
    hover_color=AZUL_ESCURO,
    text_color=TEXTO_CLARO,
    command=limpar_console
).pack(side="right")

console_text = ctk.CTkTextbox(
    console_frame,
    fg_color=AZUL_PAINEL,
    text_color=VERDE_LOG,
    font=ctk.CTkFont(family="Courier", size=12),
    corner_radius=0, border_width=0,
    wrap="word", state="disabled"
)
console_text.pack(fill="both", expand=True, padx=10, pady=(0, 10))

console_log("Iniciando sistema...")
console_log("Aguardando acao do usuario...")

# ============================
# COLUNA DIREITA
# ============================
right = ctk.CTkFrame(body, fg_color=AZUL_PAINEL, corner_radius=14, width=220)
right.pack(side="right", fill="y", padx=(0, 14), pady=14)
right.pack_propagate(False)

# Título MENU centralizado
ctk.CTkLabel(
    right, text="MENU",
    font=ctk.CTkFont(size=14, weight="bold"),
    text_color=TEXTO_CLARO,
    anchor="center"
).pack(fill="x", pady=(16, 10), padx=14)

# Botões principais do menu
botoes_menu = [
    ("Historico",        abrir_historico,        "transparent"),
    ("Consultar Ativos", abrir_consultar_ativos, "transparent"),
    ("Cadastrar Ativos", abrir_cadastrar_ativos, "transparent"),
    ("Consultar tipos de OS", abrir_consultar_tipos_OS, "transparent"),
    ("Cadastrar tipo de OS", abrir_cadastrar_tipos_OS, "transparent"),
]

for texto, cmd, cor in botoes_menu:
    ctk.CTkButton(
        right, text=texto,
        font=ctk.CTkFont(size=13),
        height=40, corner_radius=10,
        fg_color=cor,
        hover_color=AZUL_BOTAO,
        text_color=TEXTO_CLARO,
        border_width=1 if cor == "transparent" else 0,
        border_color=AZUL_BOTAO,
        anchor="center",
        command=cmd
    ).pack(fill="x", padx=14, pady=3)

# Botão Desfazer logo abaixo dos demais
ctk.CTkButton(
    right, text="Desfazer ultima renomeação",
    font=ctk.CTkFont(size=12),
    height=38, corner_radius=10,
    fg_color="transparent",
    hover_color="#7a1a1a",
    text_color="#e07070",
    border_width=1,
    border_color="#7a3030",
    anchor="center",
    command=servicos.desfazer_acao
).pack(fill="x", padx=14, pady=(3, 0))

# Separador e Resumo Rápido

# ============================
# RODAPÉ
# ============================
footer = ctk.CTkFrame(app, fg_color=AZUL_PAINEL, height=36, corner_radius=0)
footer.pack(fill="x", side="bottom")
footer.pack_propagate(False)

footer.columnconfigure(0, weight=1)
footer.columnconfigure(1, weight=1)
footer.columnconfigure(2, weight=1)
footer.rowconfigure(0, weight=1)

ctk.CTkLabel(
    footer,
    text=f"Ultima atualizacao: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}",
    font=ctk.CTkFont(size=10),
    text_color=CINZA_TEXTO
).grid(row=0, column=0, padx=20, sticky="w")

ctk.CTkLabel(
    footer,
    text="Versao: 2.0.0",
    font=ctk.CTkFont(size=10),
    text_color=CINZA_TEXTO
).grid(row=0, column=1)

ctk.CTkLabel(
    footer,
    #texto abaixo tem como espaço livre para colocar o nome de sua organização no rodapé
    text="",
    font=ctk.CTkFont(size=10),
    text_color=CINZA_TEXTO
).grid(row=0, column=2, padx=20, sticky="e")

if __name__ == "__main__":
    app.mainloop()
