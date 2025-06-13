from multiprocessing import Process, Pipe, Queue
from src.analizador import analizar
from src.generador import generar

if __name__ == "__main__":
    gen_a, frec_pipe = Pipe()
    gen_b, pres_pipe = Pipe()
    gen_c, oxig_pipe = Pipe()

    n = 4 #Automatizar, esta mal hardcodear
    
    gen = Process(target=generar, args=(n,gen_a,gen_b,gen_c))
 
    q = Queue()

    a = Process(target=analizar, args=('frecuencia',frec_pipe,q,n))
    b = Process(target=analizar, args=('presion',pres_pipe,q,n))
    c = Process(target=analizar, args=('oxigeno',oxig_pipe,q,n))

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
