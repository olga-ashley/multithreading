import multiprocessing as multipro
import time
import random
semaphore:None

def init(sem):
    global semaphore
    semaphore =sem

def corredor(id):
    global semaphore
    par_espera:float=0.1
    andar(id,par_espera)
    with semaphore:
        porta(id,par_espera)

def andar(id,espera):
    distancia:int=0
    velocidade:int=0
    final=200

    while (distancia<final):
        velocidade=int((random.randint(4000,6000))/1000)
        distancia=distancia+velocidade
        print('Pessoa',id,'percorreu',distancia,'metros.')
        time.sleep(espera)

def porta(id,espera):
    print('Pessoa',id,'está abrindo a porta.')
    timer=int(random.randint(10000,20000)/10000)
    recebe_e=timer*espera
    time.sleep(espera)
    print('Pessoa',id,'passou pela porta.')

def main():
    parametros:int=[0]*4
    sem= None

    for i in range(0,4):
        parametros[i]=i+1

    with multipro.Manager() as gerenciador:
        sem=gerenciador.Semaphore(1)
        with multipro.Pool(processes=4, initializer=init, initargs=(sem,)) as threads:
            threads.map(corredor,parametros)
if __name__ == '__main__':
    main()