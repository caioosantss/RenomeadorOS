"""
Módulo de Serviços da Interface
Contém as funções que executam as ações dos botões
"""

from logging import root
import sys
import os

# Adiciona o diretório pai ao path para importar módulos
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import banco
import renomeador


class ServicoInterface:
    """Classe para gerenciar os serviços da interface"""
    
    def __init__(self, console_log_func):
        """
        Inicializa os serviços com referência da função de log
        
        Args:
            console_log_func: Função para escrever no console da interface
        """
        self.console_log = console_log_func
        self.db = banco.database()
        self.db.criar_banco()
        self.db.criar_tabela_historico()
    
    def renomear_os(self):
        """Executa a função de renomear OS e registra no histórico"""
        try:
            self.console_log("Iniciando renomeação de OS...", "INFO")
            # Chama a função renomear que retorna lista de arquivos renomeados
            resultado = renomeador.renomear(self.console_log)
            
            if resultado == "operação foi cancelada pelo usuário (não foi selecionada nenhuma pasta)":
                self.console_log("Operação cancelada pelo usuário (não foi selecionada nenhuma pasta)", "WARNING")

            elif resultado:
                self.console_log(f"Renomeação concluída: {len(resultado)} arquivo(s) processado(s)", "SUCCESS")                

            else:
                self.console_log("Nenhum arquivo foi renomeado", "WARNING")
        except Exception as e:
            self.console_log(f"Erro ao renomear OS: {str(e)}", "ERROR")
    
    def cadastrar_ativo(self, codigo_ativo, descricao):
        """
        Cadastra um novo ativo no banco de dados
        
        Args:
            codigo_ativo: Código de identificação do ativo
            descricao: Descrição do ativo
        """
        try:
            if not codigo_ativo or not codigo_ativo.strip():
                self.console_log("Código do ativo não pode estar vazio", "ERROR")
                return False
            
            ativo = self.db.registrar_ativo(codigo_ativo.upper(), descricao)
            
            if ativo:
                self.console_log(f"Ativo '{codigo_ativo.upper()}' cadastrado com sucesso", "SUCCESS")
                return True
            else:
                self.console_log(f"Ativo '{codigo_ativo.upper()}' não foi cadastrado pois ja se encontra no sistema ", "ERROR")
                return False
            
        except Exception as e:
            self.console_log(f"Erro ao cadastrar ativo: {str(e)}", "ERROR")
            return False
        
    def cadastrar_tipo_OS(self, tipo_OS):
        """
        Cadastra um novo tipo OS no banco de dados
        
        Args:
            tipo OS: Código de identificação do ativo

        """
        try:
            if not tipo_OS or not tipo_OS.strip():
                self.console_log("Código do tipo de OS não pode estar vazio", "ERROR")
                return False
            
            verificar = self.db.registrar_tipo_OS(tipo_OS.upper())
            
            if verificar:
                self.console_log(f"tipo de OS '{tipo_OS.upper()}' cadastrado com sucesso", "SUCCESS")
                return True
            else:
                self.console_log(f"tipo de OS '{tipo_OS.upper()}' não foi cadastrado pois ja se encontra no sistema ", "ERROR")
                return False
            
        except Exception as e:
            self.console_log(f"Erro ao cadastrar tipo de OS: {str(e)}", "ERROR")
            return False
    
    def consultar_ativos(self):
        """Consulta todos os ativos cadastrados e exibe no console"""
        try:
            ativos = self.db.verificar_ativos()
            
            return ativos
        except Exception as e:
            self.console_log(f"Erro ao consultar ativos: {str(e)}", "ERROR")
            return []
        
    def consultar_descricao(self):
        """Consulta todos os ativos cadastrados e exibe no console"""
        try:
            descricao = self.db.verificar_descricao()
            
            return descricao
        
        except Exception as e:
            self.console_log(f"Erro ao consultar ativos: {str(e)}", "ERROR")
            return []

    def consultar_tipo_OS(self):
        """Consulta todos os tipos de OS cadastrados e exibe no console"""
        try:
            tipos_OS = self.db.verificar_tipo_OS()
            
            return tipos_OS
        except Exception as e:
            self.console_log(f"Erro ao consultar tipos de OS: {str(e)}", "ERROR")
            return []

    def excluir_ativos(self, ativo):
        """exclui ativos do banco de dados"""
        try:
            self.db.excluir_ativo(ativo)
            self.console_log(f"Ativo {ativo} excluído com sucesso", "SUCCESS")
            return True

        except Exception as e:
            self.console_log(f"Erro ao excluir ativos: {str(e)}", "ERROR")
            return False

    def excluir_tipos_OS(self,tipo):
        """exclui ativos do banco de dados"""
        try:
            self.db.excluir_tipo_OS(tipo)
            self.console_log(f"tipo de OS {tipo} excluído com sucesso", "SUCCESS")
            return True
        except Exception as e:
            self.console_log(f"Erro ao consultar tipos de OS: {str(e)}", "ERROR")
            return False

    
    def consultar_historico(self):
        """Consulta o histórico de renomeações"""
        try:
            historico = self.db.consultar_historico()
                        
            return historico
        except Exception as e:
            self.console_log(f"Erro ao consultar histórico: {str(e)}", "ERROR")
            return []
    
    def desfazer_acao(self):
        """Desfaz a última ação de renomeação"""
        try:
            self.console_log("Desfazendo última ação...", "INFO")
            resultado = renomeador.desfazer_acao(self.console_log)
            
            if resultado:
                self.console_log(f"Ação desfeita: {len(resultado)} arquivo(s) revertido(s)", "SUCCESS")
            else:
                self.console_log("Nenhuma ação para desfazer", "WARNING")
            
            return resultado
        except Exception as e:
            self.console_log(f"Erro ao desfazer ação: {str(e)}", "ERROR")
            return False


    
    