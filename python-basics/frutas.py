frutas = ["bananas", "maçãs", "peras", "uvas", "laranjas"]

while True:
  fruta = input("Digite uma fruta: ")

  if fruta == "999":
    break

  if fruta in frutas:
    print(fruta, "já existe na lista.")
  else:
    frutas.append(fruta)
    print(fruta, "foi adicionada à lista.")

print("Lista final de frutas:", frutas)