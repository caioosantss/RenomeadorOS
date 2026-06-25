import sqlite3

class database:
    def __init__(self):
        self.conexao = sqlite3.connect("database\database.db")
        self.cur = self.conexao.cursor()
        self.executar = self.cur.execute

    def criar_banco(self):
        self.executar("""
            CREATE TABLE IF NOT EXISTS dados(
                ativos TEXT PRIMARY KEY
            )
        """)
        self.conexao.commit()
        

    def registrar_ativos(self):
        
        ativo = input("qual ativo deseja inserir? ")
        
        self.executar(
            "SELECT 1 FROM dados WHERE ativos = ?",
            (ativo,)
        )

        resultado = self.cur.fetchone()
        
            
        if resultado is None:
                
            self.executar.fetchone("""
            INSERT INTO dados
            VALUES (?)
        """, (ativo,)) 
            self.conexao.commit()
            print(f"ativo {ativo} ja cadastrado")
        else:
            return print("ativo ja cadastrado")

    def verificar_ativos(self):
        self.executar("SELECT ativos FROM dados")
        return self.cur.fetchall()

data = database()
data.criar_banco()
        

            