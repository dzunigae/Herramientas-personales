import os
import shutil

# Ruta de la carpeta que contiene las subcarpetas
carpeta_contenedora = "./CVs"

# Carpeta donde se copiarán los PDFs
nueva_carpeta = "./pdfs_unificados"

# Recorrer todas las subcarpetas y archivos
for subdir, _, files in os.walk(carpeta_contenedora):
    for file in files:
        if file.endswith(".pdf"):  # Si el archivo es PDF
            file_path = os.path.join(subdir, file)

            # Generar una nueva ruta en la carpeta de destino
            nuevo_archivo = os.path.join(nueva_carpeta, file)
            
            # Si el archivo ya existe, lo ignoramos
            if os.path.exists(nuevo_archivo):
                print(f"{file} ya existe, ignorado.")
                continue

            
            # Copiar el archivo
            shutil.copy2(file_path, nuevo_archivo)

            print(f"{file} copiado con éxito")