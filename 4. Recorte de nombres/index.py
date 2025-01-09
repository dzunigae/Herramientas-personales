import os

directorio = "./4. Recorte de nombres/assets"

# Recorrer todos los directorios y archivos dentro del directorio
for ruta_directorio, subdirectorios, archivos in os.walk(directorio):
    for archivo in archivos:
        if len(archivo) > 50:
            antigua_ruta = os.path.join(ruta_directorio, archivo)
            archivo_en_reversa = "".join(reversed(archivo))
            posicion_punto = archivo_en_reversa.find('.')
            extension_en_reversa = archivo_en_reversa[:posicion_punto]
            extension = "".join(reversed(extension_en_reversa))
            extension = "." + extension
            archivo = archivo[:50]
            nuevo_nombre = archivo + extension

            contador = 1

            while os.path.exists(os.path.join(ruta_directorio, nuevo_nombre)):
                nuevo_nombre = archivo + "_" + str(contador) + extension
                contador += 1

            nueva_ruta = os.path.join(ruta_directorio, nuevo_nombre)

            os.rename(antigua_ruta, nueva_ruta)