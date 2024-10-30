def divisores(num, inicio, fin):
    print(f"Divisores de {num} en el rango de {inicio} a {fin}:")
    for i in range(inicio, fin + 1):
        if num % i == 0:
            resultado = num // i
            print(f"{num} ÷ {i} = {resultado}")
        else:
            print(f"{num} no es divisible por {i}")

# Ejemplo de uso
numero = int(input("Ingresa un número: "))
rango_inicio = int(input("Ingresa el inicio del rango: "))
rango_fin = int(input("Ingresa el final del rango: "))

divisores(numero, rango_inicio, rango_fin)