# Faça um programa que leia um número Inteiro qualquer e mostre na tela a sua tabuada.

t = int(input("Digite um número: "))
print(f"A tabuada do {t} é:  \n{t*1}\n{t*2}\n{t*3}\n{t*4}\n{t*5}\n{t*6}\n{t*7}\n{t*8}\n{t*9}\n{t*10}")

# O \n é para pular uma linha, deixando a tabuada mais organizada e fácil de ler.

# ------------OUTRA FORMA DE FAZER--------------------------------------------------------------------------------------

t = int(input("Digite um número: "))
print("-"*20)
print(f"A tabuada do {t} é:  \n{t}x1={t*1}\n{t}x2={t*2}\n{t}x3={t*3}\n{t}x4={t*4}\n{t}x5={t*5}\n{t}x6={t*6}\n{t}x7={t*7}\n{t}x8={t*8}\n{t}x9={t*9}\n{t}x10={t*10}")
print("-"*20)