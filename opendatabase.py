import shelve

# Abre la base de datos shelve en modo lectura
with shelve.open("threads_db", flag='r') as db:
    # Itera sobre todos los elementos de la base de datos
    for key in db.keys():
        # Imprime la clave y su valor correspondiente
        print(f"{key}: {db[key]}")