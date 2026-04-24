#------------DESAFIO RÁPIDO SEM VALER NADA------------------------------------------------------

n1 = int(input("digite um valor: "))
n2 = int(input("digite outro valor: "))
s = n1 + n2
# jeito muito longo ---> print("A soma entre ", n1, "e", n2, "é", s)

# jeito antigo no Python 3.2 ---> print("A soma entre {} e {} vale {}".format(n1, n2, s))

print(f"A soma entre {n1} e {n2} vale {s}")

#------------DESAFIO_004-----------------------------------------------------------------------

# Faça um programa que leia algo pelo teclado e mostre na tela o seu tipo primitivo e todas as informações possíveis sobre ele?

n = input("Digite algo: ")
print(n.isnumeric)
