# Este script recorre de forma recursiva un directorio y calcula el hash SHA-256
# de cada archivo para detectar duplicados reales por contenido.
#
# Los hashes y metadatos de los archivos se almacenan en una base de datos SQLite,
# lo que permite evitar reprocesar archivos ya analizados y reanudar el proceso
# en caso de interrupción (Ctrl+C).
#
# Cuando se detectan archivos con el mismo hash, se registran como duplicados y
# se genera un reporte consolidado en un archivo Excel con los hashes y las rutas
# de todos los archivos duplicados encontrados.
#
# El script maneja errores de acceso a archivos y permite una detención segura
# del proceso sin pérdida de progreso.


import os
import hashlib
import sqlite3
import pandas as pd
from pathlib import Path
import signal

# Variables globales para manejo de interrupciones
stop_processing = False

def signal_handler(sig, frame):
    global stop_processing
    stop_processing = True
    print("\nProceso detenido de forma segura. Puedes reanudarlo más tarde.")

signal.signal(signal.SIGINT, signal_handler)

def calculate_hash(file_path, chunk_size=8192):
    """Calcula el hash SHA-256 de un archivo."""
    sha256 = hashlib.sha256()
    try:
        with open(file_path, 'rb') as f:
            while chunk := f.read(chunk_size):
                sha256.update(chunk)
        print(f"Archivo {file_path} procesado.")
        return sha256.hexdigest()
    except (PermissionError, FileNotFoundError):
        print(f"No se pudo acceder al archivo: {file_path}")
        return None

def initialize_database(db_path):
    """Inicializa la base de datos SQLite."""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS files (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        file_name TEXT,
                        file_path TEXT,
                        file_hash TEXT UNIQUE
                    )''')
    conn.commit()
    return conn

def process_directory(directory, conn):
    """Procesa los archivos en un directorio y detecta duplicados."""
    cursor = conn.cursor()
    report = {}

    # Recuperar el progreso anterior
    cursor.execute("SELECT MAX(file_path) FROM files")
    last_processed = cursor.fetchone()[0]
    skip = bool(last_processed)

    for root, _, files in os.walk(directory):
        for file_name in files:
            if stop_processing:
                return report

            file_path = os.path.join(root, file_name)
            if skip:
                if file_path == last_processed:
                    skip = False
                continue

            file_hash = calculate_hash(file_path)
            if file_hash:
                cursor.execute("SELECT file_path FROM files WHERE file_hash = ?", (file_hash,))
                duplicate = cursor.fetchall()

                if duplicate:
                    if file_hash not in report:
                        report[file_hash] = []
                    report[file_hash].append(file_path)
                    for dup in duplicate:
                        report[file_hash].append(dup[0])
                else:
                    cursor.execute("INSERT INTO files (file_name, file_path, file_hash) VALUES (?, ?, ?)",
                                   (file_name, file_path, file_hash))

            conn.commit()

    return report

def save_report_to_excel(report, output_path):
    """Guarda todos los duplicados en una única hoja de Excel."""
    consolidated_data = []
    for file_hash, paths in report.items():
        for path in paths:
            consolidated_data.append({"Hash": file_hash, "File Path": path})
    # Crear un DataFrame consolidado
    df = pd.DataFrame(consolidated_data)
    # Guardar en un único archivo Excel
    df.to_excel(output_path, sheet_name="Duplicates", index=False)


if __name__ == "__main__":
    # Configuración inicial
    directory_to_scan = './59. Backup_PC_mesa'
    database_path = "file_hashes.db"
    excel_report_path = "duplicate_report.xlsx"

    conn = initialize_database(database_path)

    try:
        print("Iniciando el proceso. Presiona Ctrl+C para detenerlo de forma segura.")
        duplicates = process_directory(directory_to_scan, conn)

        if duplicates:
            print(f"Generando reporte en {excel_report_path}...")
            save_report_to_excel(duplicates, excel_report_path)
            print("Reporte generado con éxito.")
        else:
            print("No se encontraron archivos duplicados.")

    finally:
        conn.close()
