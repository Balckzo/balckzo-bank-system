# 🏦 Banco Balckzo

Sistema bancário simples feito em **Python** com **MySQL**, rodando no terminal.

O projeto simula operações básicas de um banco real, incluindo criação de contas, autenticação de usuários, movimentações financeiras e histórico de transações.

Foi desenvolvido com foco em **aprendizado de backend, banco de dados e organização de código**.

---

# 🚀 Funcionalidades

✔ Criar conta
✔ Login com CPF e senha
✔ Senhas protegidas com **hash usando bcrypt**
✔ Depósito de dinheiro
✔ Saque de dinheiro
✔ Transferência entre contas
✔ Visualização de dados da conta
✔ Extrato das últimas movimentações
✔ Registro de todas as transações no banco de dados

---

# 🧠 Tecnologias utilizadas

* Python
* MySQL
* mysql-connector-python
* bcrypt
* Rich
* Colorama

---

# 🗂 Estrutura do projeto

```
balckzo-bank-system/

main.py          # Interface e fluxo do sistema
banco.py         # Lógica das operações bancárias

database.sql     # Script para criar o banco e tabelas
requirements.txt # Dependências do projeto
README.md
```

---

# 🗄 Estrutura do banco de dados

O sistema utiliza duas tabelas principais.

## Usuarios

Armazena os dados das contas.

Campos:

* id
* nome
* cpf
* senha (hash bcrypt)
* saldo
* criado_em

---

## Transacoes

Registra todas as movimentações financeiras.

Campos:

* id
* origem
* destino
* valor
* tipo
* data

Tipos de transação:

* Depósito
* Saque
* Transação (transferência entre contas)

---

# 📊 Extrato bancário

O sistema mostra as **8 movimentações mais recentes** da conta.

Cada registro inclui:

* nome de quem enviou
* nome de quem recebeu
* valor da transação
* tipo de operação
* data e hora

---

# ⚙ Como executar o projeto

### 1️⃣ Clonar o repositório

```
git clone https://github.com/seu-usuario/balckzo-bank-system.git
```

---

### 2️⃣ Instalar dependências

```
pip install -r requirements.txt
```

---

### 3️⃣ Criar o banco de dados

Execute o script:

```
database.sql
```

no MySQL.

---

### 4️⃣ Executar o sistema

```
python main.py
```

---

# 🎯 Objetivo do projeto

Este projeto foi criado para praticar:

* Python
* Integração com banco de dados
* Segurança de senha
* Estruturação de sistemas
* Lógica de aplicações backend
* Transações em banco de dados

---

# 📌 Observação

Este projeto é **educacional** e não deve ser usado como sistema bancário real.

---

# 👨‍💻 Autor

Pedro Höhne Miranda 
