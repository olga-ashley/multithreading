import multiprocessing as multipro
import time
import random

def init(sem,pos,col):
    global semaphore, posicao, colocacao
    semaphore = sem
    posicao = pos
    colocacao = col

def sapo(id):
    global semaphore, posicao
    correr(id)
    with semaphore:
        chegada(id)

def correr(id):
    distancia:int=0
    velocidade:int=0
    final=200
    espera:float=0.1

    while (distancia<final):
        velocidade=int((random.randint(4000,6000))/1000)
        distancia+=velocidade
        print('Sapo',id,'pulou',velocidade,'cm e percorreu',distancia,'cm.')
        time.sleep(espera)

def chegada(id):
    localpos=posicao.value
    colocacao[localpos]=id
    posicao.value+=1
    print('Sapo',id,'chegou em '+str(localpos+1)+'o lugar.')

def main():
    parametros:int=[0]*5
    sem= None
    posicao = multipro.Value('i', 0)
    colocacao=multipro.Array('i', [0]*5)

    for i in range(0,5):
        parametros[i]=i+1

    with multipro.Manager() as gerenciador:
        sem=gerenciador.Semaphore(1)
        with multipro.Pool(processes=5, initializer=init, initargs=(sem,posicao,colocacao)) as threads:
            threads.map(sapo,parametros)
    for i in range(5):
            print(f'{i+1}o lugar - Sapo {colocacao[i]}.')
    
if __name__ == '__main__':
    main()