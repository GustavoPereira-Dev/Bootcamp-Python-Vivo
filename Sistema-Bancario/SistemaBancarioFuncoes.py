import re

def menu():
    menu = """
    ==================== SISTEMA BANCÁRIO ====================
    |                    *[d]   Depositar                    |
    |                    *[s]   Sacar                        |
    |                    *[e]   Extrato                      |
    |                    *[nvc] Nova conta                   |
    |                    *[lc]  Listar contas                |
    |                    *[nvu] Novo usuário                 |
    |                    *[q]   Sair                         |
    ==========================================================
    => """

    return input(menu)


def depositar(saldo, valor, extrato):
    if valor > 0:
        saldo += valor
        extrato += f"         + Depósito: R$ {valor:.2f}\n"
    else:
        print("Operação falhou! O valor informado é inválido.")

    return saldo, extrato

def sacar(*,saldo,valor,extrato,limite,numeroSaques,LIMITE_SAQUES):
    if valor > saldo:
        print("Operação falhou! Você não tem saldo suficiente.")
    elif valor > limite:
        print("Operação falhou! O valor do saque excede o limite.")
    elif numeroSaques >= LIMITE_SAQUES:
        print("Operação falhou! Número máximo de saques excedido.")
    elif valor > 0:
        saldo -= valor
        extrato += f"         - Saque: R$ {valor:.2f}\n"
        numeroSaques += 1
    else:
        print("Operação falhou! O valor informado é inválido.")

    return saldo,extrato

def emitirExtrato(saldo,/,*,extrato):
    print("\n================ EXTRATO ================")
    print("Não foram realizadas movimentações." if not extrato else extrato)
    print(f"\nSaldo: R$ {saldo:.2f}")
    print("==========================================")

def filtrarUsuario(cpf, usuarios):
    filtragem = [usuario for usuario in usuarios if usuario["cpf"] == cpf]
    return filtragem[0] if filtragem else None

def criarConta(agencia, nConta, usuarios):
    cpf = input("Por favor, informe o CPF do usuário: ")
    usuario = filtrarUsuario(cpf, usuarios)

    if usuario:
        print(f"Conta do usuário do número de agência {agencia} número da conta {nConta} e cpf {cpf} criado com sucesso")
        return{"agencia": agencia, "numeroConta": nConta, "usuario": usuario}
    print("Infelizmente o usuário de determinado CPF não foi encontrado")

def criarUsuario(usuarios):
    cpf = input("Por favor, informe o CPF do usuário: ")
    usuario = filtrarUsuario(cpf, usuarios)
    
    if usuario:
        print("Já existe um usuário com esse CPF!")
        return
    elif not re.match(r"\d{11}", cpf):
        print("Essa numeração não bate com um CPF comum!")
        return

    nome = input("Informe o nome: ")
    dataNascimento = input("Informe a data de nascimento do usuário no formato (dd-mm-aaaa): ")
    endereco = input("Informe o endereço do usuário no formato (logradouro, nro - bairro - cidade/sigla estado): ")
    usuarios.append({"nome": nome, "dataNascimento": dataNascimento, "cpf": cpf, "endereco": endereco})

    print("Usuario criado com sucesso!")

def listarContas(contas):
    if len(contas) > 0:
        for conta in contas:
            lista = f"""
                Agência:              {conta['agencia']}
                Número da conta:      {conta['numeroConta']}
                Usuário:              {conta['usuario']['nome']}
            """
            print("=" * 60)
            print(lista)
    else:
        print("Não existem contas para visualizar!")
        


    


def main():
    saldo = 0
    limiteSaldo = 500
    extrato = ""
    numeroSaques = 0

    lUsuarios = []
    lContas = []

    LIMITE_SAQUES = 3
    AGENCIA = "0001"
    while True:

        opcao = menu()

        match opcao:
            case "d" | "D":
                valor = float(input("Informe o valor do depósito: "))
                saldo, extrato = depositar(saldo, valor, extrato)

            case "s" | "S":
                valor = float(input("Informe o valor do saque: "))
                saldo, extrato = sacar(
                    saldo=saldo,
                    valor=valor,
                    extrato=extrato,
                    limite=limiteSaldo,
                    numeroSaques=numeroSaques,
                    LIMITE_SAQUES=LIMITE_SAQUES
                )
                
            case "e" | "E":
                emitirExtrato(
                    saldo,
                    extrato=extrato
                )
                
            case "nvc" | "NVC":
                numeroConta = len(lContas) + 1
                conta = criarConta(AGENCIA, numeroConta, lUsuarios)

                if conta:
                    lContas.append(conta)
                    
            case "lc" | "LC":
                listarContas(lContas)

            case "nvu" | "NVU":
                criarUsuario(lUsuarios)
                
            case "q" | "Q":
                print("Saindo do sistema...")
                break

            case _:
                print("Operação inválida, por favor selecione novamente a operação desejada.")

main()
