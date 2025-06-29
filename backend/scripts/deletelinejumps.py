with open("../data/reviews.txt", "r", encoding="utf-8") as file:
    contenido = file.read()

contenido_sin_saltos = contenido.replace("\n", ". ").replace("\r", ". ")

print(contenido_sin_saltos)

with open("../data/reviews_sin_saltos.txt", "w", encoding="utf-8") as file:
    file.write(contenido_sin_saltos)