import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.padding import PKCS7

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

# Función para descifrar un archivo
def decrypt_file(file_path: str, key: bytes):
    # Leer el archivo cifrado
    with open(file_path, 'rb') as f:
        data = f.read()

    # Separar el IV y los datos cifrados
    iv = data[:16]
    encrypted_data = data[16:]

    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()

    # Descifrar los datos
    padded_data = decryptor.update(encrypted_data) + decryptor.finalize()

    # Remover el padding
    unpadder = PKCS7(algorithms.AES.block_size).unpadder()
    original_data = unpadder.update(padded_data) + unpadder.finalize()

    # Sobrescribir el archivo con los datos descifrados
    with open(file_path, 'wb') as f:
        f.write(original_data)

# Función para recorrer directorios y descifrar archivos
def decrypt_directory(directory: str, password: str):
    # Leer el salt guardado durante el cifrado
    salt_path = os.path.join(directory, "encryption_salt.bin")
    if not os.path.exists(salt_path):
        print("Error: No se encontró el archivo 'encryption_salt.bin'. Asegúrate de estar en el directorio correcto.")
        return

    with open(salt_path, 'rb') as f:
        salt = f.read()

    # Derivar la clave usando la contraseña y el salt
    key = derive_key(password, salt)

    # Recorrer todos los archivos y descifrarlos
    for root, _, files in os.walk(directory):
        for file in files:
            if file != "encryption_salt.bin":  # Evitar procesar el archivo del salt
                file_path = os.path.join(root, file)
                print(f"Descifrando: {file_path}")
                try:
                    decrypt_file(file_path, key)
                except Exception as e:
                    print(f"Error al descifrar {file_path}: {e}")

    # Eliminar el archivo 'encryption_salt.bin' si ya no es necesario
    os.remove(salt_path)
    print("Descifrado completado. El archivo 'encryption_salt.bin' ha sido eliminado.")

if __name__ == "__main__":
    # Solicitar carpeta y contraseña al usuario
    directory = './17. Algoritmo para encriptar/Encriptar'
    password = ''

    decrypt_directory(directory, password)
