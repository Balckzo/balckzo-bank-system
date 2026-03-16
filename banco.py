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
        dados = self.cursor.fetchone()
        id_u, nome, saldo, cpf, senha ,criado_em = dados
    # Retornamos um DICIONÁRIO para o main.py saber o que imprimir
        return {
            "id": id_u,
            "nome": nome.title(),
            "saldo": saldo,
            "cpf": f"{cpf[:3]}.***.***-{cpf[-2:]}",
            "criado_em": criado_em
    }

#--------------------------------------------------------------------------------------    

    def obter_extrato(self, meu_id):
        query = """
            SELECT origem, destino, valor, tipo, data 
            FROM transacoes 
            WHERE origem = %s OR destino = %s 
            ORDER BY data DESC LIMIT 8
        """
        self.cursor.execute(query, (meu_id, meu_id))
        extrato_bruto = self.cursor.fetchall()
        
        if not extrato_bruto:
            return [] # Retorna lista vazia se não tiver nada

        extrato_limpo = []

        for registro in extrato_bruto:
            origem, destino, valor, tipo, data = registro
            
            # Montamos um "pacotinho" de dados para cada linha
            item = {
                "tipo": tipo,
                "valor": valor,
                "data": data.strftime('%d/%m/%Y %H:%M'),
                "detalhe": "" 
            }

            # Lógica de quem é quem (sem print!)
            if tipo not in ["Depósito", "Saque"]:
                self.cursor.execute("SELECT id, nome FROM Usuarios WHERE id IN (%s, %s)", (origem, destino))
                nomes = dict(self.cursor.fetchall())
                n_origem = nomes.get(origem, "Desconhecido")
                n_destino = nomes.get(destino, "Desconhecido")

                if meu_id == origem:
                    item["direcao"] = "SAÍDA"
                    item["detalhe"] = f"Para: {n_destino} (ID: {destino})"
                else:
                    item["direcao"] = "ENTRADA"
                    item["detalhe"] = f"De: {n_origem} (ID: {origem})"
            else:
                item["direcao"] = "SAÍDA" if tipo == "Saque" else "ENTRADA"
                item["detalhe"] = f"{tipo.upper()} realizado"

            extrato_limpo.append(item)

        return extrato_limpo
#--------------------------------------------------------------------------------------    

    def depositar(self, id, quantia):

        if quantia <= 0:
            return False, "Você não pode adicionar uma quantia negativa ou igual a 0."

        else:
            query = "UPDATE Usuarios SET saldo = saldo + %s WHERE id = %s"
            self.cursor.execute(query, (quantia, id))
            self.cursor.execute("INSERT INTO Transacoes (origem, valor, tipo) VALUES (%s, %s, %s)", (self.usuario_atual, quantia, "Depósito"))
            self.conexao.commit()
            return True, f"R$ {quantia:,.2f} depositado com sucesso."
            
#--------------------------------------------------------------------------------------    

    def sacar(self, id, quantia):
        saldo = self.obter_saldo(id)

        if saldo < quantia:
                return False, f"Saldo insuficiente. Saldo atual: R$ {saldo:,.2f}"
            
        else:

            query = "UPDATE Usuarios SET saldo = saldo - %s WHERE id = %s"
            self.cursor.execute(query, (quantia, id))
            self.cursor.execute("INSERT INTO Transacoes (origem, valor, tipo) VALUES (%s, %s, %s)", (self.usuario_atual, quantia, "Saque"))
            self.conexao.commit()
            return True, f"Saque de R$ {quantia:,.2f} realizado com sucesso!"

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
                self.conexao.rollback()
                return False, "Usuário destino não existe."

            elif valor1 < quantia:
                self.conexao.rollback()
                return False, f"Saldo insuficiente. Saldo: R$ {valor1:,.2f}"

            else:

                self.cursor.execute(
                    "UPDATE Usuarios SET saldo = saldo - %s WHERE id = %s",
                    (quantia, origem)
                )

                self.cursor.execute(
                    "UPDATE Usuarios SET saldo = saldo + %s WHERE id = %s",
                    (quantia, destino)
                )

                self.cursor.execute("INSERT INTO Transacoes (origem, destino, valor, tipo) VALUES (%s, %s, %s, %s)", (origem, destino, quantia, "Transação"))
                self.conexao.commit()

                return True, f"Transferência concluída.\n ID origem:{origem}\nID destino:{destino}\nValor: R$ {quantia:,.2f}"
            
        except Exception as erro:

            self.conexao.rollback()
            return False, f"Erro: {erro}"
            
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