from multiprocessing import Process, Pipe, Queue, Value, Condition, Event
from src.analizador import analizar
from src.generador import generar
from src.verificador import verificar
from args import set_args

if __name__ == "__main__":
    args = set_args()
    
    print(f'[+] Modo verboso: {"Activo" if args.verbose else "Inactivo"} - Datos a generar: {args.num} datos.')
    
    n = args.num
    q = Queue()
    done_count = Value('i', 0)
    cond = Condition()

    pipes = [Pipe(duplex=False) for _ in range(3)]
    generador_pipes = [p[1] for p in pipes]
    analizador_pipes = [p[0] for p in pipes]

    gen = Process(target=generar, args=(n,generador_pipes,args.verbose), name='Generador')
    tipos = ('frecuencia', 'presion', 'oxigeno')
    proc_analizadores = [
        Process(target=analizar, args=(tipos[i], analizador_pipes[i], q, n, done_count, cond, 3, args.verbose), name=f"Analizador-{tipos[i]}") for i in range(3)
    ]

    gen.start()
    for p in proc_analizadores:
        p.start()
 
    gen.join()
    for p in proc_analizadores:
        p.join()

    total_resultados = args.num * 3  # Frecuencia, presión, oxígeno
    verificador = Process(target=verificar ,args=(q,total_resultados))
    verificador.start()
    verificador.join()

    # while not q.empty():
    #     print(q.get())
