import argparse

def main():
    parser = argparse.ArgumentParser(
        prog='Prueba de argparse',
        description="Ejemplo de uso de argparse"
    )
    
    parser.add_argument("-i", "--input", type=str, required=True, help="Archivo de entrada")
    parser.add_argument("-o", "--output", type=str, required=True, help="Archivo de salida")
    parser.add_argument("-v", "--verbose", action="store_true", help="Modo verboso")
    parser.add_argument("-n", "--number", type=int, help="Número entero")

    args = parser.parse_args()

    print(f"Modo verboso: {'Activo' if args.verbose else 'Inactivo'}")
    if args.verbose:
        print(f"Número entero: {args.number}")
    print(f"Archivo de entrada: {args.input}")
    print(f"Archivo de salida: {args.output}")

if __name__ == "__main__":
    main()