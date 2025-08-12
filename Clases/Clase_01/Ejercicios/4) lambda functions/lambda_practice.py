if __name__ == '__main__':
    odd = lambda number: number*2 if number%2 != 0 else number
    number = int(input('Ingrese un numero para convertirlo en par: '))
    print(odd(number))