# Faça um programa que leia a largura e a altura de uma parede em metros, calcule a sua área e a quantidade de tinta necessária para pintá-la, sabendo que cada litro de tinta, pinta uma área de 2m².

largura = float(input("Qual a largura da sua parede em metros? "))
altura = float(input("Qual a altura da sua parede em metros? "))
area = largura * altura
quantidade_de_tinta = area / 2
print(f"A área da sua parede é de {area:.2f} m²")
print(f"A quantidade de tinta necessária em litros para pintar sua parede é de {quantidade_de_tinta:.1f} L")
