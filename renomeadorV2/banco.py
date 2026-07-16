import sqlite3
import os
from datetime import datetime


class database:
    def __init__(self):
        
        base_dir = os.path.dirname(os.path.abspath(__file__)) 
        
        db_path = os.path.join( 
            base_dir, "database", "database.db")
        
        self.conexao = sqlite3.connect(db_path)
        self.cur = self.conexao.cursor()
        self.executar = self.cur.execute

    def criar_banco(self):
        """Cria a tabela de ativos se não existir"""
        self.executar("""
            CREATE TABLE IF NOT EXISTS dados(
                ativos TEXT PRIMARY KEY,
                descrição TEXT
            )
        """)
        self.conexao.commit()
        
    def admin(self):
        self.executar("DELETE FROM dados WHERE ativos IS NULL AND descrição IS NULL;")
        print("apagado")
    
    def criar_tabela_historico(self):
        """Cria a tabela de histórico de renomeações"""
        self.executar("""
            CREATE TABLE IF NOT EXISTS historico_renomeacoes(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                novo_nome TEXT NOT NULL,
                nome_antigo TEXT NOT NULL,
                horario TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                alteracoes TEXT NOT NULL
            )
        """)
        self.conexao.commit()
        
    def criar_tabela_Tipo_OS(self):
        self.executar("""
            CREATE TABLE IF NOT EXISTS tipo_OS(
                tipo_OS TEXT PRIMARY KEY
            )   
    """)
    
    def registrar_historico(self, novo_nome, nome_antigo, alteracoes="Renomeação"):
        """
        Registra uma renomeação no histórico
        
        Args:
            novo_nome: Novo nome do arquivo
            nome_antigo: Nome antigo do arquivo
            alteracoes: Descrição da alteração
        """
        horario = datetime.now().strftime("%H:%M:%S")
        self.executar("""
            INSERT INTO historico_renomeacoes (novo_nome, nome_antigo, horario, alteracoes)
            VALUES (?, ?, ?, ?)
        """, (novo_nome, nome_antigo, horario, alteracoes))
        self.conexao.commit()
    
    def consultar_historico(self, limite=None):
        """
        Consulta o histórico de renomeações
        
        Args:
            limite: Número máximo de registros a retornar (None = todos)
            
        Returns:
            Lista com tuplas (id, novo_nome, nome_antigo, horario, alteracoes)
        """
        if limite:
            self.executar("""
                SELECT id, novo_nome, nome_antigo, horario, alteracoes 
                FROM historico_renomeacoes 
                ORDER BY id DESC LIMIT ?
            """, (limite,))
        else:
            self.executar("""
                SELECT id, novo_nome, nome_antigo, horario, alteracoes 
                FROM historico_renomeacoes 
                ORDER BY id DESC
            """)
        return self.cur.fetchall()
    
    def limpar_historico(self):
        """Limpa todo o histórico de renomeações"""
        self.executar("DELETE FROM historico_renomeacoes")
        self.conexao.commit()

    def registrar_ativo(self, codigo_ativo, descricao=""):
        """
        Registra um novo ativo
        
        Args:
            codigo_ativo: Código de identificação do ativo
            descricao: Descrição do ativo
        """
        self.executar(
            "SELECT 1 FROM tipo_os WHERE ativos = ?",
            (codigo_ativo,)
        )

        resultado = self.cur.fetchone()
        
        if resultado is None:
            self.executar("""
                INSERT INTO dados (ativos, descrição)
                VALUES (?, ?)
            """, (codigo_ativo, descricao)) 
            self.conexao.commit()

            return True
        else:
   
            return False
        
    def registrar_Tipo_OS(self, codigo,):
        """
        Registra um novo ativo
        
        Args:
            codigo_ativo: Código de identificação do ativo
            descricao: Descrição do ativo
        """
        self.executar(
            "SELECT 1 FROM tipo_OS WHERE tipo_OS = ?",
            (codigo,)
        )

        resultado = self.cur.fetchone()
        
        if resultado is None:
            self.executar("""
                INSERT INTO tipo_OS (tipo_OS)
                VALUES (?)
            """, (codigo,)) 
            self.conexao.commit()

            return True
        else:
   
            return False

    def verificar_ativos(self):
        """Retorna lista de todos os ativos cadastrados"""
        self.executar("SELECT ativos FROM dados WHERE ativos IS NOT NULL;")
        dados = self.cur.fetchall()
        resultado = []

        for n in range(len(dados)):
            resultado.append(dados[n][0])

        return resultado
    
    def verificar_descricao(self):
        """Retorna lista de todas as descrições cadastradas"""
        self.executar("SELECT descrição FROM dados")
        dados = self.cur.fetchall()
        resultado = []

        for n in range(len(dados)):
            resultado.append(dados[n][0])

        return resultado
    
    def verificar_Tipo_OS(self):
        """Retorna lista de todos os tipos OS cadastrados"""
        self.executar("SELECT tipo_OS FROM tipo_OS")
        dados = self.cur.fetchall()
        resultado = []

        for n in range(len(dados)):
            resultado.append(dados[n][0])

        print(resultado)
        return resultado    
    
    def alterar_ativo(self):
        ativo = input("qual ativo deseja alterar?")
        novo_nome = input("qual sera o novo nome? ")
        
        
        self.executar(
            "SELECT 1 FROM dados WHERE ativos = ?",
            (ativo,)
        )

        resultado = self.cur.fetchone()
               
        if resultado is not None:
        
            self.executar(
                """
                UPDATE dados 
                set ativos = ?
                where ativos = ?  
                      """, (novo_nome, ativo, ))
            self.conexao.commit()
            
        else:
            print("o ativo não foi localizado")
            return

    def alterar_descricao(self):
        ativo = input("qual ativo deseja alterar a descricao?")
        nova_descricao = input("insira a nova descrição")
        
        while nova_descricao == "":
            nova_descricao = input("insira a nova descrição")

 
        self.executar(
            "SELECT 1 FROM dados WHERE ativos = ?",
            (ativo,)
        )

        resultado = self.cur.fetchone()
               
        if resultado is not None:
        
            self.executar(
                """
                UPDATE dados 
                set descrição = ?
                where ativos = ?  
                      """, (nova_descricao, ativo, ))
            self.conexao.commit()
            
        else:
            print("o ativo não foi localizado")
            return
              
data = database()
data.criar_banco()
data.criar_tabela_Tipo_OS()
data.criar_tabela_historico()


            