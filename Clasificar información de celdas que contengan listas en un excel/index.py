import pandas as pd
import numpy as np

data = './Clasificar información de celdas que contengan listas en un excel/assets/input.xlsx'
out = './Clasificar información de celdas que contengan listas en un excel/out/output.txt'

def bubble_sort_tuplas(lista_de_tuplas):
    n = len(lista_de_tuplas)

    #Iteración sobre el tamaño de la lista
    for i in range(n):
        # Últimos i elementos ya están ordenados, no necesitamos compararlos
        for j in range(0, n - i - 1):
            # Comparamos los segundos elementos de las tuplas
            if lista_de_tuplas[j][1] < lista_de_tuplas[j + 1][1]:
                # Hacemos swap si el segundo elemento está en el orden incorrecto
                lista_de_tuplas[j], lista_de_tuplas[j + 1] = lista_de_tuplas[j + 1], lista_de_tuplas[j]


def moda(data,out):
    #Nombre de la columna
    #name = input("Nombre de la columna: ")
    name = 'Carreras solicitadas'

    #Apertura del archivo
    df_input = pd.read_excel(data,header=0)

    #Diccionario de las carreras
    carreras = {}
    
    #Recorrer todas las filas extrayendo la cantidad de veces que aparecen las carreras
    for i in range(len(df_input)):
        ROW = df_input.iloc[i]
        CARRERAS = ROW[name]

        #Si la celda no contiene un nan
        if not pd.isna(CARRERAS):
            VALORES = CARRERAS.split(', ')
            #Rellenar el diccionario con la moda de las carreras
            for j in VALORES:
                if j in carreras:
                    carreras[j] = carreras[j] + 1
                else:
                    carreras[j] = 1

    #Convertir diccionario en lista de tuplas
    carreras = list(carreras.items())

    bubble_sort_tuplas(carreras)

    with open(out, 'a') as output:
        for i in range(len(carreras)):
            output.write(carreras[i][0]+": "+str(carreras[i][1])+"\n")

moda(data,out)