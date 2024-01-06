import pandas as pd

data = './Clasificar información de celdas que contengan listas en un excel/assets/input.xlsx'
out = './Clasificar información de celdas que contengan listas en un excel/out/output.txt'
excel = './Clasificar información de celdas que contengan listas en un excel/out/output.xlsx'

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


def moda(data,out,excel):
    #Nombre de la columna
    name = input("Nombre de la columna: ")

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
    touples_list = list(carreras.items())

    #Ordenar de mayor a menor las frecuencias
    bubble_sort_tuplas(touples_list)

    #Reporte formato txt
    with open(out, 'a') as output:
        for i in range(len(touples_list)):
            output.write(touples_list[i][0]+": "+str(touples_list[i][1])+"\n")

    #Convertir el diccionario en un data frame
    keys = list(carreras.keys())
    values = list(carreras.values())

    #Reporte a excel
    df_reporte_excel = pd.DataFrame(list(zip(keys,values)), columns=['Carrera','Frecuencia'])
    df_reporte_excel.to_excel(excel,index=False)

moda(data,out,excel)