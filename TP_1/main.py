from multiprocessing import Process, Pipe, Queue
from src.analizador import Analizador
from src.generador import generar

if __name__ == "__main__":
    gen_a, frec_pipe = Pipe()
    gen_b, pres_pipe = Pipe()
    gen_c, oxig_pipe = Pipe()

    n = 4 #Automatizar, esta mal hardcodear
    
    gen = Process(target=generar, args=(n,gen_a,gen_b,gen_c))
 
    q = Queue()
    
    frec_analizer = Analizador('frecuencia',frec_pipe,q)
    pres_analizer = Analizador('presion',pres_pipe,q)
    oxig_analizer = Analizador('oxigeno',oxig_pipe,q)

    a = Process(target=frec_analizer.procesar, args=(n,))
    b = Process(target=pres_analizer.procesar, args=(n,))
    c = Process(target=oxig_analizer.procesar, args=(n,))

    gen.start()
    a.start()
    b.start()
    c.start()

    gen.join()
    a.join()
    b.join()
    c.join()

    while not q.empty():
        print(q.get())
