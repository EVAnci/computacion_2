from multiprocessing import Process, Pipe, Queue
from src.analizador import analizar
from src.generador import generar
from src.verificador import verificar
from args import set_args

if __name__ == "__main__":
    
    args = set_args()
    print(f'[+] Modo verboso: {"Activo" if args.verbose else "Inactivo"} - Datos a generar: {args.num} datos.')

    gen_a, frec_pipe = Pipe()
    gen_b, pres_pipe = Pipe()
    gen_c, oxig_pipe = Pipe()

    n = args.num
    
    gen = Process(target=generar, args=(n,gen_a,gen_b,gen_c,args.verbose))
 
    q = Queue()

    a = Process(target=analizar, args=('frecuencia',frec_pipe,q,n,args.verbose))
    b = Process(target=analizar, args=('presion',pres_pipe,q,n,args.verbose))
    c = Process(target=analizar, args=('oxigeno',oxig_pipe,q,n,args.verbose))


    gen.start()
    a.start()
    b.start()
    c.start()

    gen.join()
    a.join()
    b.join()
    c.join()

    total_resultados = args.num * 3  # Frecuencia, presión, oxígeno
    verificador = Process(target=verificar ,args=(q,total_resultados))
    verificador.start()
    verificador.join()

    # while not q.empty():
    #     print(q.get())
