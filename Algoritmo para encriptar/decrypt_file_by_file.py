import os  # Librería estándar para manejar archivos y directorios.
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes  # De la librería 'cryptography' (NO estándar).
from cryptography.hazmat.backends import default_backend  # Necesario para inicializar el cifrado.
from cryptography.hazmat.primitives.padding import PKCS7  # Implementa padding PKCS7 (para AES).
import base64  # Para decodificar nombres de archivos que fueron codificados en Base64.

# Tamaño de bloque usado para leer los archivos al descifrar (64 KB).
BLOCK_SIZE = 64 * 1024  

# --- FUNCIONES ---

def derive_key(password: str) -> bytes:
    """
    Deriva la clave AES a partir de una contraseña.
    - Convierte la contraseña a bytes y toma los primeros 32 bytes (AES-256).
    - IMPORTANTE: Esto no usa KDF (función derivadora segura como PBKDF2), por lo que es más débil.
    """
    return password.encode()[:32]  # Toma máximo 32 bytes.

def decrypt_filename(encrypted_filename: str, key: bytes) -> str:
    """
    Descifra el nombre de un archivo previamente cifrado:
    - Usa AES en modo ECB (poco seguro, pero suficiente para nombres).
    - Los nombres están codificados en Base64 URL-safe.
    - Aplica PKCS7 para remover padding.
    Retorna el nombre descifrado como cadena.
    """
    cipher = Cipher(algorithms.AES(key), modes.ECB(), backend=default_backend())
    decryptor = cipher.decryptor()
    
    # Decodificar el nombre desde Base64 (añadiendo '=' por padding).
    encrypted_bytes = base64.urlsafe_b64decode(encrypted_filename + '==')
    
    # Descifrar bytes.
    decrypted_padded = decryptor.update(encrypted_bytes) + decryptor.finalize()
    
    # Remover el padding PKCS7.
    unpadder = PKCS7(algorithms.AES.block_size).unpadder()
    decrypted_name = unpadder.update(decrypted_padded) + unpadder.finalize()
    
    return decrypted_name.decode()  # Convertir a string.

def decrypt_file(file_path: str, key: bytes):
    """
    Descifra el contenido de un archivo cifrado con AES-CBC:
    - Lee el IV (16 bytes) al inicio del archivo.
    - Descifra en bloques de 64 KB.
    - Aplica unpadding PKCS7 al final.
    - Reemplaza el archivo original con la versión descifrada.
    """
    try:
        # Abrir el archivo original para lectura binaria.
        with open(file_path, 'rb') as f_in:
            iv = f_in.read(16)  # Leer el vector de inicialización (IV) de 16 bytes.
            
            # Configurar el descifrador AES-CBC.
            cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
            decryptor = cipher.decryptor()
            
            # Crear archivo temporal donde se escribirá el contenido descifrado.
            temp_file_path = file_path + ".dec"
            with open(temp_file_path, 'wb') as f_out:
                # Leer por bloques para no saturar la memoria.
                while chunk := f_in.read(BLOCK_SIZE):
                    decrypted_chunk = decryptor.update(chunk)
                    f_out.write(decrypted_chunk)
                f_out.write(decryptor.finalize())
            
        # Quitar padding PKCS7 al contenido descifrado.
        with open(temp_file_path, 'rb') as f:
            data = f.read()
        unpadder = PKCS7(algorithms.AES.block_size).unpadder()
        unpadded_data = unpadder.update(data) + unpadder.finalize()
        
        # Sobrescribir el archivo temporal sin padding.
        with open(temp_file_path, 'wb') as f:
            f.write(unpadded_data)
        
        # Reemplazar el archivo original por el descifrado.
        os.replace(temp_file_path, file_path)
        print(f"Archivo descifrado: {file_path}")
    except Exception as e:
        print(f"Error al descifrar {file_path}: {e}")

def decrypt_directory(directory: str, password: str):
    """
    Recorre un directorio y descifra:
    1. El contenido de todos los archivos.
    2. Los nombres de los archivos.
    3. Los nombres de las carpetas.
    - Primero procesa archivos (topdown=True).
    - Luego procesa directorios (topdown=False).
    """
    key = derive_key(password)  # Derivar clave a partir de la contraseña.
    
    # --- Descifrar archivos primero ---
    for root, dirs, files in os.walk(directory, topdown=True):  # Procesa archivos antes que carpetas.
        for file in files:
            file_path = os.path.join(root, file)
            print(f"Descifrando contenido: {file_path}")
            
            # Descifrar el contenido del archivo.
            decrypt_file(file_path, key)
            
            # Descifrar el nombre del archivo.
            decrypted_name = decrypt_filename(file, key)
            decrypted_path = os.path.join(root, decrypted_name)
            
            # Renombrar el archivo con el nombre descifrado.
            os.rename(file_path, decrypted_path)
            print(f"Nombre del archivo descifrado: {decrypted_path}")
        
    # --- Descifrar nombres de directorios después ---
    for root, dirs, _ in os.walk(directory, topdown=False):  # Procesa directorios al final.
        for dir_name in dirs:
            dir_path = os.path.join(root, dir_name)
            decrypted_name = decrypt_filename(dir_name, key)
            decrypted_path = os.path.join(root, decrypted_name)
            
            # Renombrar el directorio.
            os.rename(dir_path, decrypted_path)
            print(f"Nombre del directorio descifrado: {decrypted_path}")

def main(directory, ruta_contraseña):
    """
    Punto de entrada principal:
    - Lee la contraseña desde un archivo.
    - Llama a decrypt_directory para descifrar todo el directorio.
    """
    with open(ruta_contraseña, 'r') as archivo:
        contraseña = archivo.readline().strip()  # Leer primera línea del archivo y limpiar espacios.
    decrypt_directory(directory, contraseña)

"""
if __name__ == "__main__":
    ruta = "./Algoritmo para encriptar/Encriptar"
    contra = './Algoritmo para encriptar/assets/password1.txt'

    for subcarpeta in os.listdir(ruta):
        ruta_subcarpeta = os.path.join(ruta, subcarpeta)
        if os.path.isdir(ruta_subcarpeta):
            main(ruta_subcarpeta,contra)
"""
