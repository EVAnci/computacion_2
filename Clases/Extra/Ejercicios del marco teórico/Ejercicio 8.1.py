# Enunciado: Crea dos listas diferentes pero con el mismo contenido. Imprime sus direcciones de memoria y verifica si son iguales o distintas.

list_1 = ['hola', 1, True]
list_2 = ['hola', 1, True]
list_3 = list_1

print(f'Lista 1: {list_1} -> ID: {id(list_1)}\nLista 2: {list_2} -> ID: {id(list_2)}')
print(f'list_1 == list_2: {list_1 == list_2}')
print(f'list_1 is list_2: {list_1 is list_2}\n')

print(f'Lista 1: {list_1} -> ID: {id(list_1)}\nLista 3: {list_3} -> ID: {id(list_3)}')
print(f'list_1 == list_3: {list_1 == list_3}')
print(f'list_1 is list_3: {list_1 is list_3}')
