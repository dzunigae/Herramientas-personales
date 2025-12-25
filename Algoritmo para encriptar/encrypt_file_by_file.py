import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.padding import PKCS7
import secrets
import base64

# Tamaño del bloque para manejar archivos grandes
BLOCK_SIZE = 64 * 1024  # 64 KB

# Función para derivar una clave usando solo la contraseña
def derive_key(password: str) -> bytes:
    return password.encode()[:32]  # Usar los primeros 32 bytes de la contraseña

def secure_delete(file_path, block_size=64 * 1024):
    """Sobrescribe un archivo con datos aleatorios por bloques antes de eliminarlo."""
    try:
        file_size = os.path.getsize(file_path)
        with open(file_path, "r+b") as f:
            for _ in range(file_size // block_size):
                f.write(os.urandom(block_size))  # Sobrescribe en bloques
            remaining_bytes = file_size % block_size
            if remaining_bytes:
                f.write(os.urandom(remaining_bytes))  # Sobrescribe el resto
            f.flush()
            os.fsync(f.fileno())  # Asegurar escritura en disco
    except Exception as e:
        print(f"Error al sobrescribir {file_path}: {e}")
    finally:
        os.remove(file_path)  # Eliminar el archivo

# Función para cifrar nombres de archivos
def encrypt_filename(filename: str, key: bytes) -> str:
    cipher = Cipher(algorithms.AES(key), modes.ECB(), backend=default_backend())
    encryptor = cipher.encryptor()

    # Agregar padding al nombre para que sea múltiplo del tamaño del bloque (16 bytes)
    padder = PKCS7(algorithms.AES.block_size).padder()
    padded_name = padder.update(filename.encode()) + padder.finalize()

    # Cifrar el nombre
    encrypted_name = encryptor.update(padded_name) + encryptor.finalize()

    # Convertir a base64 para que sea compatible con nombres de archivo
    return base64.urlsafe_b64encode(encrypted_name).decode().rstrip('=')

# Función para cifrar un archivo en bloques grandes
def encrypt_file(file_path: str, key: bytes):
    try:
        # Generar un IV único para cada archivo
        iv = secrets.token_bytes(16)
        cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
        encryptor = cipher.encryptor()

        temp_file_path = file_path + ".enc"

        ultimo_bloque_no_necesita_padding = True

        with open(file_path, 'rb') as f_in, open(temp_file_path, 'wb') as f_out:
            # Escribir el IV al principio del archivo cifrado
            f_out.write(iv)

            # Procesar el archivo en bloques
            while chunk := f_in.read(BLOCK_SIZE):
                if len(chunk) < BLOCK_SIZE:  # Último bloque
                    ultimo_bloque_no_necesita_padding = False
                    padder = PKCS7(algorithms.AES.block_size).padder()
                    chunk = padder.update(chunk) + padder.finalize()

                encrypted_chunk = encryptor.update(chunk)
                f_out.write(encrypted_chunk)
        
            if ultimo_bloque_no_necesita_padding:
                # Definir 16 bytes con el valor 0x10 (16 en decimal)
                padding_bytes = bytes([16] * 16)

                encrypted_chunk = encryptor.update(padding_bytes)

                # Escribir el padding al final del archivo
                f_out.write(encrypted_chunk)
            
            # Finalizar el cifrado
            f_out.write(encryptor.finalize())

        secure_delete(file_path)

        # Reemplazar el archivo original por el cifrado
        os.replace(temp_file_path, file_path)
        print(f"Archivo cifrado: {file_path}")

    except Exception as e:
        print(f"Error al cifrar {file_path}: {e}")

# Función para recorrer directorios, cifrar archivos y sus nombres y los nombres de los directorios
def encrypt_directory(directory: str, password: str):
    key = derive_key(password)
    
    # Recorrer primero los archivos
    for root, dirs, files in os.walk(directory, topdown=False):  # topdown=False para procesar los directorios después de los archivos
        for file in files:
            file_path = os.path.join(root, file)
            print(f"Cifrando contenido: {file_path}")

            # Cifrar el contenido del archivo
            encrypt_file(file_path, key)

            # Cifrar el nombre del archivo
            encrypted_name = encrypt_filename(file, key)
            encrypted_path = os.path.join(root, encrypted_name)

            # Renombrar el archivo con el nombre cifrado
            os.rename(file_path, encrypted_path)
            print(f"Nombre del archivo cifrado: {encrypted_path}")

        # Ahora cifrar nombres de directorios
        for dir_name in dirs:
            dir_path = os.path.join(root, dir_name)
            encrypted_name = encrypt_filename(dir_name, key)
            encrypted_path = os.path.join(root, encrypted_name)

            # Renombrar el directorio
            os.rename(dir_path, encrypted_path)
            print(f"Nombre del directorio cifrado: {encrypted_path}")

def main(directory,ruta_contraseña):
    with open(ruta_contraseña, 'r') as archivo:
        contraseña = archivo.readline().strip()
    encrypt_directory(directory, contraseña)