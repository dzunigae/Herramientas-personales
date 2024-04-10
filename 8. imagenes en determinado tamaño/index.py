import sys

sys.set_int_max_str_digits(10000000)

resultado = 256**(1024*1024*3)

with open('./8. imagenes en determinado tamaño/resultado.txt', 'w') as archivo:
    archivo.write(str(resultado))

print("El número se ha guardado en 'resultado.txt'")