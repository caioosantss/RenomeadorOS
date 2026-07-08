import sqlite3
import os

class database:
    def __init__(self):
        
        base_dir = os.path.dirname(os.path.abspath(__file__)) 
        
        db_path = os.path.join( 
            base_dir, "database", "database.db")
        
        self.conexao = sqlite3.connect(db_path)
        self.cur = self.conexao.cursor()
        self.executar = self.cur.execute

    def criar_banco(self):
        self.executar("""
            CREATE TABLE IF NOT EXISTS dados(
                ativos TEXT PRIMARY KEY,
                descrição TEXT
            )
        """)
        self.conexao.commit()
        

    def registrar_ativos(self):
        
        
        ativo = input("qual ativo deseja inserir? ").upper()
        descricao = input("deseja inserir descriçao? ")
        
        
        self.executar(
            "SELECT 1 FROM dados WHERE ativos = ?",
            (ativo,)
        )

        resultado = self.cur.fetchone()
        
            
        if resultado is None:
                
            self.executar("""
            INSERT INTO dados (ativos, descrição)
            VALUES (?, ?)
        """, (ativo, descricao,)) 
            self.conexao.commit()
            print(f"código de identificação de OS: {ativo} cadastrado com sucesso")
        else:
            return print("não foi possivel cadastra-lo, pois o ativo ja se encontra cadastrado")
        

    def verificar_ativos(self):
        self.executar("SELECT ativos FROM dados")
        dados = self.cur.fetchall()
        resultado = []

        for n in range(len(dados)):
            resultado.append(dados[n][0])

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



            