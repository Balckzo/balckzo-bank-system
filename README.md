# 🏦 Balckzo Bank System - ## Version v1.0 - Initial release

A simple **banking system built with Python and MySQL**, running entirely in the terminal.

This project simulates basic operations of a real bank, including account creation, authentication, financial transactions, and transaction history.

It was developed as a **learning project focused on backend development, database integration, and code organization.**

---

# 🚀 Features

✔ Account creation
✔ Login using CPF and password
✔ Passwords securely stored using **bcrypt hashing**
✔ Deposit money
✔ Withdraw money
✔ Transfer money between accounts
✔ View account details
✔ Transaction history (latest operations)
✔ All transactions recorded in the database

---

# 🧠 Technologies Used

* Python
* MySQL
* mysql-connector-python
* bcrypt
* Rich
* Colorama

---

# 📂 Project Structure

```
balckzo-bank-system/

main.py          # CLI interface and application flow
banco.py         # Banking system logic

database.sql     # Database schema
requirements.txt # Project dependencies
README.md
```

---

# 🗄 Database Structure

The system uses two main tables.

## Users

Stores account information.

Fields:

* id
* name
* cpf
* password (bcrypt hash)
* balance
* created_at

---

## Transactions

Stores all financial operations.

Fields:

* id
* origin
* destination
* value
* type
* date

Transaction types:

* Deposit
* Withdraw
* Transfer

---

# 📊 Transaction History

The system displays the **8 most recent transactions** related to the account.

Each record includes:

* sender name
* receiver name
* transaction value
* transaction type
* date and time

---

# ⚙ How to Run the Project

### 1️⃣ Clone the repository

```
git clone https://github.com/YOUR_USERNAME/balckzo-bank-system.git
```

### 2️⃣ Install dependencies

```
pip install -r requirements.txt
```

### 3️⃣ Create the database

Run the script:

```
database.sql
```

inside MySQL.

### 4️⃣ Run the application

```
python main.py
```

---

# 🎯 Project Goal

This project was created to practice:

* Python programming
* Database integration
* Password security (hashing)
* Backend application structure
* Transaction logic
* Database transactions

---

# ⚠ Disclaimer

This project is **for educational purposes only** and should not be used as a real banking system.

---

# 👨‍💻 Author

Pedro Höhne Miranda
