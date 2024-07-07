menu = """
==================== SISTEMA BANCÁRIO ====================
|                    *[d] Depositar                      |
|                    *[s] Sacar                          |
|                    *[e] Extrato                        |
|                    *[q] Sair                           |
==========================================================
=> """

saldo = 0
limiteSaldo = 500
extrato = ""
numeroSaques = 0
LIMITE_SAQUES = 3

while True:

    opcao = input(menu)

    match opcao:
        case "d" | "D":
            valor = float(input("Informe o valor do depósito: "))

            if valor > 0:
                saldo += valor
                extrato += f"         + Depósito: R$ {valor:.2f}\n"
            else:
                print("Operação falhou! O valor informado é inválido.")

        case "s" | "S":
            valor = float(input("Informe o valor do saque: "))

            if valor > saldo:
                print("Operação falhou! Você não tem saldo suficiente.")
            elif valor > limiteSaldo:
                print("Operação falhou! O valor do saque excede o limite.")
            elif numeroSaques >= LIMITE_SAQUES:
                print("Operação falhou! Número máximo de saques excedido.")
            elif valor > 0:
                saldo -= valor
                extrato += f"         - Saque: R$ {valor:.2f}\n"
                numeroSaques += 1
            else:
                print("Operação falhou! O valor informado é inválido.")

        case "e" | "E":
            print("\n================ EXTRATO ================")
            print("Não foram realizadas movimentações." if not extrato else extrato)
            print(f"\nSaldo: R$ {saldo:.2f}")
            print("==========================================")

        case "q" | "Q":
            print("Saindo do sistema...")
            break

        case _:
            print("Operação inválida, por favor selecione novamente a operação desejada.")