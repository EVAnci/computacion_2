#Enunciado: Diseña una función modificar_elemento que reciba una lista y cambie su primer elemento a 999. Prueba luego con una tupla y explica qué sucede.

def modificar_elemento(lista):
    lista[0] = 999

# Envio de lista
lista = ['Hola', 'mundo', 11]
print(f'Lista antes de la modificación: {lista}')

modificar_elemento(lista)
print(f'Lista despues de la modificación: {lista}\n')

# Prueba con tupla
tupla = ('Hola', 'mundo', 11)
print(f'Lista antes de la modificación: {tupla}')

modificar_elemento(tupla)
print(f'Lista despues de la modificación: {tupla}\n')

# Lo que sucede es el siguiente error:

# Traceback (most recent call last):
#   File "/run/media/elio/Datos/Devices/Linux User/home/Documentos/UM/4to/Computación 2/mi_repositorio/Clases/Extra/Ejercicio 8.2.py", line 17, in <module>
#     modificar_elemento(tupla)
#     ~~~~~~~~~~~~~~~~~~^^^^^^^
#   File "/run/media/elio/Datos/Devices/Linux User/home/Documentos/UM/4to/Computación 2/mi_repositorio/Clases/Extra/Ejercicio 8.2.py", line 4, in modificar_elemento
#     lista[0] = 999
#     ~~~~~^^^
# TypeError: 'tuple' object does not support item assignment

# El error es claro, nos dice que la tupla no permite asignación, esto es porque es un objeto inmutable. Como está almacenado en el heap, deberíamos crear un objeto
# exactamente igual en el heap con el valor cambiado.