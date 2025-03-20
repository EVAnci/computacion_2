import sys
import getopt

def main(argv):
    input_file = ''
    output_file = ''
    
    try:
        opts, args = getopt.getopt(argv, "hi:o:", ["help", "input=", "output="])
        print(f'Opciones: {opts}')
        print(f'Argumentos: {args}')
    except getopt.GetoptError:
        print('Uso: script.py -i <inputfile> -o <outputfile>')
        sys.exit(2) # usamos el código de salida erroneo (stderr)
    
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            print('Uso: script.py -i <inputfile> -o <outputfile>')
            sys.exit()
        elif opt in ("-i", "--input"):
            input_file = arg
        elif opt in ("-o", "--output"):
            output_file = arg

    print(f"Archivo de entrada: {input_file}")
    print(f"Archivo de salida: {output_file}")

if __name__ == "__main__":
    # Le pasamos la lista con todos los argumentos recibidos a la función main
    # menos el nombre o ruta del script (primer elemento en `sys.argv`)
    main(sys.argv[1:])