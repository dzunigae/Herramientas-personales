import os

directorio = r"Ruta"

# Obtener una lista de todos los archivos en el directorio
archivos = os.listdir(directorio)

# Cambiar los nombres de los archivos
for archivo in archivos:
    if len(archivo) > 34:
        antigua_ruta = os.path.join(directorio, archivo)
        archivo_en_reversa = "".join(reversed(archivo))
        posicion_punto = archivo_en_reversa.find('.')
        extension_en_reversa = archivo_en_reversa[:posicion_punto]
        extension = "".join(reversed(extension_en_reversa))
        extension = "."+extension
        archivo = archivo[:34]
        nuevo_nombre = archivo + extension

        contador = 1

        while os.path.exists(os.path.join(directorio, nuevo_nombre)):
            nuevo_nombre = archivo + "_" + str(contador) + extension 
            contador += 1

        nueva_ruta = os.path.join(directorio, nuevo_nombre)

        os.rename(antigua_ruta, nueva_ruta)



