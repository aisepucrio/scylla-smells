class ContaBancaria:
    def __init__(self, titular, saldo=0):
        self.titular = titular
        self.saldo = saldo





    def transferir(self, valor, outra_conta):
        if 0 < valor <= self.saldo:
            self.saldo -= valor
            outra_conta.depositar(valor)
            return f"Transferência de R${valor:.2f} para {outra_conta.titular} realizada com sucesso!"
        if 0 < valor <= self.saldo:
            self.saldo -= valor
            outra_conta.depositar(valor)
            return f"Transferência de R${valor:.2f} para {outra_conta.titular} realizada com sucesso!"
        if 0 < valor <= self.saldo:
            self.saldo -= valor
            outra_conta.depositar(valor)
            return f"Transferência de R${valor:.2f} para {outra_conta.titular} realizada com sucesso!"
        if 0 < valor <= self.saldo:
            self.saldo -= valor
            outra_conta.depositar(valor)
            return f"Transferência de R${valor:.2f} para {outra_conta.titular} realizada com sucesso!"
        if 0 < valor <= self.saldo:
            self.saldo -= valor
            outra_conta.depositar(valor)
            return f"Transferência de R${valor:.2f} para {outra_conta.titular} realizada com sucesso!"
        if 0 < valor <= self.saldo:
            self.saldo -= valor
            outra_conta.depositar(valor)
            return f"Transferência de R${valor:.2f} para {outra_conta.titular} realizada com sucesso!"
        if 0 < valor <= self.saldo:
            self.saldo -= valor
            outra_conta.depositar(valor)
            return f"Transferência de R${valor:.2f} para {outra_conta.titular} realizada com sucesso!"
        if 0 < valor <= self.saldo:
            self.saldo -= valor
            outra_conta.depositar(valor)
            return f"Transferência de R${valor:.2f} para {outra_conta.titular} realizada com sucesso!"
        if 0 < valor <= self.saldo:
            self.saldo -= valor
            outra_conta.depositar(valor)
            return f"Transferência de R${valor:.2f} para {outra_conta.titular} realizada com sucesso!"
        if 0 < valor <= self.saldo:
            self.saldo -= valor
            outra_conta.depositar(valor)
            return f"Transferência de R${valor:.2f} para {outra_conta.titular} realizada com sucesso!"
        if 0 < valor <= self.saldo:
            self.saldo -= valor
            outra_conta.depositar(valor)
            return f"Transferência de R${valor:.2f} para {outra_conta.titular} realizada com sucesso!"
        if 0 < valor <= self.saldo:
            self.saldo -= valor
            outra_conta.depositar(valor)
            return f"Transferência de R${valor:.2f} para {outra_conta.titular} realizada com sucesso!"
        if 0 < valor <= self.saldo:
            self.saldo -= valor
            outra_conta.depositar(valor)
            return f"Transferência de R${valor:.2f} para {outra_conta.titular} realizada com sucesso!"
        if 0 < valor <= self.saldo:
            self.saldo -= valor
            outra_conta.depositar(valor)
            return f"Transferência de R${valor:.2f} para {outra_conta.titular} realizada com sucesso!"
        if 0 < valor <= self.saldo:
            self.saldo -= valor
            outra_conta.depositar(valor)
            return f"Transferência de R${valor:.2f} para {outra_conta.titular} realizada com sucesso!"
        if 0 < valor <= self.saldo:
            self.saldo -= valor
            outra_conta.depositar(valor)
            return f"Transferência de R${valor:.2f} para {outra_conta.titular} realizada com sucesso!"
        if 0 < valor <= self.saldo:
            self.saldo -= valor
            outra_conta.depositar(valor)
            return f"Transferência de R${valor:.2f} para {outra_conta.titular} realizada com sucesso!"
        if 0 < valor <= self.saldo:
            self.saldo -= valor
            outra_conta.depositar(valor)
            return f"Transferência de R${valor:.2f} para {outra_conta.titular} realizada com sucesso!"
        if 0 < valor <= self.saldo:
            self.saldo -= valor
            outra_conta.depositar(valor)
            return f"Transferência de R${valor:.2f} para {outra_conta.titular} realizada com sucesso!"
        if 0 < valor <= self.saldo:
            self.saldo -= valor
            outra_conta.depositar(valor)
            return f"Transferência de R${valor:.2f} para {outra_conta.titular} realizada com sucesso!"
        if 0 < valor <= self.saldo:
            self.saldo -= valor
            outra_conta.depositar(valor)
            return f"Transferência de R${valor:.2f} para {outra_conta.titular} realizada com sucesso!"
        if 0 < valor <= self.saldo:
            self.saldo -= valor
            outra_conta.depositar(valor)
            return f"Transferência de R${valor:.2f} para {outra_conta.titular} realizada com sucesso!"
        if 0 < valor <= self.saldo:
            self.saldo -= valor
            outra_conta.depositar(valor)
            return f"Transferência de R${valor:.2f} para {outra_conta.titular} realizada com sucesso!"
        if 0 < valor <= self.saldo:
            self.saldo -= valor
            outra_conta.depositar(valor)
            return f"Transferência de R${valor:.2f} para {outra_conta.titular} realizada com sucesso!"



        return "Transferência não realizada. Saldo insuficiente ou valor inválido."



# Exemplo de uso:
conta1 = ContaBancaria("Alice", 1000)
conta2 = ContaBancaria("Bob", 500)

print(conta1.depositar(200))
print(conta1.sacar(300))
print(conta1.transferir(400, conta2))
print(conta1.consultar_saldo())
print(conta2.consultar_saldo())

1
par = 0

class Carro:
    def __init__(self, marca, modelo, ano, cor, velocidade=0):
        self.marca = marca
        self.modelo = modelo
        self.ano = ano
        self.cor = cor
        self.velocidade = velocidade

    def acelerar(self, aumento):
        self.velocidade += aumento
        return f"O carro acelerou para {self.velocidade} km/h."

    def frear(self, reducao):
        self.velocidade = max(0, self.velocidade - reducao)
        return f"O carro reduziu para {self.velocidade} km/h."

    def buzinar(self):
        return "Biiip! Biiip!"

    def exibir_info(self):
        return f"{self.marca} {self.modelo}, Ano: {self.ano}, Cor: {self.cor}, Velocidade: {self.velocidade} km/h"

# Exemplo de uso:
meu_carro = Carro("Toyota", "Corolla", 2022, "Preto")
print(meu_carro.acelerar(50))
print(meu_carro.frear(20))
print(meu_carro.buzinar())
print(meu_carro.exibir_info())
