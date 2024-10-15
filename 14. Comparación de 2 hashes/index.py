import hashlib
import os

def calcular_hash(archivo):
    """Calcula el hash SHA-256 de un archivo."""
    hash_sha256 = hashlib.sha256()
    with open(archivo, "rb") as f:
        for bloque in iter(lambda: f.read(4096), b""):
            hash_sha256.update(bloque)
    return hash_sha256.hexdigest()

def obtener_archivos(carpeta):
    """Obtiene los dos primeros archivos de la carpeta dada."""
    archivos = [f for f in os.listdir(carpeta) if os.path.isfile(os.path.join(carpeta, f))]
    if len(archivos) < 2:
        raise ValueError("La carpeta debe contener al menos dos archivos.")
    return archivos[:2]

def comparar_archivos(carpeta):
    """Compara los hashes de los dos primeros archivos en la carpeta."""
    archivo1, archivo2 = obtener_archivos(carpeta)
    ruta1 = os.path.join(carpeta, archivo1)
    ruta2 = os.path.join(carpeta, archivo2)

    hash1 = calcular_hash(ruta1)
    hash2 = calcular_hash(ruta2)

    print(f"Hash de {archivo1}: {hash1}")
    print(f"Hash de {archivo2}: {hash2}")

    if hash1 == hash2:
        print("Los archivos son idénticos (hashes iguales).")
    else:
        print("Los archivos son diferentes (hashes distintos).")

# Ejemplo de uso
carpeta = "./14. Comparación de 2 hashes/assets"  # Ajusta la ruta si es necesario
comparar_archivos(carpeta)
