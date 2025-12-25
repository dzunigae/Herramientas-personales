import tkinter as tk
import encrypt_file_by_file
import os
import shutil
import zipfile
from tkinter import filedialog, messagebox

def comprimir_contenido(carpeta_origen, zip_destino):
    try:
        with zipfile.ZipFile(zip_destino, 'w', zipfile.ZIP_DEFLATED, allowZip64=True) as zipf:
            for carpeta_raiz, _, archivos in os.walk(carpeta_origen):
                for archivo in archivos:
                    ruta_completa = os.path.join(carpeta_raiz, archivo)
                    ruta_relativa = os.path.relpath(ruta_completa, carpeta_origen)  
                    zipf.write(ruta_completa, ruta_relativa)  
        print(f"✅ ¡Zip creado correctamente en {zip_destino}!")
    except Exception as e:
        messagebox.showerror("Error", f"Hubo un problema al comprimir: {str(e)}")

def limpiar_carpeta(ruta_carpeta):
    if not os.path.exists(ruta_carpeta):
        print(f"La carpeta '{ruta_carpeta}' no existe.")
        return
    
    for archivo in os.listdir(ruta_carpeta):
        ruta_archivo = os.path.join(ruta_carpeta, archivo)
        try:
            if os.path.isfile(ruta_archivo) or os.path.islink(ruta_archivo):
                os.unlink(ruta_archivo)  # Eliminar archivos y enlaces simbólicos
            elif os.path.isdir(ruta_archivo):
                shutil.rmtree(ruta_archivo)  # Eliminar directorios y su contenido
        except Exception as e:
            print(f"Error al eliminar {ruta_archivo}: {e}")

# Variables clave
ruta_encriptado = './0.Assets/Encriptar'
ruta_comprimido = './0.Assets/comprimido'
clave_1 = './0.Assets/password1.txt'
clave_2 = './0.Assets/password2.txt'

# Ejecutar encriptación con la primera clave
if os.path.exists(clave_1):
    encrypt_file_by_file.main(ruta_encriptado, clave_1)
else:
    messagebox.showerror("Error", "La primera clave no es válida.")
    exit()

# Definir el nombre del zip dentro de la misma carpeta
zip_salida = os.path.join(ruta_comprimido, "contenido_comprimido.zip")
comprimir_contenido(ruta_encriptado, zip_salida)

# Eliminar los archivos comprimidos
limpiar_carpeta(ruta_encriptado)

# Ejecutar encriptación con la segunda clave
if os.path.exists(clave_2):
    encrypt_file_by_file.main(ruta_comprimido, clave_2)
else:
    messagebox.showerror("Error", "La segunda clave no es válida.")
    exit()