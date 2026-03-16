import time
import os
from colorama import init
from rich.console import Console
import time
import mysql.connector
import bcrypt

# Inicializa cores
init(strip=False)
os.system('')

console = Console()

class Banco:

    def __init__(self, conexao, console):
        self.conexao = conexao
        self.cursor = conexao.cursor()
        self.console = console
        self.login = False
        self.usuario_atual = ""

#--------------------------------------------------------------------------------------    

    def obter_saldo(self,id):
        self.cursor.execute(
        "SELECT saldo FROM Usuarios WHERE id = %s",
        (id,)
    )
        return self.cursor.fetchone()[0]
    
    #--------------------------------------------------------------------------------------    
    
    def criar_conta(self, nome, cpf, senha):
        query = "INSERT INTO Usuarios (nome, cpf, senha) VALUES(%s, %s, %s)"
        senha_bytes = senha.encode()
        hash_senha = bcrypt.hashpw(senha_bytes, bcrypt.gensalt())
        self.cursor.execute(query, (nome, cpf, hash_senha))
        self.conexao.commit()

#--------------------------------------------------------------------------------------    

    def mostrar_conta(self, id):
        query = "SELECT * FROM Usuarios WHERE id = %s"
        self.cursor.execute(query, (id,))
        resultado = self.cursor.fetchone()
        id, nome, saldo, cpf, senha, criado_em = resultado

        print("\n" + "="*30)
        print(f"📌 DETALHES DA CONTA (ID: {id})")
        print("-"*30)
        print(f"👤 Nome:  {nome.title()}")
        print(f"🆔 CPF:   {cpf[:3]}.***.***-{cpf[-2:]}")
        print(f"💰 Saldo: R$ {saldo:,.2f}")
        print(f"⏱️ Conta criada em: {criado_em}")
        print("="*30 + "\n")

#--------------------------------------------------------------------------------------    

    def obter_extrato(self, meu_id):
    # Passamos o ID duas vezes para o OR
        query = """
        SELECT origem, destino, valor, tipo, data 
        FROM transacoes 
        WHERE origem = %s OR destino = %s 
        ORDER BY data DESC 
        LIMIT 8
    """
        self.cursor.execute(query, (meu_id, meu_id))
        extrato = self.cursor.fetchall()

        if not extrato:
            print("\n--- Nenhuma movimentação encontrada ---")
            return

        self.console.print(f"\n[bold]=== EXTRATO (Últimas {len(extrato)} transações) ===[/]")
    
        for registro in extrato:
            origem, destino, valor, tipo, data = registro
            print("-" * 40)

            # Lógica para TRANSFERÊNCIAS (Tem origem e destino)
            if tipo not in ["Depósito", "Saque"]:
                # Buscamos os nomes de forma segura
                self.cursor.execute("SELECT id, nome FROM Usuarios WHERE id IN (%s, %s)", (origem, destino))
                nomes_dict = dict(self.cursor.fetchall()) # Cria um dicionário {id: nome}
            
                n_origem = nomes_dict.get(origem, "Desconhecido")
                n_destino = nomes_dict.get(destino, "Desconhecido")

                if meu_id == origem:
                    self.console.print(f"[red]SAÍDA:[/] Para {n_destino} (ID: {destino})")
                    cor_valor = "red"
                else:
                    self.console.print(f"[green]ENTRADA:[/] De {n_origem} (ID: {origem})")
                    cor_valor = "green"
        
            # Lógica para SAQUE/DEPÓSITO
            else:
                if tipo == "Saque":
                    self.console.print(f"[red]SAQUE EFETUADO[/]")
                    cor_valor = "red"
                else:
                    self.console.print(f"[green]DEPÓSITO RECEBIDO[/]")
                    cor_valor = "green"

            self.console.print(f"VALOR: [{cor_valor}]R$ {valor:,.2f}[/]")
            self.console.print(f"DATA:  [grey50]{data.strftime('%d/%m/%Y %H:%M')}[/]")
    
    print("-" * 40)

#--------------------------------------------------------------------------------------    

    def depositar(self, id, quantia):

        if quantia <= 0:
            self.console.print("[red]Você não pode adicionar um valor negativo.[/]")
            time.sleep(2)

        else:
            query = "UPDATE Usuarios SET saldo = saldo + %s WHERE id = %s"
            self.cursor.execute(query, (quantia, id))
            self.console.print(f"[green]R$ {quantia:,.2f} depositado com sucesso.[/]")
            time.sleep(2)
            self.cursor.execute("INSERT INTO Transacoes (origem, valor, tipo) VALUES (%s, %s, %s)", (self.usuario_atual, quantia, "Depósito"))
            self.conexao.commit()
            
#--------------------------------------------------------------------------------------    

    def sacar(self, id, quantia):
        saldo = self.obter_saldo(id)

        if saldo < quantia:

            self.console.print(
                f"[red]Saldo insuficiente.[/] Saldo atual: R$ {saldo:,.2f}"
            )
            time.sleep(2)

        else:

            query = "UPDATE Usuarios SET saldo = saldo - %s WHERE id = %s"
            self.cursor.execute(query, (quantia, id))
            self.console.print(f"[green]R$ {quantia:,.2f} sacado com sucesso.[/]")
            self.cursor.execute("INSERT INTO Transacoes (origem, valor, tipo) VALUES (%s, %s, %s)", (self.usuario_atual, quantia, "Saque"))
            self.conexao.commit()
            time.sleep(2)

#--------------------------------------------------------------------------------------    

    def transferir(self, origem, destino, quantia):

        try:

            self.conexao.rollback()
            self.conexao.start_transaction()
            
            valor1 = self.obter_saldo(origem)

            query2 = "SELECT * FROM Usuarios WHERE id = %s"
            self.cursor.execute(query2, (destino,))
            destinatario = self.cursor.fetchone()

            if destinatario is None:

                self.console.print("[red]Usuário destino não existe.[/]")
                self.conexao.rollback()
                time.sleep(2)
                return

            elif valor1 < quantia:

                self.console.print(
                    f"[red]Saldo insuficiente.[/] Saldo: R$ {valor1:,.2f}"
                )
                self.conexao.rollback()
                time.sleep(2)
                return

            else:

                self.cursor.execute(
                    "UPDATE Usuarios SET saldo = saldo - %s WHERE id = %s",
                    (quantia, origem)
                )

                self.cursor.execute(
                    "UPDATE Usuarios SET saldo = saldo + %s WHERE id = %s",
                    (quantia, destino)
                )

                self.cursor.execute("INSERT INTO Transacoes (origem, destino, valor, tipo) VALUES (%s, %s, %s, %s)", (self.usuario_atual, destino, quantia, "Transação"))
                self.conexao.commit()

                self.console.print(
                    f"[green]Transferência concluída.[/]\n"
                    f"ID origem:{origem}\n"
                    f"ID destino:{destino}\n"
                    f"Valor: R$ {quantia:,.2f}"
                )

                time.sleep(2)

        except Exception as erro:

            self.conexao.rollback()
            self.console.print(f"[red]Erro:[/] {erro}")
            
#--------------------------------------------------------------------------------------                

    def fazer_login(self, cpf, senha):

        query = "SELECT TRIM(senha) FROM Usuarios WHERE TRIM(cpf) = %s"
        self.cursor.execute(query, (cpf.strip(),))
        try:
            resultado = self.cursor.fetchone()[0]
        except TypeError as error:
            console.print("[red]CPF[/] não foi encontrado.")
        else:
        
            hash_banco = resultado.encode()
        
            if bcrypt.checkpw(senha.encode(), hash_banco):

                self.console.print("[green]Acesso liberado.[/]")
                time.sleep(1.5)

                query = "SELECT id FROM Usuarios WHERE cpf = %s"
                self.cursor.execute(query, (cpf,))

                self.usuario_atual = self.cursor.fetchone()[0]
                self.login = True

            else:

                self.console.print("[red]Acesso Negado.[/] CPF ou senha incorretos.")
                time.sleep(1.5)