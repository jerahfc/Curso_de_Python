# Crie um programa que leia quanto dinheiro uma pessoa tem na carteira e mostre quantos Dólares ela pode comprar. Considere US$1.00 = R$3.27.

Dólar = 3.27
Dinheiro = float(input("Quanto dinheiro você tem na carteira? "))
print(f"Com esse dinheiro você pode comprar em Dólares um valor de: US${Dinheiro/Dólar:.2f}")

# O :.2f é para mostrar o resultado com 2 casas decimais, deixando a resposta mais bonita e fácil de ler.
