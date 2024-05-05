import pandas as pd
import re

# Crear un DataFrame de Pandas vacío que contenga cómo cabeza de columnas: Año, Título, Autores, DOI
DF_ARTICULOS = pd.DataFrame(columns=['Año', 'Título', 'Autores', 'DOI'])

# Crear una lista que contenga cada línea del documento en una posición distinta 
#(Asegurarse de que el caracter salto de línea al final sea eliminado de todas las líneas)
LINEAS = []

with open('./7. Clasificación de artículos/assets/abstract-Epinephelu-set.txt', 'r') as archivo:
    # Leer cada línea del archivo y agregarla a la lista
    for linea in archivo:
        LINEAS.append(linea.strip())

# Crear variable que contenga el último artículo revisado, inicializada en 0
ULTIMO_ARTICULO = 0
# Variable que sea el id para usar en el While, inicializada en 0
i = 0

# Recorrido de la lista a través de un while hasta el tamaño de la lista
while i < len(LINEAS):
    ERROR = False
    # Si la línea comienza con un número, revisar si este es ún valor superior a la variable del último artículo revisado
    LINEA_ACTUAL = LINEAS[i]
    DIVISION_LINEA_ACTUAL = LINEA_ACTUAL.split(' ')
    try:
        ARTICULO_ACTUAL = int(DIVISION_LINEA_ACTUAL[0][:-1])
    except:
        ARTICULO_ACTUAL = ULTIMO_ARTICULO
        ERROR = True
    if ARTICULO_ACTUAL == ULTIMO_ARTICULO + 1 and not ERROR :
        # De ser cierto:
        ULTIMO_ARTICULO = ARTICULO_ACTUAL
        # Dividir el string de la línea utilizando: ;
        DIVISION_LINEA_ACTUAL = LINEA_ACTUAL.split(';')
        # Dividir el primer string resultado del proceso anterior utilizando: .
        DIVISION_LINEA_ACTUAL = DIVISION_LINEA_ACTUAL[0].split('.')
        # Dividir el tercer resultado del proceso anterior utilizando: (espacio)
        DIVISION_LINEA_ACTUAL = DIVISION_LINEA_ACTUAL[2].split(' ')
        # El segundo resultado del proceso anterior será el año del documento
        ano = DIVISION_LINEA_ACTUAL[1]
        # Sumar 2 al id
        i += 2
        LINEA_ACTUAL = LINEAS[i]
        # Mediante While, concatenar en un string todas las líneas siguientes hasta que la línea evaluada esté vacía,
        # este será el Título del documento
        titulo = LINEA_ACTUAL
        i += 1
        while LINEAS[i] != '':
            titulo = titulo + ' ' + LINEAS[i]
            i += 1
        # Sumar 1 al id
        i += 1
        LINEA_ACTUAL = LINEAS[i]
        # Mediante While, concatenar en un string todas las líneas siguientes hasta que la línea evaluada esté vacía,
        # esto serán los Autores del documento
        autores = LINEA_ACTUAL
        i += 1
        while LINEAS[i] != '':
            autores = autores + ' ' + LINEAS[i]
            i += 1
        # A la variable que contiene a los autores, hay que eliminarle todas las subcadenas que cumplan el patrón:
        # (-algo-)
        PATRON = r'\([^)]*\)'
        autores = re.sub(PATRON, '', autores)
        # Mediante While, seguir avanzando en la revisión de líneas hasta encontrar aquella que comience con: DOI:,
        # esto será el DOI del documento
        while LINEAS[i][:4] != 'DOI:':
            i += 1
        DIVISION_LINEA_ACTUAL = LINEAS[i].split()
        doi = DIVISION_LINEA_ACTUAL[1]
        # Añadir un nuevo registro en el DataFrame con los datos ya encontrados
        nuevo_registro = {
            'Año':ano,
            'Título': titulo,
            'Autores': autores, 
            'DOI': doi
        }
        DF_ARTICULOS = DF_ARTICULOS._append(nuevo_registro, ignore_index=True)
        # Sumar 1 al id
        i += 1
    else:
        # De no ser cierto:
        # Sumar 1 al id
        i += 1

# Crear finalmente el excel con la información del DataFrame
DF_ARTICULOS.to_excel('./7. Clasificación de artículos/out/datos.xlsx', index=False)