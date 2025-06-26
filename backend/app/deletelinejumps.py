# Abrir el archivo y procesarlo para eliminar saltos de línea
with open("reviews.txt", "r", encoding="utf-8") as file:
    contenido = file.read()

# Reemplazar saltos de línea con un espacio vacío
contenido_sin_saltos = contenido.replace("\n", ". ").replace("\r", ". ")

# Ver el resultado
print(contenido_sin_saltos)

# Si quieres guardar el resultado en un nuevo archivo
with open("data_sin_saltos.txt", "w", encoding="utf-8") as file:
    file.write(contenido_sin_saltos)