import pandas as pd

def eliminar_filas_duplicadas(archivo_entrada, archivo_salida):
    # Leer el archivo Excel omitiendo las primeras 2 filas (el encabezado está en la fila 3)
    df = pd.read_excel(archivo_entrada, header=0)

    # Eliminar filas duplicadas
    #df_sin_duplicados = df.drop_duplicates(subset=['NOMBRE_ENTIDAD', 'ID_DE_LA_CONVOCATORIA', 'CC_ESTUDIANTE_QUE_APLICO'])
    #df_sin_duplicados = df.drop_duplicates(subset=['NAME'])
    df_sin_duplicados = df.drop_duplicates()

    # Guardar el resultado en un nuevo archivo Excel
    df_sin_duplicados.to_excel(archivo_salida, index=False)

    print("Filas duplicadas eliminadas correctamente.")

# Reemplaza "archivo_entrada.xlsx" y "archivo_salida.xlsx" con los nombres de tus archivos
eliminar_filas_duplicadas("entrada.xlsx", "salida.xlsx")
