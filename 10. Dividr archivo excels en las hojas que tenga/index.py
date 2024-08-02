import pandas as pd
import os

# Rutas de las carpetas
input_folder = './10. Dividr archivo excels en las hojas que tenga/assets'
output_folder = './10. Dividr archivo excels en las hojas que tenga/out'

# Obtener la lista de archivos en la carpeta de entrada
input_files = os.listdir(input_folder)

# Filtrar solo archivos de Excel
excel_files = [file for file in input_files if file.endswith('.xlsx')]

# Asegurarse de que haya al menos un archivo de Excel
if not excel_files:
    raise FileNotFoundError("No se encontraron archivos de Excel en la carpeta 'assets'.")

# Tomar el primer archivo de Excel encontrado
excel_file = os.path.join(input_folder, excel_files[0])

# Asegúrate de que la carpeta de salida exista
os.makedirs(output_folder, exist_ok=True)

# Cargar el archivo de Excel
xls = pd.ExcelFile(excel_file)

# Iterar sobre cada hoja y guardarla como un nuevo archivo
for sheet_name in xls.sheet_names:
    # Leer la hoja
    df = pd.read_excel(xls, sheet_name=sheet_name)
    
    # Guardar la hoja en un nuevo archivo Excel en la carpeta de salida
    output_file = os.path.join(output_folder, f'{sheet_name}.xlsx')
    df.to_excel(output_file, index=False)

    print(f'Hoja "{sheet_name}" guardada en el archivo "{output_file}".')