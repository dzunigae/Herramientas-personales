import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.padding import PKCS7
import secrets

# Función para derivar una clave usando una contraseña y un salt
def derive_key(password: str, salt: bytes) -> bytes:
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100_000,
        backend=default_backend()
    )
    return kdf.derive(password.encode())

# Función para cifrar un archivo
def encrypt_file(file_path: str, key: bytes):
    # Generar un IV único para cada archivo
    iv = secrets.token_bytes(16)
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()

    # Leer el contenido del archivo y agregar padding
    with open(file_path, 'rb') as f:
        data = f.read()

    padder = PKCS7(algorithms.AES.block_size).padder()
    padded_data = padder.update(data) + padder.finalize()

    # Cifrar los datos
    encrypted_data = encryptor.update(padded_data) + encryptor.finalize()

    # Sobrescribir el archivo con los datos cifrados (IV + datos cifrados)
    with open(file_path, 'wb') as f:
        f.write(iv + encrypted_data)

# Función para recorrer directorios y cifrar archivos
def encrypt_directory(directory: str, password: str):
    # Generar un salt para la derivación de clave
    salt = secrets.token_bytes(16)
    key = derive_key(password, salt)

    # Guardar el salt para descifrado posterior (puede guardarse en un archivo aparte)
    with open(os.path.join(directory, "encryption_salt.bin"), "wb") as f:
        f.write(salt)

    # Recorrer todos los archivos y cifrarlos
    for root, _, files in os.walk(directory):
        for file in files:
            if file != "encryption_salt.bin":  # Evitar cifrar el archivo del salt
                file_path = os.path.join(root, file)
                print(f"Cifrando: {file_path}")
                try:
                    encrypt_file(file_path, key)
                except PermissionError as e:
                    print(f"Error de permisos al cifrar {file_path}: {e}")

if __name__ == "__main__":
    # Solicitar carpeta y contraseña al usuario
    directory = './17. Algoritmo para encriptar/Encriptar'
    password = ''
    
    encrypt_directory(directory, password)
