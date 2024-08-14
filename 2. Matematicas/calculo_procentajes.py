#Esto es una prueba

def calcular_porcentaje(numero, total):
    try:
        porcentaje = (numero / total) * 100
        return porcentaje
    except ZeroDivisionError:
        return "El denominador no puede ser cero"

while True:
    total = float(input("Ingrese el número que representa el 100%: "))
    
    numero = float(input("Ingrese el número para calcular el porcentaje: "))
    
    resultado = calcular_porcentaje(numero, total)
    print(f"{numero} representa el {resultado}% de {total}.")

