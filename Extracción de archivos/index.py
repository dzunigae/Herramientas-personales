import os
import shutil

def procesar_carpeta(origen, destino_normal, destino_expecial):
    # Recorrer todos los archivos y subdirectorios en la carpeta de origen
    for raiz, directorios, archivos in os.walk(origen):
        for archivo in archivos:
            #Obtener la ruta del archivo actual
            ruta_archivo = os.path.join(raiz,archivo)
            
            #Verificar si el archivo es multimedia
            if es_multimedia(archivo):
                # Copiar el archivo multimedia al directorio de destino
                shutil.copy(ruta_archivo, destino_normal)
            else:
                nombre_archivo, extension = os.path.splitext(archivo)
                if not extension:
                    shutil.copy(ruta_archivo, destino_expecial)

def es_multimedia(archivo):
    #Lista de extensiones
    extensiones_multimedia = ['.jpg',
                              '.jpeg',
                              '.png',
                              '.gif',
                              '.bmp',
                              '.tiff',
                              '.web',
                              '.mp4',
                              '.avi',
                              '.mkv',
                              '.mov',
                              '.wmv',
                              '.flv']
    return any(archivo.lower().endswith(extension) for extension in extensiones_multimedia)

# Rutas de las carpetas de origen y destino
carpeta_origen = './5. Extracción de archivos/assets/Angelica/'
carpeta_destino_out_normal = './5. Extracción de archivos/out_normal/'
carpeta_destino_out_sin_extension = './5. Extracción de archivos/out_sin_extension/'

procesar_carpeta(carpeta_origen, carpeta_destino_out_normal,carpeta_destino_out_sin_extension)