import multiprocessing as multipro
import time
import random
semaphore:None

def init(sem):
    global semaphore
    semaphore =sem

def carro(id):
    global semaphore
    carro_andar(id)
    with semaphore:
        cruzamento(id)

def carro_andar(id):
    distancia:int=0
    velocidade:int=0
    espera:float=0.1
    final=100

    while (distancia<final):
        velocidade=int((random.randint(100,8000))/100)
        distancia=distancia+velocidade
        print('Carro',id,'percorreu',distancia,'metros.')
        time.sleep(espera)

def cruzamento(id):
    sentido=['','Direita','Esquerda','Cima','Baixo']

    if id==1 or id==2:
        print('O carro vindo da',sentido[id],'cruzou.')
    elif id==3 or id==4:
        print('O carro vindo de',sentido[id],'cruzou.')

def main():
    parametros:int=[0]*4
    sem= None

    for i in range(0,4):
        parametros[i]=i+1

    with multipro.Manager() as gerenciador:
        sem=gerenciador.Semaphore(1)
        with multipro.Pool(processes=4, initializer=init, initargs=(sem,)) as threads:
            threads.map(carro,parametros)
if __name__ == '__main__':
    main()