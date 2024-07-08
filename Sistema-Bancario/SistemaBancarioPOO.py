import re
from abc import ABC, abstractclassmethod, abstractproperty
from datetime import datetime


class Cliente:
    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = []

    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)

    def adicionar_conta(self, conta):
        self.contas.append(conta)


class PessoaFisica(Cliente):
    def __init__(self, nome, data_nascimento, cpf, endereco):
        super().__init__(endereco)
        self.cpf = cpf
        self.nome = nome
        self.data_nascimento = data_nascimento
        


class Conta:
    def __init__(self, numero, cliente):
        self._saldo = 0
        self._numero = numero
        self._agencia = "0001"
        self._cliente = cliente
        self._historico = Historico()

    @property
    def saldo(self):
        return self._saldo

    @property
    def numero(self):
        return self._numero

    @property
    def agencia(self):
        return self._agencia

    @property
    def cliente(self):
        return self._cliente

    @property
    def historico(self):
        return self._historico

    def sacar(self, valor):
        saldo = self.saldo

        if valor > saldo:
            print("Operação falhou! Você não tem saldo suficiente.")

        elif valor > 0:
            self._saldo -= valor
            print("Saque realizado com sucesso!")
            return True

        else:
            print("Operação falhou! O valor informado é inválido.")

        return False

    @classmethod
    def nova_conta(cls, cliente, numero):
        return cls(numero, cliente)

    
    def depositar(self, valor):
        if valor > 0:
            self._saldo += valor
            print("Depósito realizado com sucesso!")
        else:
            print("Operação falhou! O valor informado é inválido.")
            return False

        return True


class ContaCorrente(Conta):
    def __init__(self, numero, cliente, limite=500, limite_saques=3):
        super().__init__(numero, cliente)
        self._limite = limite
        self._limite_saques = limite_saques

    def sacar(self, valor):
        numeroSaques = len(
            [transacao for transacao in self.historico.transacoes if transacao["tipo"] == Saque.__name__]
        )

        if valor > self._limite:
            print("Operação falhou! O valor do saque excede o limite.")
        elif numeroSaques >= self._limite_saques:
           print("Operação falhou! Número máximo de saques excedido.")
        else:
            return super().sacar(valor)


        return False

    def __str__(self):
        return f"""
                Agência:          {self.agencia}
                Número da conta:  {self.numero}
                Nome do Cliente:  {self.cliente.nome}
            """


class Historico:
    def __init__(self):
        self._transacoes = []

    @property
    def transacoes(self):
        return self._transacoes

    def adicionar_transacao(self, transacao):
        self._transacoes.append(
            {
                "tipo": transacao.__class__.__name__,
                "valor": transacao.valor,
                "data": str(datetime.now().strftime("%d-%m-%Y")),
            }
        )


class Transacao(ABC):
    @property
    @abstractproperty
    def valor(self):
        pass

    @abstractclassmethod
    def registrar(self, conta):
        pass


class Saque(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        sucesso_transacao = conta.sacar(self.valor)

        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)


class Deposito(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        sucesso_transacao = conta.depositar(self.valor)

        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)


def menu():
    menu = """
    ==================== SISTEMA BANCÁRIO ====================
    |                    *[d]   Depositar                    |
    |                    *[s]   Sacar                        |
    |                    *[e]   Extrato                      |
    |                    *[nvc] Nova Conta                   |
    |                    *[lc]  Listar Contas                |
    |                    *[nvu] Novo Usuário                 |
    |                    *[q]   Sair                         |
    ==========================================================
    => """

    return input(menu)

def recuperarContaCliente(cliente):
    if not cliente.contas:
        print("Cliente não possui conta!")
        return

    nConta = int(input(f"Digite o número da conta que deseja acessar (de 1 a {len(cliente.contas)}): "))

    if nConta < 1 or nConta > len(cliente.contas):
        print("Cliente não possui esse número de conta!")               
        return
    return cliente.contas[nConta - 1]

def filtrarCliente(cpf, clientes):
    filtragem = [cliente for cliente in clientes if cliente.cpf == cpf]
    return filtragem[0] if filtragem else None

def depositar(clientes):
    cpf = input("Por favor, informe o CPF do cliente: ")
    cliente = filtrarCliente(cpf, clientes)
    
    if not cliente:
        print("Infelizmente o cliente não foi encontrado")
        return

    valor = float(input("Informe por favor o valor do depósito: "))
    transacao = Deposito(valor)

    conta = recuperarContaCliente(cliente)
    if not conta:
        return

    cliente.realizar_transacao(conta, transacao)
                  
    

def sacar(clientes):
    cpf = input("Por favor, informe o CPF do cliente: ")
    cliente = filtrarCliente(cpf, clientes)

    if not cliente:
        print("Infelizmente o cliente não encontrado")
        return

    valor = float(input("Informe o valor do saque: "))
    transacao = Saque(valor)

    conta = recuperarContaCliente(cliente)
    if not conta:
        return

    cliente.realizar_transacao(conta, transacao)

def emitirExtrato(clientes):
    cpf = input("Por favor, informe o CPF do cliente: ")
    cliente = filtrarCliente(cpf, clientes)

    if not cliente:
        print("Infelizmente o cliente não encontrado")
        return

    conta = recuperarContaCliente(cliente)
    if not conta:
        return

    print("\n================ EXTRATO ================")
    transacoes = conta.historico.transacoes

    extrato = ""
    if not transacoes:
        extrato = "Não foram realizadas movimentações."
    else:
        for transacao in transacoes:
            extrato += f"         {transacao['tipo']} R$ {transacao['valor']:.2f} \n"
    
    print(extrato)
    print(f"Saldo: {conta.saldo:.2f}")
    print("==========================================")

def criarConta(nConta, clientes, contas):
    cpf = input("Por favor, informe o CPF do cliente: ")
    cliente = filtrarCliente(cpf, clientes)

    if not cliente:
        print("Infelizmente o usuário com determinado CPF não foi encontrado")
        return

    conta = ContaCorrente.nova_conta(cliente=cliente, numero=nConta)
    contas.append(conta)
    cliente.contas.append(conta)

    print("Conta criada com sucesso!")

def listarContas(contas):
    if len(contas) > 0:
        for conta in contas:
            print("=" * 60)
            print(str(conta))
    else:
        print("Não existe nenhuma conta criada ainda")
    

def criarCliente(clientes):
    cpf = input("Informe o CPF (somente número): ")
    cliente = filtrarCliente(cpf, clientes)

    if cliente:
        print("Já existe usuário com esse CPF!")
        return
    elif not re.match("\d{11}",cpf):
        print("Os números digitados não batem com o formato de um cpf padrão!")
        return

    nome = input("Informe o nome completo do usuário: ")
    dataNascimento = input("Informe a data de nascimento do usuário de acordo com o formato (dd-mm-aaaa): ")
    endereco = input("Informe o endereçodo usuário de acordo com o formato (logradouro, nro - bairro - cidade/sigla estado): ")

    cliente = PessoaFisica(nome=nome, data_nascimento=dataNascimento, cpf=cpf, endereco=endereco)
    clientes.append(cliente)
    
    print("Cliente criado com sucesso!")



def main():
    lClientes = []
    lContas = []
    
    while True:
        opcao = menu()

        match opcao:
            case "d" | "D":
                depositar(lClientes)

            case "s" | "S":
                sacar(lClientes)
                
            case "e" | "E":
                emitirExtrato(lClientes)
                
            case "nvc" | "NVC":
                numeroConta = len(lContas) + 1
                criarConta(numeroConta, lClientes, lContas)

            case "lc" | "LC":
                listarContas(lContas)
                
            case "nvu" | "NVU":
                criarCliente(lClientes)

            case "q" | "Q":
                print("Saindo do sistema...")
                break
            
            case _:
                print("Operação inválida, por favor selecione novamente a operação desejada.")

main()
