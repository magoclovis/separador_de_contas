# funcao para pegar a data e hora do SO
import datetime

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

def main():

    # vetor de pessoas, inicialmente com 0
    pessoas = {}
    
    # menu
    while True:
        print("\nEscolha uma opção:")
        print("1. Adicionar pessoa")
        print("2. Adicionar transação")
        print("3. Adicionar saldo")
        print("4. Remover pessoa")
        print("5. Calcular saldos e salvar")
        print("6. Sair")
        
        opcao = int(input("Opção: "))
        
        if opcao == 1:
            nome = input("\nDigite o nome da pessoa: ")
            pessoas[nome] = Pessoa(nome)
            print(f"{nome} foi adicionado(a) à lista de pessoas.")
        
        elif opcao == 2:
            if pessoas:
                print("\nEscolha uma pessoa para quem foi a transação:")
                for idx, pessoa in enumerate(pessoas.keys(), start=1):
                    print(f"{idx}. {pessoa}")
                para_idx = int(input("Escolha o número da pessoa: "))
                
                print("\nEscolha uma pessoa que fez a transação:")
                for idx, pessoa in enumerate(pessoas.keys(), start=1):
                    print(f"{idx}. {pessoa}")
                de_idx = int(input("Escolha o número da pessoa: "))
                
                if de_idx == para_idx:
                    print("Não é possível fazer uma transação de si mesmo.")
                else:
                    valor = float(input("Digite o valor da transação: "))
                    
                    pessoas_list = list(pessoas.keys())
                    de = pessoas_list[de_idx - 1]
                    para = pessoas_list[para_idx - 1]
                    
                    pessoas[de].adicionar_transacao(pessoas[para], -valor)
                    pessoas[para].adicionar_transacao(pessoas[de], valor)
                    print("Transação adicionada com sucesso!")
            else:
                print("Lista de pessoas vazia. Adicione pessoas primeiro.")
        
        elif opcao == 3:
            if pessoas:
                print("\nEscolha uma pessoa para adicionar saldo:")
                for idx, pessoa in enumerate(pessoas.keys(), start=1):
                    print(f"{idx}. {pessoa}")
                pessoa_idx = int(input("Escolha o número da pessoa: "))
                
                saldo = float(input("Digite o valor do saldo a ser adicionado: "))
                pessoa = list(pessoas.keys())[pessoa_idx - 1]
                pessoas[pessoa].adicionar_saldo(saldo)
                print(f"Saldo de R${saldo:.2f} adicionado para {pessoa}.")
            else:
                print("Lista de pessoas vazia. Adicione pessoas primeiro.")
        
        elif opcao == 4:
            if pessoas:
                print("\nEscolha uma pessoa para remover:")
                for idx, pessoa in enumerate(pessoas.keys(), start=1):
                    print(f"{idx}. {pessoa}")
                pessoa_idx = int(input("Escolha o número da pessoa: "))
                
                pessoa = list(pessoas.keys())[pessoa_idx - 1]
                del pessoas[pessoa]
                print(f"{pessoa} foi removido(a) da lista de pessoas.")
            else:
                print("Lista de pessoas vazia. Nada para remover.")
        
        elif opcao == 5:
            if pessoas:
                salvar_saldos(pessoas)
                print("Saldos calculados e salvos com sucesso.")
            else:
                print("Lista de pessoas vazia. Nada para calcular e salvar.")
        
        elif opcao == 6:
            break
        
        else:
            print("Opção inválida. Escolha uma opção válida.")

if __name__ == "__main__":
    main()
