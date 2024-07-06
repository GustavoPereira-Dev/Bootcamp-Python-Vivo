def menu():
    menu = """
    ==================== SISTEMA BANCÁRIO ====================
    |                    *[d] Depositar                      |
    |                    *[s] Sacar                          |
    |                    *[e] Extrato                        |
    |                    *[q] Sair                           |
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


def main():
    saldo = 0
    limiteSaldo = 500
    extrato = ""
    numeroSaques = 0
    LIMITE_SAQUES = 3
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
            case "q" | "Q":
                print("Saindo do sistema...")
                break

            case _:
                print("Operação inválida, por favor selecione novamente a operação desejada.")

main()
