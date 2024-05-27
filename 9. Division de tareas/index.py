import pandas as pd
import os

RUTA = './9. Division de tareas/Tareas.xlsx'

PUNTAJE_MAXIMO = 0

valores = {
    'Daniel': 0,
    'David': 0,
    'Gabriel': 0,
    'Sergio': 10,
    'Yeison': 0
}

valores_a_eliminar = [2,3,4,7,8,10]

def division(ruta):
    global PUNTAJE_MAXIMO
    df = pd.read_excel(ruta)
    
    # Calculo del puntaje máximo
    for i in range(len(df)):
        fila_actual = df.loc[i]
        estudiantes = fila_actual['Numero de estudiantes']
        dificultad = fila_actual['Dificultad']
        
        # Verificar si hay NaN en los datos y manejarlos
        if pd.isna(estudiantes) or pd.isna(dificultad):
            continue  # Saltar esta iteración si hay datos faltantes
        
        PUNTAJE_MAXIMO += estudiantes * (dificultad + 1)

    # Eliminar las lineas con las tareas que ya han sido hechas
    df_filtrado = df[~df['Tareas'].isin(valores_a_eliminar)].reset_index(drop=True)

    # Asegurarse de que las columnas correspondientes puedan contener strings
    for persona in valores.keys():
        df_filtrado[persona] = ''

    # Asignar tareas
    for i in range(len(df_filtrado)):
        fila_actual = df_filtrado.loc[i]
        estudiantes = fila_actual['Numero de estudiantes']
        dificultad = fila_actual['Dificultad']

        puntaje = estudiantes * (dificultad + 1)

        persona_menor_valor = min(valores, key=valores.get)

        df_filtrado.at[i, persona_menor_valor] = 'x'

        valores[persona_menor_valor] += puntaje

    print(valores)

    # Guardar el DataFrame filtrado en un nuevo archivo Excel
    directorio, nombre_archivo = os.path.split(ruta)
    nuevo_archivo = os.path.join(directorio, 'Tareas_filtrado.xlsx')
    df_filtrado.to_excel(nuevo_archivo, index=False)

division(RUTA)