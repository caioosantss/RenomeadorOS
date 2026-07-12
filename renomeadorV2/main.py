"""
Arquivo principal do Renomeador de OS
Executa a aplicação da interface gráfica
"""

import sys
import os


# Adiciona o diretório ao path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from interface.principal import app
from interface.principal import fechar_app

app.protocol("WM_DELETE_WINDOW", fechar_app)

if __name__ == "__main__":
    app.mainloop()
    