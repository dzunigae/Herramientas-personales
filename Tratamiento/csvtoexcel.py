import pandas as pd

def csv_a_excel(archivo_csv, archivo_excel):
    # Leer datos desde el archivo CSV
    df = pd.read_csv(archivo_csv)

    # Guardar los datos en un archivo de Excel
    df.to_excel(archivo_excel, index=False)

    print("Archivo CSV convertido a Excel correctamente.")

# Reemplaza "archivo.csv" y "archivo.xlsx" con los nombres de tus archivos
csv_a_excel("archivo.csv", "archivo.xlsx")