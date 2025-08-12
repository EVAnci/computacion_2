import argparse

def valid_range(value):
    value = int(value)
    if value < 1 or value > 100:
        raise argparse.ArgumentTypeError("El numero debe ser un entero entre 1 y 100")
    return value

def main():
    parser = argparse.ArgumentParser(
        prog="Ejercicio",
        description="Ejercicio propuesto para resolver"
    )

    parser.add_argument(
        "-n",
        "--numbers",
        nargs="+",
        type=valid_range,
        help="Lista de numeros enteros entre 1 y 100"
    )

    parser.add_argument(
        "-m",
        "--mode",
        choices=("fast", "slow", "medium"),
        help="Modo de operación: fast, slow, medium"
    )

    args = parser.parse_args()

    print(f'Números ingresados: {args.numbers}')
    print(f'Modo de operación: {args.mode}')

if __name__ == '__main__':
    main()