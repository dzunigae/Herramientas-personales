def ordenar(archivo_entrada, archivo_salida):
    try:
        # Abrir el archivo de entrada en modo lectura
        with open(archivo_entrada, 'r') as file:
            # Leer todas las líneas del archivo
            lines = file.readlines()

            # Ordenar las líneas alfabéticamente
            lines.sort()

            # Abrir el archivo de salida en modo escritura
            with open(archivo_salida, 'w') as output:
                # Escribir las líneas ordenadas en el archivo de salida
                output.writelines(lines)

        print(f'Se ha ordenado y guardado correctamente en {archivo_salida}')

    except FileNotFoundError:
        print(f'Error: No se encuentra el archivo {archivo_entrada}')

# Nombre del archivo de entrada y salida
archivo_entrada = './3. Ordenar txt/assets/strings.txt'
archivo_salida = './3. Ordenar txt/out/strings_out.txt'

# Llamar a la función para ordenar y guardar
ordenar(archivo_entrada, archivo_salida)
