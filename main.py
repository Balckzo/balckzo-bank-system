import os
from colorama import init
from rich.console import Console
import time
import mysql.connector
from banco import Banco

decisao = ""

try:

    conexao = mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="123456",
        database="banco_balckzo",
        connection_timeout=5
    )

    print("Conectou!")

except mysql.connector.Error as erro:
    print("Erro:", erro)

# Inicializa cores
init(strip=False)
os.system('')

console = Console()

banco = Banco(conexao, console)

while banco.login != True:

    console.print("[cyan]Banco[/] - [magenta]Balckzo®[/]")

    login_criar = console.input("""
1 - Criar Conta\n

2 - Fazer login\n

Escolha uma das opções acima:""")

    if login_criar == "1":

        criar_quebra = False

        while criar_quebra != True:

            nome = console.input("Insira aqui seu nome, (Máximo de 50 caracteres):")

            if any(char.isdigit() for char in nome):
                print("Você digitou algum número.")
                time.sleep(1)
                continue

            elif len(nome) > 50:
                print("Máximo de 50 digitos.")
                time.sleep(1)
                continue

            else:

                while True:

                    cpf = console.input("Digite aqui seu cpf, (Exatos 11 digitos):")

                    if any(char.isalpha() for char in cpf):
                        print("Você colocou alguma letra.")
                        time.sleep(1)

                    elif len(cpf) != 11:
                        print("Deve ter 11 dígitos.")
                        time.sleep(1)

                    else:

                        while True:

                            senha = console.input("Insira sua nova senha: ")

                            if len(senha) < 8:
                                print("Sua senha deve ter 8 ou mais caracteres.")
                                continue

                            else:

                                banco.criar_conta(nome, cpf, senha)

                                print(f"Conta criada com sucesso! ID: {banco.cursor.lastrowid}")

                                time.sleep(4)

                                criar_quebra = True
                                break

                    break

    elif login_criar == "2":

        cpf = console.input("[bright_cyan]CPF[/]: ")

        if any(char.isalpha() for char in cpf):
            print("Você colocou alguma letra.")
            time.sleep(1)
            continue

        elif len(cpf) != 11:
            print("Deve ter 11 dígitos.")
            time.sleep(1)
            continue

        senha = console.input("[bright_cyan]Senha[/]: ")

        banco.fazer_login(cpf, senha)

while decisao != "7":

    decisao = console.input("""
Bem vindo ao [cyan]Banco[/] - [magenta]Balckzo®[/]

1 - Depositar
2 - Sacar
3 - Transferência
4 - Mostrar Conta
5- - Mostrar Extrato
6 - Encerrar

Selecione:""")

    if decisao == "6":

        console.print("Encerrando o programa, obrigado por utilizar o [cyan]Banco[/] - [magenta]Balckzo®[/].")
        time.sleep(2)

        decisao = "7"

    if decisao == "1":
        try:
            valor_deposito = float(console.input("Valor do saque: R$"))
            
            sucesso, mensagem = banco.depositar(banco.usuario_atual, valor_deposito)
            
            if sucesso:
                    console.print(f"[green]✅ {mensagem}[/]")
            else:
                console.print(f"[bold red]❌ FALHA NA OPERAÇÃO:[/] {mensagem}")
                
        except ValueError:
            console.print("[red]Entrada inválida. Use apenas números.[/]")
    
        time.sleep(2)
        

    if decisao == "2":
        try:
            valor_saque = float(console.input("Valor do saque: R$"))
            
            sucesso, mensagem = banco.sacar(banco.usuario_atual, valor_saque)
            
            if sucesso:
                    console.print(f"[green]✅ {mensagem}[/]")
            else:
                console.print(f"[bold red]❌ FALHA NA OPERAÇÃO:[/] {mensagem}")
                
        except ValueError:
            console.print("[red]Entrada inválida. Use apenas números.[/]")
    
        time.sleep(2)

    if decisao == "3":

        try:
            id_dest = int(console.input("ID do destinatário: "))
            valor_trans = float(console.input("Valor da transferência: R$"))
        
            # Chama a função e recebe a "tupla" (True/False, Mensagem)
            sucesso, mensagem = banco.transferir(banco.usuario_atual, id_dest, valor_trans)
        
            if sucesso:
                console.print(f"[green]✅ {mensagem}[/]")
            else:
                console.print(f"[bold red]❌ FALHA NA OPERAÇÃO:[/] {mensagem}")
            
        except ValueError:
            console.print("[red]Entrada inválida. Use apenas números.[/]")
    
        time.sleep(2)

    if decisao == "4":

        dados = banco.mostrar_conta(banco.usuario_atual)

        if dados:
            print("\n" + "="*30)
            console.print(f"📌 [bold]DETALHES DA CONTA (ID: {dados['id']})[/]")
            print("-" * 30)
            print(f"👤 Nome:  {dados['nome']}")
            print(f"🆔 CPF:   {dados['cpf']}")
            console.print(f"💰 Saldo: [green]R$ {dados['saldo']:,.2f}[/]")
            print(f"⏱️ Criada em: {dados['criado_em']}")
            print("="*30 + "\n")

            console.input("Aperte enter para voltar:")
            
    if decisao == "5":
        movimentacoes = banco.obter_extrato(banco.usuario_atual)

        if not movimentacoes:
            console.print("\n[yellow]⚠ Nenhuma movimentação encontrada.[/]")
        else:
            console.print(f"\n[bold magenta]=== EXTRATO RECENTE ===[/]")
            
            for m in movimentacoes:
                # A cor depende da direção que o banco calculou
                cor = "red" if m["direcao"] == "SAÍDA" else "green"
                
                print("-" * 40)
                console.print(f"[{cor}][{m['direcao']}][/] {m['detalhe']}")
                console.print(f"VALOR: [bold {cor}]R$ {m['valor']:,.2f}[/]")
                console.print(f"DATA:  [grey50]{m['data']}[/]")
            
            print("-" * 40)
        
        console.input("\n[cyan]Pressione ENTER para voltar...[/]")