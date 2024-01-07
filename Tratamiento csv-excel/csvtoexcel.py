import pandas as pd
import os

RUTA = './Tratamiento csv-excel/assets'

def csv_a_excel(RUTA):
    # Listar archivos CSV en la carpeta
    ARCHIVOS_CSV = [archivo for archivo in os.listdir(RUTA) if archivo.endswith('.csv')]
    
    # Iterar sobre los archivos CSV
    for archivo in ARCHIVOS_CSV:
        # Construir la ruta completa del archivo CSV
        ruta_csv = os.path.join(RUTA, archivo)
        
        # Construir la ruta completa del archivo Excel
        archivo_excel = os.path.join(RUTA, archivo.replace('.csv', '.xlsx'))

        # Leer datos desde el archivo CSV
        df = pd.read_csv(ruta_csv)

        # Guardar los datos en un archivo de Excel
        df.to_excel(archivo_excel, index=False)

        print(f"Archivo CSV '{ruta_csv}' convertido a Excel correctamente.")
        

# Reemplaza "carpeta_csv" y "carpeta_excel" con las rutas de tus carpetas
csv_a_excel(RUTA)
