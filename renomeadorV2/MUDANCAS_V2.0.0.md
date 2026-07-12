# RENOMEADOR DE OS - DOCUMENTAÇÃO DE MUDANÇAS v2.0.0

## 📋 Resumo das Alterações

Este documento descreve todas as mudanças implementadas na versão 2.0.0 do projeto Renomeador de Ordens de Serviço.

---

## 1️⃣ DIVISÃO DO ARQUIVO interface.py

### Antes:
- Um único arquivo `interface.py` com toda a lógica da interface

### Depois:
- **Pasta `interface/`** criada contendo:
  - `principal.py` - Janela principal e componentes visuais
  - `servicos.py` - Funções de serviços desacopladas
  - `__init__.py` - Inicialização do módulo

### Estrutura:
```
interface/
├── __init__.py
├── principal.py      (Janela principal, layouts, componentes)
└── servicos.py       (Funções de negócio, chamadas ao banco)
```

---

## 2️⃣ VINCULAÇÃO DE BOTÕES ÀS FUNÇÕES

### Botão: RENOMEAR OS
- **Arquivo:** `interface/principal.py` (linha ~265)
- **Comando:** `servicos.renomear_os()`
- **Função Original:** `renomeador.renomear()`
- **Comportamento:**
  - Abre diálogo de seleção de pasta
  - Processa arquivos PDF
  - Registra renomeações no histórico
  - Exibe logs no console da interface

### Botão: CADASTRAR ATIVOS
- **Arquivo:** `interface/principal.py` (janela secundária)
- **Comando:** `servicos.cadastrar_ativo(codigo, descricao)`
- **Função Original:** `banco.registrar_ativo()`
- **Comportamento:**
  - Valida entrada de código
  - Salva no banco de dados
  - Exibe confirmação no console

### Botão: CONSULTAR ATIVOS
- **Arquivo:** `interface/principal.py` (janela secundária)
- **Comando:** `servicos.consultar_ativos()`
- **Função Original:** `banco.verificar_ativos()`
- **Comportamento:**
  - Lista todos os ativos cadastrados
  - Exibe no console e na janela
  - Mostra total de ativos

### Botão: HISTÓRICO
- **Arquivo:** `interface/principal.py` (janela secundária)
- **Comando:** `servicos.consultar_historico()`
- **Função Original:** `banco.consultar_historico()`
- **Comportamento:**
  - Exibe histórico de renomeações
  - Mostra: horário, arquivo antigo, arquivo novo
  - Exibe no console e na janela

### Botão: DESFAZER ÚLTIMA AÇÃO
- **Arquivo:** `interface/principal.py` (linha ~385)
- **Comando:** `servicos.desfazer_acao()`
- **Função Original:** `renomeador.desfazer_acao()`
- **Comportamento:**
  - Reverte última renomeação
  - Retorna arquivos ao nome antigo
  - Registra ação no histórico

---

## 3️⃣ SAÍDAS NO CONSOLE

### Todas as funções agora usam:
```python
console_log(mensagem, nivel)
```

### Níveis de Log:
- `INFO` - Informações gerais
- `SUCCESS` - Operação bem-sucedida ✓
- `WARNING` - Aviso ⚠️
- `ERROR` - Erro ✗

### Exemplo:
```python
console_log("Ativo cadastrado com sucesso", "SUCCESS")
console_log("Nenhum arquivo foi renomeado", "WARNING")
console_log("Erro ao conectar ao banco", "ERROR")
```

---

## 4️⃣ ATUALIZAÇÃO DO ARQUIVO banco.py

### Novas Funções:

#### `criar_tabela_historico()`
- Cria a tabela `historico_renomeacoes`
- Campos:
  - `id` (PRIMARY KEY)
  - `novo_nome` (TEXT)
  - `nome_antigo` (TEXT)
  - `horario` (TIMESTAMP)
  - `alteracoes` (TEXT - descrição da alteração)

#### `registrar_historico(novo_nome, nome_antigo, alteracoes)`
- Registra uma renomeação no histórico
- Chamada automaticamente ao renomear arquivos
- Exemplo:
```python
banco.data.registrar_historico(
    "OS 12345678 CORRETIVA.pdf",
    "file_corretiva.pdf",
    "Renomeação automática"
)
```

#### `consultar_historico(limite=None)`
- Retorna histórico de renomeações
- Parâmetro `limite` (opcional): número máximo de registros
- Retorna: Lista de tuplas `(id, novo_nome, nome_antigo, horario, alteracoes)`
- Ordenado por data decrescente
- Exemplo:
```python
historico = banco.data.consultar_historico(limite=10)  # Últimas 10
historico = banco.data.consultar_historico()  # Todas
```

#### `limpar_historico()`
- Limpa todo o histórico
- Útil para resetar o sistema

#### `registrar_ativo(codigo_ativo, descricao="")`
- Refatoração da função anterior
- Agora retorna `True/False` indicando sucesso
- Integrada com interface

### Funções Mantidas:
- `criar_banco()` - Cria tabela de ativos
- `verificar_ativos()` - Lista ativos
- `alterar_ativo()` - Altera código do ativo
- `alterar_descricao()` - Altera descrição

---

## 5️⃣ ATUALIZAÇÃO DO ARQUIVO renomeador.py

### Função `renomear(console_log=None)`

**Assinatura:**
```python
def renomear(console_log=None):
```

**Parâmetros:**
- `console_log` (função, opcional): Função para escrever no console

**Retorna:**
- Lista de tuplas `(nome_antigo, nome_novo)` dos arquivos renomeados

**Comportamento:**
- Extrai PDFs da pasta selecionada
- Procura padrão de código de OS (8 dígitos)
- Procura padrão de ativo cadastrado
- Renomeia para formato: `OS {codigo} {ativo}.pdf`
- Registra cada renomeação no histórico
- Exibe logs detalhados

**Exemplo de uso:**
```python
from renomeador import renomear

# Na interface
servicos.renomear_os()

# Ou manualmente
resultado = renomear(console_log=print)
```

### Função `desfazer_acao(console_log=None)` ⭐ NOVA

**Assinatura:**
```python
def desfazer_acao(console_log=None):
```

**Parâmetros:**
- `console_log` (função, opcional): Função para escrever no console

**Retorna:**
- Lista de tuplas `(nome_novo, nome_antigo)` dos arquivos desfeitos

**Comportamento:**
- Lê histórico da última renomeação
- Reverte os arquivos ao nome anterior
- Processa em ordem inversa
- Limpa o histórico após desfazer

**Limitação:**
- Só funciona com a última operação de renomeação
- Se a aplicação foi reiniciada, o histórico é perdido

**Exemplo de uso:**
```python
desfeitos = renomeador.desfazer_acao(console_log=print)
# Retorna: [('OS 12345678 CORRETIVA.pdf', 'file_corretiva.pdf'), ...]
```

---

## 6️⃣ CLASSE ServicoInterface

**Localização:** `interface/servicos.py`

Classe que centraliza todas as operações da interface:

```python
class ServicoInterface:
    def __init__(self, console_log_func)
    def renomear_os()
    def cadastrar_ativo(codigo_ativo, descricao)
    def consultar_ativos()
    def consultar_historico()
    def desfazer_acao()
```

Cada método:
- Chama a função correspondente
- Trata erros
- Registra logs no console
- Retorna resultado

---

## 📁 ESTRUTURA DO PROJETO (NOVO)

```
renomeadorV2/
├── main.py                    (Ponto de entrada principal)
├── banco.py                   (Banco de dados com histórico)
├── renomeador.py              (Lógica de renomeação + desfazer)
├── LeitorPDF.py               (Leitura de PDFs)
├── interface/
│   ├── __init__.py
│   ├── principal.py           (Janela principal)
│   └── servicos.py            (Funções de serviço)
├── assets/
│   └── logo_RGT.png
├── database/
│   └── database.db            (SQLite com histórico)
└── README.md                  (Esta documentação)
```

---

## 🚀 COMO EXECUTAR

### Opção 1: Executar main.py
```bash
python main.py
```

### Opção 2: Executar interface diretamente
```bash
python interface/principal.py
```

---

## 🔄 FLUXO DE OPERAÇÕES

### Renomear OS:
1. Usuário clica em "RENOMEAR OS"
2. Interface chama `servicos.renomear_os()`
3. Serviço chama `renomeador.renomear(console_log)`
4. Renomeador extrai PDFs e renomeia
5. Cada renomeação é registrada em `banco.registrar_historico()`
6. Logs aparecem no console
7. Histórico fica disponível para consulta e desfazer

### Desfazer Ação:
1. Usuário clica em "DESFAZER ÚLTIMA AÇÃO"
2. Interface chama `servicos.desfazer_acao()`
3. Serviço chama `renomeador.desfazer_acao(console_log)`
4. Renomeador lê histórico em memória
5. Reverte os arquivos em ordem inversa
6. Limpa histórico após desfazer
7. Logs aparecem no console

### Cadastrar Ativo:
1. Usuário clica em "CADASTRAR ATIVOS"
2. Janela secundária abre com formulário
3. Usuário preenche código e descrição
4. Clica em "SALVAR ATIVO"
5. Interface chama `servicos.cadastrar_ativo()`
6. Serviço chama `banco.registrar_ativo()`
7. Ativo é salvo no banco
8. Confirmação aparece no console

### Consultar Histórico:
1. Usuário clica em "HISTÓRICO"
2. Janela secundária abre
3. Interface chama `servicos.consultar_historico()`
4. Serviço consulta `banco.consultar_historico()`
5. Histórico é exibido na janela
6. Também aparece no console

---

## ⚠️ OBSERVAÇÕES IMPORTANTES

### Histórico em Memória
- A função `desfazer_acao()` usa variável global `historico_renomeacoes`
- Só funciona na mesma sessão
- Se reiniciar a aplicação, perde o histórico de desfazer
- Mas o histórico fica salvo no banco para consulta posterior

### Banco de Dados
- Novo arquivo: `database.db` com tabela `historico_renomeacoes`
- Compatível com SQL queries
- Pode ser consultado externamente

### Console
- Todos os prints foram redirecionados para o console da interface
- Função `console_log(msg, nivel)` padroniza mensagens
- Cores diferentes para cada nível de log

---

## 🔧 TROUBLESHOOTING

### Problema: "ModuleNotFoundError: No module named 'interface'"
**Solução:** Certifique-se de executar `main.py` do diretório raiz do projeto

### Problema: Botões não fazem nada
**Solução:** Verifique se todos os arquivos estão no local correto, especialmente `servicos.py`

### Problema: Histórico não aparece
**Solução:** Verifique se a tabela `historico_renomeacoes` foi criada no banco de dados

### Problema: Desfazer não funciona
**Solução:** 
- Verifique se há renomeações no histórico
- A função só desfaz a última operação
- Se reiniciou a app, o histórico foi limpo

---

## 📝 EXEMPLO DE USO PROGRAMÁTICO

```python
# Importar os módulos
from interface.servicos import ServicoInterface
import banco

# Inicializar serviços
def meu_console_log(msg, nivel="INFO"):
    print(f"[{nivel}] {msg}")

servicos = ServicoInterface(meu_console_log)

# Cadastrar ativo
servicos.cadastrar_ativo("UE-001", "Unidade de Energia")

# Consultar ativos
ativos = servicos.consultar_ativos()

# Renomear arquivos
servicos.renomear_os()

# Consultar histórico
historico = servicos.consultar_historico()

# Desfazer última ação
servicos.desfazer_acao()
```

---

## 📄 VERSÃO
- **Versão:** 2.0.0
- **Data:** 2026
- **Alterações principais:** 
  - Divisão da interface em módulos
  - Sistema de histórico
  - Função desfazer ação
  - Console integrado
  - Vinculação completa de botões

---

**Fim da documentação**
