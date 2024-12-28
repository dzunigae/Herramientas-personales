import os
from tkinter import Tk, filedialog
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
import hashlib
import zipfile

def select_file():
    """Open a dialog to select an encrypted file."""
    Tk().withdraw()  # Close the root Tk window
    file_path = filedialog.askopenfilename(title="Select the encrypted (.enc) file")
    return file_path

def decrypt_file(encrypted_file, key):
    """Decrypt the .enc file using AES and return the decrypted data."""
    with open(encrypted_file, 'rb') as f:
        iv = f.read(16)  # Read the IV (first 16 bytes)
        ciphertext = f.read()  # Read the rest of the file

    cipher = AES.new(key, AES.MODE_CBC, iv=iv)
    plaintext = unpad(cipher.decrypt(ciphertext), AES.block_size)

    # Save the decrypted content as a zip file
    decrypted_file = encrypted_file.replace('.enc', '_decrypted.zip')
    with open(decrypted_file, 'wb') as f:
        f.write(plaintext)

    return decrypted_file

def extract_zip_file(zip_file):
    """Extract the decrypted zip file to a folder."""
    output_folder = zip_file.replace('_decrypted.zip', '_extracted')
    with zipfile.ZipFile(zip_file, 'r') as zipf:
        zipf.extractall(output_folder)
    return output_folder

def main():
    print("Select the encrypted file you want to decrypt...")
    encrypted_file = select_file()
    if not encrypted_file:
        print("No file selected. Exiting.")
        return

    password = input("Enter the password for decryption: ")
    key = hashlib.sha256(password.encode()).digest()  # Derive the 256-bit key from the password

    print("Decrypting file...")
    try:
        decrypted_zip = decrypt_file(encrypted_file, key)
        print(f"File decrypted successfully: {decrypted_zip}")

        print("Extracting zip file...")
        extracted_folder = extract_zip_file(decrypted_zip)
        print(f"Files extracted successfully to: {extracted_folder}")

        # Optionally, delete the decrypted zip file for security
        os.remove(decrypted_zip)
        print("Decrypted zip file deleted for security.")
    except (ValueError, KeyError) as e:
        print("Decryption failed. Ensure the password is correct.")

if __name__ == "__main__":
    main()