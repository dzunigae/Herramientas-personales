import pandas as pd
import os
import re

# Ruta de la carpeta pdfs_unificados
RUTA_PDFS_UNIFICADOS = "./pdfs_unificados"

# Ruta de la carpeta Organización de hojas de vida
RUTA_HOJAS_DE_VIDA = "./Organización Hojas de vida empresas"

#Dataframe curriculums
DF_CURRICULUMS = pd.read_excel('./assets/Curriculums_out.xlsx')

#Dataframe convocatorias
DF_CONVOCATORIAS = pd.read_excel('./assets/Hoja de Nuevas Convocatorias.xlsx')

#Dataframe del reporte
DF_REPORTE = pd.DataFrame(columns=['Nombre',
                                   'Documento',
                                   'Correo EST',
                                   'Tipo de admisión',
                                   'Facultad',
                                   'Empresa',
                                   'Correo EMP',
                                   'Programas requeridos'])

#Diccionario con las hojas de vida por estudiante
PARES_CC_CV = dict()

#Diccionario con los números de convocatorias a las que se han postulado
PARES_CC_CONVOCATORIAS = dict()

#Set con claves(CC) ya revisadas para el reporte
CC_REVISADAS = set()

#Recorremos la información de los estudiantes
for index, row in DF_CURRICULUMS.iterrows():
    CC = row['Número de documento de identidad']
    CV = row['CV'].replace(" - Google Drive", "")
    #Lista que contiene los archivos que empatan con el CV del estudiante
    LIST_ARCHIVOS = set()
    # Recorrer los archivos en la carpeta pdfs_unificados
    for archivo in os.listdir(RUTA_PDFS_UNIFICADOS):
        # Convertir ambos nombres en conjuntos de palabras
        CV_SET = set(re.split(r'[ .]+', CV.lower()))
        CV_SET.discard('')
        ARCHIVO_SET = set(re.split(r'[ .]+', archivo.lower()))
        ARCHIVO_SET.discard('')
        if ARCHIVO_SET.issubset(CV_SET):
            LIST_ARCHIVOS.add(archivo)
    
    if CC in PARES_CC_CV:
        PARES_CC_CV[CC].update(LIST_ARCHIVOS)
    else:
        PARES_CC_CV[CC] = LIST_ARCHIVOS

#Recorremos el diccionario con las CV para extraer las convocatorias
for clave, valor in PARES_CC_CV.items():
    if len(valor) != 0:
        PARES_CC_CONVOCATORIAS[clave] = set()
        #Recorremos el set que posee los nombres de los archivos con las hojas de vida
        for elemento in valor:
            for carpeta in os.listdir(RUTA_HOJAS_DE_VIDA):
                ruta_carpeta = os.path.join(RUTA_HOJAS_DE_VIDA, carpeta)
                # Verificar si es un directorio
                if os.path.isdir(ruta_carpeta):
                    # Recorrer los archivos en la carpeta
                    for arch in os.listdir(ruta_carpeta):
                        # Verificar si el archivo está en la lista de nombres de PDFs
                        if arch == elemento:
                            PARES_CC_CONVOCATORIAS[clave].add(carpeta)

#Realización del reporte
for clave in PARES_CC_CONVOCATORIAS:
    if clave not in CC_REVISADAS:
        CC_REVISADAS.add(clave)
        DOCUMENTO = clave
        #Nos quedamos con las versiones más largas de los datos
        DF_CURRICULUMS_POR_DOCUMENTO = DF_CURRICULUMS[DF_CURRICULUMS['Número de documento de identidad'] == clave]
        NOMBRE = DF_CURRICULUMS_POR_DOCUMENTO['Nombres y apellidos'].loc[DF_CURRICULUMS_POR_DOCUMENTO['Nombres y apellidos'].str.len().idxmax()]
        CORREO_EST = DF_CURRICULUMS_POR_DOCUMENTO['Dirección de correo electrónico'].loc[DF_CURRICULUMS_POR_DOCUMENTO['Dirección de correo electrónico'].str.len().idxmax()]
        ADMISION = DF_CURRICULUMS_POR_DOCUMENTO['Tipo de admisión'].loc[DF_CURRICULUMS_POR_DOCUMENTO['Tipo de admisión'].str.len().idxmax()]
        FACULTAD = DF_CURRICULUMS_POR_DOCUMENTO['Programa al que pertenece'].loc[DF_CURRICULUMS_POR_DOCUMENTO['Programa al que pertenece'].str.len().idxmax()]
        for conv in PARES_CC_CONVOCATORIAS[clave]:
            ID_DATAFRAME_CONVOCATORIAS = int(conv)-2
            EMPRESA = DF_CONVOCATORIAS.at[ID_DATAFRAME_CONVOCATORIAS,'1. Nombre de la entidad']
            CORREO_EMP = DF_CONVOCATORIAS.at[ID_DATAFRAME_CONVOCATORIAS,'3. Correo electrónico']
            P_REQUERIDOS = DF_CONVOCATORIAS.at[ID_DATAFRAME_CONVOCATORIAS,'5. Programas académicos requeridos']
            new_row = pd.DataFrame({
                'Nombre':[NOMBRE],
                'Documento':[DOCUMENTO],
                'Correo EST':[CORREO_EST],
                'Tipo de admisión':[ADMISION],
                'Facultad':[FACULTAD],
                'Empresa':[EMPRESA],
                'Correo EMP':[CORREO_EMP],
                'Programas requeridos':[P_REQUERIDOS]
            })
            # Usar _append para añadir la nueva fila
            DF_REPORTE = DF_REPORTE._append(new_row, ignore_index=True)

#Generación del reporte
DF_REPORTE.to_excel('./out/Reporte.xlsx', index=False)