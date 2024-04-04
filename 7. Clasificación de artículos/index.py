import pandas as pd
import re

RUTA = './7. Clasificación de artículos/assets/abstracts.txt'

DATAFRAME = {
    'Nombre':[],
    'Autores':[],
    'DOI':[]
}

lineas = []

def organizacion(RUTA):
    articulo_actual = 0

    with open(RUTA, 'r') as archivo:
        for linea in archivo:
            lineas.append(linea)
    
    i = 0

    while i < len(lineas):
        actual = lineas[i]
        j = 0
        digito_s = ""
        if actual[j].isdigit():
            digito_s = digito_s + actual[j]
            j = j + 1
            while True:
                if actual[j].isdigit():
                    digito_s = digito_s + actual[j]
                    j = j + 1
                elif actual[j] == '.':
                    break
            digito_n = int(digito_s)
            if digito_n > articulo_actual:
                articulo_actual = digito_n
                i = i + 1
                while lineas[i] != "":
                    i = i + 1
                i = i + 1
                


organizacion(RUTA)