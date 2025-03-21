# Enunciado: Crea un objeto en Python, obtén su id() y, usando ctypes, recupera una referencia al mismo. Luego, elimina la referencia original y verifica qué ocurre si intentas seguir utilizando la dirección.

import ctypes

class Node():
    def __init__(self, node_id, pointer, parent):
        self._id = node_id
        self._pointer = pointer
        self._parent = parent 

    def __repr__(self):
        return f'\nNode: {self._id}\nPointer: {self._pointer._id if self._pointer != None else None}\nParent: {self._parent._id if self._parent != None else None}\n'

node_a = Node('Node A', None, None)
node_b = Node('Node B', None, node_a)
node_a._pointer = node_b

print(f'Estado del Nodo A antes de crear la nueva referencia: {node_a}')

copy_of_node_a = ctypes.cast(id(node_a), ctypes.py_object).value

print(f'Estado del Nodo A despues de crear la nueva referencia: {node_a}')

del node_a

print(f'Estado de la referencia nueva al Nodo A despues de crear la nueva referencia: {copy_of_node_a}')