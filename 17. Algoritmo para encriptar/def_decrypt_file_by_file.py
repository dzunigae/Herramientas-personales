import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.padding import PKCS7
import base64

# Tamaño del bloque para manejar archivos grandes
BLOCK_SIZE = 64 * 1024  # 64 KB

# Función para derivar una clave usando solo la contraseña
def derive_key(password: str) -> bytes:
    return password.encode()[:32]  # Usar los primeros 32 bytes de la contraseña

def decrypt_file(file_path: str, key: bytes):
    """
    Descifra el contenido de un archivo cifrado previamente.
    """
    try:
        temp_file_path = file_path + ".dec"

        with open(file_path, 'rb') as f_in, open(temp_file_path, 'wb') as f_out:
            # Leer el IV desde el principio del archivo cifrado
            iv = f_in.read(16)  # Los primeros 16 bytes son el IV
            cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
            decryptor = cipher.decryptor()

            # Procesar el archivo en bloques
            decrypted_data = b''  # Para manejar el último bloque con padding
            while chunk := f_in.read(BLOCK_SIZE):
                decrypted_data += decryptor.update(chunk)

            # Finalizar el descifrado
            decrypted_data += decryptor.finalize()

            # Remover padding del último bloque
            try:
                unpadder = PKCS7(algorithms.AES.block_size).unpadder()
                decrypted_data = unpadder.update(decrypted_data) + unpadder.finalize()
            except ValueError as e:
                print(f"Error al remover padding: {e}")
                print(f"Archivo posiblemente corrupto: {file_path}")
                return

            f_out.write(decrypted_data)

        # Reemplazar el archivo cifrado con el archivo descifrado
        os.replace(temp_file_path, file_path)
        print(f"Archivo descifrado: {file_path}")

    except Exception as e:
        print(f"Error al descifrar {file_path}: {e}")


def decrypt_filename(encrypted_filename: str, key: bytes) -> str:
    """
    Descifra un nombre de archivo o directorio cifrado previamente.
    """
    try:
        cipher = Cipher(algorithms.AES(key), modes.ECB(), backend=default_backend())
        decryptor = cipher.decryptor()

        # Convertir de base64 a bytes
        encrypted_bytes = base64.urlsafe_b64decode(encrypted_filename + '=' * (-len(encrypted_filename) % 4))

        # Descifrar el nombre y eliminar padding
        padded_name = decryptor.update(encrypted_bytes) + decryptor.finalize()
        unpadder = PKCS7(algorithms.AES.block_size).unpadder()
        original_name = unpadder.update(padded_name) + unpadder.finalize()

        return original_name.decode()

    except Exception as e:
        print(f"Error al descifrar el nombre '{encrypted_filename}': {e}")
        return encrypted_filename  # Retorna el nombre original si falla


def decrypt_directory(directory: str, password: str):
    """
    Descifra los archivos y directorios dentro de un directorio dado.
    """
    key = derive_key(password)

    # Procesar en orden inverso (archivos primero, luego directorios)
    for root, dirs, files in os.walk(directory, topdown=False):
        # Descifrar archivos
        for file in files:
            file_path = os.path.join(root, file)
            print(f"Descifrando contenido: {file_path}")

            # Descifrar contenido del archivo
            decrypt_file(file_path, key)

            # Descifrar nombre del archivo
            decrypted_name = decrypt_filename(file, key)
            decrypted_path = os.path.join(root, decrypted_name)

            # Renombrar el archivo con su nombre descifrado
            os.rename(file_path, decrypted_path)
            print(f"Nombre del archivo descifrado: {decrypted_path}")

        # Descifrar directorios
        for dir_name in dirs:
            dir_path = os.path.join(root, dir_name)
            decrypted_name = decrypt_filename(dir_name, key)
            decrypted_path = os.path.join(root, decrypted_name)

            # Renombrar el directorio con su nombre descifrado
            os.rename(dir_path, decrypted_path)
            print(f"Nombre del directorio descifrado: {decrypted_path}")


if __name__ == "__main__":
    # Solicitar carpeta y contraseña al usuario
    directory = '.\\17. Algoritmo para encriptar\\Encriptar'
    ruta_contraseña = '.\\17. Algoritmo para encriptar\\assets\\password.txt'
    with open(ruta_contraseña, 'r') as archivo:
        contraseña = archivo.readline().strip()

    decrypt_directory(directory, contraseña)

