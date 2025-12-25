import random

def numero_aleatorio(minimo, maximo):
    return random.randint(minimo, maximo)

# Ejemplo de uso
minimo = 0
maximo = 7
aleatorio = numero_aleatorio(minimo, maximo)
print(f"Número: {aleatorio}")
