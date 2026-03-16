from flask import Flask, render_template, request, redirect, url_for
from banco import Banco
import mysql.connector

app = Flask(__name__)

def get_db():
    return mysql.connector.connect(
        host="127.0.0.1", user="root", password="123456", database="banco_balckzo"
    )

@app.route('/')
def index():
    # Página inicial com botões "Login" e "Criar Conta"
    return render_template('index.html')

@app.route('/cadastrar', methods=['GET', 'POST'])
def cadastrar():
    if request.method == 'POST':
        nome = request.form.get('nome')
        cpf = request.form.get('cpf')
        senha = request.form.get('senha')
        
        banco = Banco(get_db(), None)
        sucesso, msg = banco.criar_conta(nome, cpf, senha)
        
        if sucesso:
            return redirect(url_for('login')) # Manda pro login se criar
        return f"Erro: {msg}"
    return render_template('cadastro.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        cpf = request.form.get('cpf')
        senha = request.form.get('senha')
        
        banco = Banco(get_db(), None)
        banco.fazer_login(cpf, senha)
        
        if banco.login:
            # Se logou, leva o ID do usuário para a URL do painel
            return redirect(url_for('painel', user_id=banco.usuario_atual))
    return render_template('login.html')

@app.route('/painel/<int:user_id>')
def painel(user_id):
    banco = Banco(get_db(), None)
    saldo = banco.obter_saldo(user_id)
    # Aqui você desenha os botões de Sacar, Depositar, etc.
    return render_template('painel.html', user_id=user_id, saldo=saldo)

if __name__ == '__main__':
    app.run(debug=True)