🏦 Balckzo® Bank System - v2.0.0 ⚡
"Nasty, fast and secure." > The new standard for digital banking with Cyberpunk aesthetics, Flask engine, and MySQL persistence.

Balckzo Bank has evolved. What was once a terminal script is now a full-featured Web platform, focused on high-level security and an immersive user interface.

💎 What's New in v2.0.0? (The Rebirth)
🎨 Cyberpunk Web Interface: Minimalist neon aesthetics with real-time visual feedback using Flask templates.

🌐 Web Architecture: Full migration from CLI to Flask (Web Framework).

🔐 Ironclad Security: Password hashing using Bcrypt (Salt + Hash) and secure session management to protect user data.

📊 Smart Statement (Extrato): Detailed transaction history with Flow logic (Inbound/Outbound) and recipient identification.

💸 Atomic Transactions: Deposits, Withdrawals, and Transfers processed with database integrity (Rollback/Commit logic).

🛠️ Tech Stack
Backend: Python 3 + Flask

Database: MySQL (Relational)

Security: Bcrypt (Password Hashing)

Frontend: HTML5 / CSS3 (Custom Cyberpunk Design)

Integration: MySQL Connector

📂 Project Structure
Plaintext
balckzo-bank-system/
├── api.py            # Flask Server & Web Routes
├── banco.py          # The Core: Business Logic & SQL Integration
├── templates/        # HTML Interfaces (Login, Register, Dashboard, etc.)
├── static/           # Styles & Assets
├── database.sql      # Database Schema
├── requirements.txt  # Project Dependencies
└── .env              # Sensitive Variables (Hidden/Protected)
🗄️ Data Architecture
👤 Users (Usuarios)
id, name, cpf, password (Bcrypt Hash), balance, created_at.

💸 Transactions (transacoes)
Complete logs of Origin, Destination, Value, Type, and Timestamp.

📊 Transaction History
The system displays a refined history of the 8 most recent transactions. Each record includes:

Direction: Visual indicator of INBOUND or OUTBOUND flow.

Details: Contextual information (e.g., "From: User X" or "To: User Y").

Type: Clear identification of the operation (Deposit, Withdraw, or Transfer).

Timestamp: Formatted date and time of the occurrence.

⚙️ How to Run (Local Deploy)
1️⃣ Clone the repository
Bash
git clone https://github.com/YOUR_USERNAME/balckzo-bank-system.git
2️⃣ Install dependencies
Bash
pip install -r requirements.txt
pip install python-dotenv
3️⃣ Set up your Vault (.env)
Create a .env file in the root folder to hide your credentials from the public repository. Add your MySQL details:

Plaintext
DB_HOST=127.0.0.1
DB_USER=root
DB_PASS=your_password
DB_NAME=banco_balckzo
FLASK_KEY=Balckzo
4️⃣ Create the database
Run the database.sql script inside your MySQL environment to set up the required tables.

5️⃣ Fire it up
Bash
python api.py
Access the system at: http://localhost:5000

🎯 Project Goals
v2.0.0 marks the transition to Fullstack Web Development, applying advanced concepts:

Prevention of SQL Injection.

User Session Management (Login/Logout persistence).

Password Security using industry-standard Hashing.

Backend application structure and Transaction logic.

👨‍💻 Author
Pedro Höhne Miranda

⚠ Disclaimer
This project is strictly for educational purposes. It simulates banking operations to practice backend logic and should not be used as a real financial system.