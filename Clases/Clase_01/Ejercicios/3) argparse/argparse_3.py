import argparse

def valid_range(n):
    n = int(n)
    if n < 10 or n > 50:
        raise argparse.ArgumentTypeError("Debes elegir un valor entre 10 y 50")
    return n

# Mi implementación tiene un pequeño detalle. Si un archivo cualquiera contiene txt en su nombre
# se considerará válido (por ejemplo: txt.py).

# def txt_file(f):
#     if not('.txt' in f):
#         raise argparse.ArgumentTypeError("El archivo debe tener extensión txt")
#     open(f,"r")

# La solución sugerida por chatgpt a este problema es la siguiente:
def txt_file(f):
    if not f.endswith('.txt'):
        raise argparse.ArgumentTypeError("El archivo debe tener extensión .txt")
    return f  # No es necesario abrirlo aquí, solo validar


def main():
    parser = argparse.ArgumentParser(
        prog="argparse_3",
        description="Ejercicio número 3 de argparse"
    )

    parser.add_argument(
        "--archivo",
        type=txt_file,
        nargs="+",
        help="Archivo de entrada con extensión txt"
    )

    parser.add_argument(
        "--modo",
        choices=["rapido","normal","lento"],
        help="Seleccione el modo de operación"
    )

    parser.add_argument(
        "--valores",
        type=valid_range,
        nargs="+",
        help="Introducir un valor entero de 10 a 50"
    )

    args = parser.parse_args()

    print(f'Archivos: {args.archivo} (nombres de archivos)')
    print(f'Modo de operación: {args.modo}')
    print(f'Lista de valores: {args.valores}')

if __name__ == '__main__':
    main()