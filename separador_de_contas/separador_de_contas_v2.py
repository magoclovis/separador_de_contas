import tkinter as tk
from tkinter import simpledialog, messagebox
import datetime
from tkinter import filedialog

class Pessoa:
    def __init__(self, nome):
        self.nome = nome
        self.transacoes = []

    def adicionar_transacao(self, pessoa, valor):
        self.transacoes.append((pessoa, valor))

    def adicionar_saldo(self, saldo):
        self.transacoes.append(("Saldo inicial", saldo))

    def calcular_saldo(self):
        saldo = sum(transacao[1] for transacao in self.transacoes)
        return saldo

def salvar_saldos(pessoas):
    data_hora_atual = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    nome_arquivo = f"saldos_{data_hora_atual}.txt"
    
    with open(nome_arquivo, "a") as arquivo:
        data_hora = datetime.datetime.now()
        arquivo.write(f"Saldos calculados em: {data_hora}\n")
        for pessoa in pessoas.values():
            saldo = pessoa.calcular_saldo()
            arquivo.write(f"{pessoa.nome}: Saldo = R${saldo:.2f}\n")
        arquivo.write("\n")

def atualizar_lista_pessoas():
    lista_pessoas_text.config(state=tk.NORMAL)
    lista_pessoas_text.delete("1.0", tk.END)
    for pessoa in pessoas.values():
        saldo = pessoa.calcular_saldo()
        lista_pessoas_text.insert(tk.END, f"{pessoa.nome}: Saldo = R${saldo:.2f}\n")
    lista_pessoas_text.config(state=tk.DISABLED)

def adicionar_pessoa():
    nome = simpledialog.askstring("Adicionar Pessoa", "Digite o nome da pessoa:")
    if nome and nome not in pessoas:
        pessoas[nome] = Pessoa(nome)
        atualizar_lista_pessoas()
        messagebox.showinfo("Sucesso", f"{nome} foi adicionado(a) à lista de pessoas.")
    elif nome in pessoas:
        messagebox.showwarning("Erro", f"{nome} já está na lista de pessoas.")
    else:
        messagebox.showwarning("Erro", "Nome inválido. Por favor, forneça um nome válido.")

def remover_pessoa():
    if not pessoas:
        messagebox.showwarning("Erro", "Não há pessoas para remover.")
        return
    
    nomes_pessoas = list(pessoas.keys())
    nome_remover = simpledialog.askstring("Remover Pessoa", "Escolha o número da pessoa para remover:\n" +
                                          "\n".join([f"{i+1}. {nome}" for i, nome in enumerate(nomes_pessoas)]))
    if nome_remover:
        try:
            indice = int(nome_remover) - 1
            nome = nomes_pessoas[indice]
            del pessoas[nome]
            atualizar_lista_pessoas()
            messagebox.showinfo("Sucesso", f"{nome} foi removido(a) da lista de pessoas.")
        except (ValueError, IndexError):
            messagebox.showwarning("Erro", "Escolha um número válido.")

def adicionar_transacao():
    if len(pessoas) < 2:
        messagebox.showwarning("Erro", "Não há pessoas suficientes para fazer transações.")
        return

    nomes_pessoas = list(pessoas.keys())
    nome_pagador = simpledialog.askstring("Adicionar Transação", "Escolha o número da pessoa que fez a transação:\n" +
                                          "\n".join([f"{i + 1}. {nome}" for i, nome in enumerate(nomes_pessoas)]))
    nome_recebedor = simpledialog.askstring("Adicionar Transação", "Escolha o número da pessoa para quem foi a transação:\n" +
                                            "\n".join([f"{i + 1}. {nome}" for i, nome in enumerate(nomes_pessoas)]))
    if nome_pagador and nome_recebedor:
        try:
            indice_pagador = int(nome_pagador) - 1
            indice_recebedor = int(nome_recebedor) - 1
            nome_pagador = nomes_pessoas[indice_pagador]
            nome_recebedor = nomes_pessoas[indice_recebedor]
            valor = simpledialog.askfloat("Adicionar Transação", f"Digite o valor de {nome_pagador} para {nome_recebedor}:")
            if valor is not None:
                pessoas[nome_pagador].adicionar_transacao(nome_recebedor, -valor)
                pessoas[nome_recebedor].adicionar_transacao(nome_pagador, valor)
                atualizar_lista_pessoas()
                messagebox.showinfo("Sucesso", f"Transação adicionada: {nome_pagador} transferiu R${valor:.2f} para {nome_recebedor}.")
        except (ValueError, IndexError):
            messagebox.showwarning("Erro", "Escolha um número válido.")

def adicionar_saldo():
    if not pessoas:
        messagebox.showwarning("Erro", "Não há pessoas para adicionar saldo.")
        return
    
    nomes_pessoas = list(pessoas.keys())
    nome_pessoa = simpledialog.askstring("Adicionar Saldo", "Escolha o número da pessoa:\n" +
                                         "\n".join([f"{i+1}. {nome}" for i, nome in enumerate(nomes_pessoas)]))
    if nome_pessoa:
        try:
            indice = int(nome_pessoa) - 1
            nome = nomes_pessoas[indice]
            saldo = simpledialog.askfloat("Adicionar Saldo", f"Digite o valor do saldo para {nome}:")
            if saldo is not None:
                pessoas[nome].adicionar_saldo(saldo)
                atualizar_lista_pessoas()
                messagebox.showinfo("Sucesso", f"Saldo adicionado para {nome}.")
        except (ValueError, IndexError):
            messagebox.showwarning("Erro", "Escolha um número válido.")

def carregar_dados():
    try:
        nome_arquivo = filedialog.askopenfilename(filetypes=[("Arquivos de Texto", "*.txt")])
        if nome_arquivo:
            with open(nome_arquivo, "r") as arquivo:
                linhas = arquivo.readlines()
                pessoas.clear()
                nome = ""
                saldo = 0.0
                for linha in linhas:
                    if "Saldos calculados em:" in linha:
                        continue
                    elif "Transações:" in linha:
                        break
                    elif "Saldo" in linha:
                        partes = linha.split(":")
                        nome = partes[0].strip()
                        saldo = float(partes[1].split("R$")[1].strip())
                        pessoas[nome] = Pessoa(nome)
                        pessoas[nome].adicionar_saldo(saldo)
                for linha in linhas:
                    if "Transações:" in linha:
                        partes = linha.split()
                        nome_pagador = partes[0]
                        nome_recebedor = partes[3]
                        valor = float(partes[5].split("R$")[1])
                        pessoas[nome_pagador].adicionar_transacao(nome_recebedor, -valor)
                        pessoas[nome_recebedor].adicionar_transacao(nome_pagador, valor)
                atualizar_lista_pessoas()
                messagebox.showinfo("Sucesso", "Dados carregados com sucesso!")
    except Exception as e:
        messagebox.showerror("Erro", f"Ocorreu um erro ao carregar os dados: {e}")


# Inicialização
pessoas = {}
root = tk.Tk()
root.title("Separador de Contas")

lista_pessoas_text = tk.Text(root, height=10, width=40)
lista_pessoas_text.config(state=tk.DISABLED)
lista_pessoas_text.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

adicionar_pessoa_button = tk.Button(root, text="Adicionar Pessoa", command=adicionar_pessoa)
adicionar_pessoa_button.grid(row=1, column=0, padx=10, pady=5)

remover_pessoa_button = tk.Button(root, text="Remover Pessoa", command=remover_pessoa)
remover_pessoa_button.grid(row=1, column=1, padx=10, pady=5)

adicionar_transacao_button = tk.Button(root, text="Adicionar Transação", command=adicionar_transacao)
adicionar_transacao_button.grid(row=2, column=0, padx=10, pady=5)

adicionar_saldo_button = tk.Button(root, text="Adicionar Saldo", command=adicionar_saldo)
adicionar_saldo_button.grid(row=2, column=1, padx=10, pady=5)

calcular_saldos_button = tk.Button(root, text="Calcular Saldos", command=lambda: [atualizar_lista_pessoas(), salvar_saldos(pessoas), messagebox.showinfo("Sucesso", "Saldos calculados e salvos.")])
calcular_saldos_button.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

carregar_dados_button = tk.Button(root, text="Carregar Dados", command=carregar_dados)
carregar_dados_button.grid(row=4, column=0, columnspan=2, padx=10, pady=5)

root.mainloop()
