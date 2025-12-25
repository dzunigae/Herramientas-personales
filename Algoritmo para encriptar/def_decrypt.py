import decrypt_file_by_file  # Módulo externo o script propio, encargado de la desencriptación.
import os  # Funciones para manejar el sistema de archivos.
import zipfile  # Manejo de archivos ZIP (comprimir/descomprimir).
import shutil  # Copiar, mover, eliminar archivos y carpetas.
import sys  # Para interactuar con el intérprete (ej. salir del programa).
from tkinter import filedialog, messagebox  # Cuadros de diálogo y alertas de Tkinter.

# --- Funciones personalizadas ---

def descomprimir_zip(archivo_zip, carpeta_destino):
    """
    Descomprime un archivo ZIP en la carpeta indicada.
    Retorna True si tuvo éxito, False si ocurrió un error.
    """
    if not os.path.exists(archivo_zip):
        # Si el archivo no existe, mostrar error y terminar.
        messagebox.showerror("Error", "El archivo ZIP no existe o la ruta es incorrecta.")
        return False
    try:
        # Abrimos el ZIP en modo lectura y extraemos todo.
        with zipfile.ZipFile(archivo_zip, 'r') as zip_ref:
            zip_ref.extractall(carpeta_destino)
        print(f"✅ Archivos extraídos en: {carpeta_destino}")
        return True
    except Exception as e:
        # Cualquier error al descomprimir se muestra en un mensaje.
        messagebox.showerror("Error", f"❌ No se pudo descomprimir: {str(e)}")
        return False
    
def secure_delete(file_path, block_size=64 * 1024):
    """
    Realiza un borrado seguro sobrescribiendo el archivo con datos aleatorios antes de eliminarlo.
    block_size define el tamaño de cada bloque que se sobrescribe (64 KB por defecto).
    """
    try:
        file_size = os.path.getsize(file_path)  # Tamaño del archivo.
        with open(file_path, "r+b") as f:  # Abrir en lectura/escritura binaria.
            # Sobrescribir por bloques completos.
            for _ in range(file_size // block_size):
                f.write(os.urandom(block_size))  # Genera bytes aleatorios seguros.
            # Sobrescribir los bytes restantes.
            remaining_bytes = file_size % block_size
            if remaining_bytes:
                f.write(os.urandom(remaining_bytes))
            f.flush()
            os.fsync(f.fileno())  # Asegura que los cambios se escriban en disco.
    except Exception as e:
        print(f"Error al sobrescribir {file_path}: {e}")
    finally:
        os.remove(file_path)  # Elimina el archivo definitivamente.

# --- Rutas y claves ---
ruta_encriptado = './0.Assets/Encriptar'
ruta_comprimido = './0.Assets/comprimido'
clave_1 = './0.Assets/password1.txt'
clave_2 = './0.Assets/password2.txt'

# --- Proceso principal ---

# 1. Verificar si existe la segunda clave y desencriptar archivos comprimidos.
print(os.path.exists(clave_2))  # Solo imprime True/False como depuración.
if os.path.exists(clave_2):
    decrypt_file_by_file.main(ruta_comprimido, clave_2)  # Desencripta la carpeta "comprimido".
else:
    messagebox.showerror("Error", "La segunda clave no es válida.")
    sys.exit()  # Sale del programa si falta la clave.

# 2. Buscar un archivo ZIP en la carpeta comprimido.
archivos = [f for f in os.listdir(ruta_comprimido) if f.endswith('.zip')]
if not archivos:
    messagebox.showerror("Error", "No se encontró ningún archivo ZIP en la carpeta comprimido.")
    sys.exit()

# Tomar el primer archivo ZIP encontrado.
ruta_zip = os.path.join(ruta_comprimido, archivos[0])

# 3. Mover el ZIP a la carpeta Encriptar.
ruta_zip_encriptado = os.path.join(ruta_encriptado, archivos[0])
shutil.move(ruta_zip, ruta_zip_encriptado)

# 4. Descomprimir el ZIP en la carpeta Encriptar.
if not descomprimir_zip(ruta_zip_encriptado, ruta_encriptado):
    sys.exit()

# 5. Eliminar el archivo ZIP de forma segura (sobrescribir y borrar).
secure_delete(ruta_zip_encriptado)

# 6. Verificar que se haya extraído una carpeta dentro de Encriptar.
directorios = [d for d in os.listdir(ruta_encriptado) if os.path.isdir(os.path.join(ruta_encriptado, d))]
if not directorios:
    messagebox.showerror("Error", "No se encontró la carpeta extraída en Encriptar.")
    sys.exit()

# Tomar la primera carpeta extraída.
ruta_contenido_extraido = os.path.join(ruta_encriptado, directorios[0])

# 7. Desencriptar el contenido extraído usando la primera clave.
if os.path.exists(clave_1):
    decrypt_file_by_file.main(ruta_encriptado, clave_1)
else:
    messagebox.showerror("Error", "La primera clave no es válida.")
    sys.exit()

# 8. Mensaje final.
print("✅ Proceso completado exitosamente")
