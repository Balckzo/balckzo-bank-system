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

        deposito_quebra = False

        while deposito_quebra != True:

            try:
                valor = int(input("Insira o valor que será depositado:"))

            except ValueError:

                console.print("Você colocou alguma [red]letra[/].")
                time.sleep(1)

            else:

                banco.depositar(banco.usuario_atual, valor)

                deposito_quebra = True
                break

    if decisao == "2":

        saque_quebra = False

        while saque_quebra != True:

            try:

                valor = int(input("Insira o valor que será sacado:"))

            except ValueError:

                console.print("Você colocou alguma [red]letra[/].")
                time.sleep(1)

            else:

                banco.sacar(banco.usuario_atual, valor)

                saque_quebra = True
                break

    if decisao == "3":

        trans_quebra = False

        while trans_quebra != True:

            id = console.input("Insira o ID destinatário:")

            if any(char.isalpha() for char in id):

                console.print("Você colocou alguma [red]letra[/].")
                time.sleep(1)

            else:

                idint = int(id)

                while True:

                    try:

                        valor = int(input("Insira o valor que será transferido:"))

                    except ValueError:

                        console.print("Você colocou alguma [red]letra[/].")
                        time.sleep(1)

                    else:

                        banco.transferir(banco.usuario_atual, idint, valor)

                        trans_quebra = True
                        break

    if decisao == "4":

        mostrar_quebra = False

        while mostrar_quebra != True:

            banco.mostrar_conta(banco.usuario_atual)

            mostrar_quebra = True

            console.input("Aperte enter para voltar:")
            
    if decisao == "5":
        banco.obter_extrato(banco.usuario_atual)
        input("\nPressione Enter para continuar...")