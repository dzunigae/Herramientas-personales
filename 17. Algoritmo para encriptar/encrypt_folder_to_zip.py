import os
import zipfile
from tkinter import Tk, filedialog
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
import hashlib

def select_folder():
    """Open a dialog to select a folder."""
    Tk().withdraw()  # Close the root Tk window
    folder_path = filedialog.askdirectory(title="Select a folder to encrypt")
    return folder_path

def compress_folder(folder_path):
    """Compress the selected folder into a zip file."""
    zip_file = folder_path + ".zip"
    with zipfile.ZipFile(zip_file, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, folder_path)
                zipf.write(file_path, arcname)
    return zip_file

def encrypt_file(file_path, key):
    """Encrypt the zip file using AES encryption."""
    encrypted_file = file_path + ".enc"
    cipher = AES.new(key, AES.MODE_CBC)
    iv = cipher.iv

    with open(file_path, 'rb') as f:
        plaintext = f.read()

    ciphertext = cipher.encrypt(pad(plaintext, AES.block_size))

    with open(encrypted_file, 'wb') as f:
        f.write(iv)  # Save the IV at the beginning of the file
        f.write(ciphertext)

    return encrypted_file

def main():
    print("Select the folder you want to encrypt...")
    folder_path = select_folder()
    if not folder_path:
        print("No folder selected. Exiting.")
        return

    print("Compressing folder...")
    zip_file = compress_folder(folder_path)
    print(f"Folder compressed into: {zip_file}")

    password = input("Enter a password for encryption: ")
    key = hashlib.sha256(password.encode()).digest()  # Derive a 256-bit key from the password

    print("Encrypting zip file...")
    encrypted_file = encrypt_file(zip_file, key)
    print(f"File encrypted successfully: {encrypted_file}")

    # Optionally, delete the original zip file for security
    os.remove(zip_file)
    print("Original zip file deleted for security.")

if __name__ == "__main__":
    main()