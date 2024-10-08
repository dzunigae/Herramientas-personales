import pandas as pd

# Cargar los archivos Excel
reporte = pd.read_excel('./assets/Reporte.xlsx')  # Archivo con la columna 'Empresa'
empresas = pd.read_excel('./assets/Hoja de Nuevas Convocatorias.xlsx')  # Archivo con la columna '1. Nombre de la entidad' y '2. Sector de la entidad'

# Hacer el merge de los dos dataframes, utilizando como clave la columna 'Empresa' y '1. Nombre de la entidad'
resultado = pd.merge(reporte, empresas[['1. Nombre de la entidad', '2. Sector de la entidad']], 
                     left_on='Empresa', right_on='1. Nombre de la entidad', 
                     how='left')

# Eliminar la columna '1. Nombre de la entidad' ya que es redundante
resultado.drop(columns=['1. Nombre de la entidad'], inplace=True)

# Guardar el resultado en un nuevo archivo Excel
resultado.to_excel('./out/nuevo_reporte.xlsx', index=False)
