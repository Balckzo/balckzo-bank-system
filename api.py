from flask import Flask, render_template, request, redirect, url_for, session, flash
from banco import Banco
import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

def get_db():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASS"),
        database=os.getenv("DB_NAME")
    )
    
os.getenv("FLASK_KEY") = "Balckzo"

# Rota principal (Home)
@app.route('/')
def index():
    # Isso vai procurar o arquivo index.html dentro da pasta /templates
    return render_template("index.html")

 #--------------------------------------------------------

@app.route('/cadastro', methods=["POST", "GET"])
def cadastro():
    if request.method == "POST":
        conexao = get_db()
        banco = Banco(conexao, None)
        
        nome = request.form.get("nome")
        cpf = request.form.get("cpf")
        senha = request.form.get("senha")
        
        sucesso, mensagem = banco.criar_conta(nome, cpf, senha)
        
        if sucesso:
            return redirect(url_for("login"))
        else:
            conexao.close()
            flash(f"Erro: {mensagem}", "danger")
    
    return render_template("cadastro.html")
 
 #--------------------------------------------------------
 
@app.route('/login', methods = ["POST", "GET"])
def login():
    if request.method == "POST":
            cpf = request.form.get("cpf")
            senha = request.form.get("senha")
            conexao = get_db()
            cursor = conexao.cursor()
            banco = Banco(conexao, None)
            
            
            sucesso, mensagem = banco.fazer_login(cpf, senha)
            
            if sucesso:
                cursor.execute("SELECT id FROM Usuarios WHERE cpf = %s", (cpf,))
                id_atual = cursor.fetchone()
                session['usuario_id'] = id_atual[0]
                conexao.close()
                return redirect(url_for("painel"))
            else:
                conexao.close()
                flash(f"Erro: {mensagem}", "danger")
            
    return render_template("login.html")

@app.route('/painel')
def painel():
    # 1. Verifica se tem alguém logado
    if 'usuario_id' not in session:
        return redirect(url_for('login'))

    # 2. Busca os dados desse usuário para o template não dar erro
    conexao = get_db()
    cursor = conexao.cursor(dictionary=True)
    cursor.execute("SELECT id, nome, cpf, saldo, criado_em FROM Usuarios WHERE id = %s", (session['usuario_id'],))
    dados = cursor.fetchone()
    conexao.close()

    return render_template("painel.html", usuario=dados)

@app.route('/depositar', methods=["POST", "GET"])
def depositar():
    conexao = get_db()
    banco = Banco(conexao, None)
    if 'usuario_id' not in session:
        return redirect(url_for('login'))
    
    if request.method == "POST":
        valor = float(request.form.get("valor"))
        id_atual = session['usuario_id']
        sucesso, mensagem = banco.depositar(id_atual, valor)
        
        if sucesso:
            conexao.commit()
            conexao.close()
            flash(f"Sucesso! Depósito de R$ {valor:.2f} processado.", "success")
            return redirect(url_for("painel"))
        else:
            conexao.close()
            flash(f"Erro: {mensagem}", "danger")
            return redirect(url_for("painel"))

    
    return render_template("depositar.html")
@app.route('/sacar', methods= {"POST","GET"})
def sacar():
    
    conexao = get_db()
    banco = Banco(conexao, None)
    
    if 'usuario_id' not in session:
        return redirect(url_for('login'))
    
    if request.method == "POST":
        valor = float(request.form.get("valor"))
        id_atual = session['usuario_id']
        sucesso, mensagem = banco.sacar(id_atual, valor)
        
        if sucesso:
            conexao.commit()
            conexao.close()
            flash(f"Sucesso! Saque de R$ {valor:.2f} processado.", "success")
            return redirect(url_for("painel"))
        
        else:
            conexao.close()
            flash(f"Erro: {mensagem}", "danger")
            return redirect(url_for('painel'))
    
    return render_template("sacar.html")
    
@app.route('/transferir', methods= ["POST", "GET"])
def transferir():
    conexao = get_db()
    banco = Banco(conexao, None)
    cursor = conexao.cursor()
    
    if 'usuario_id' not in session:
        return redirect(url_for('login'))
    
    if request.method == "POST":
        id_atual = session['usuario_id']
        id_destino = request.form.get("id_destino")
        valor = float(request.form.get("valor"))
        
        sucesso,mensagem = banco.transferir(id_atual, id_destino, valor)
        
        if sucesso:
            cursor.execute("SELECT nome FROM Usuarios WHERE id = %s", (id_destino,))
            nome_destino = cursor.fetchone()[0]
            conexao.commit()
            conexao.close()
            flash(f"Sucesso! Transferência feita para {nome_destino} de R$ {valor:.2f} processado.", "success")
            return redirect(url_for('painel'))
        
        else:
            conexao.close()
            flash(f"Erro: {mensagem}", "danger")
            return redirect(url_for('painel'))
    
    return render_template("transferir.html")
    
@app.route('/extrato', methods= ["GET", "POST"])
def extrato():
    conexao = get_db()
    banco = Banco(conexao, None)
    
    if 'usuario_id' not in session:
        return redirect(url_for('login'))
    
    id_atual = session['usuario_id']
    extrato = banco.obter_extrato(id_atual)
    conexao.close()
    return render_template("extrato.html", transacoes= extrato)   

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
    
    

