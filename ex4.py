import multiprocessing as mpro
import time
import random
def criarTempoMin(num):
    min= num // 60
    seg= num % 60
    tempoStr=f'{min}:{seg:02d}'
    return tempoStr

def init(sems,msem,equi,res):
    global semaphores, masterSem, Equipe, resultado
    
    semaphores=sems
    masterSem=msem
    Equipe=equi
    resultado = res

def carro(id):
    global semaphores,masterSem, Equipe
    
    semid=Equipe[id-1]
    
    with semaphores[semid]:
        with masterSem:
            correr(id)

def correr(id):
    global Equipe
    global resultado
    
    voltas:int=0
    tempoVolta:int=0
    tempoTotal:int=0
    espera:float=0.1
    mostrarVolta:str=''
    mostrarTotal:str=''
    
    print('Carro',id,'da equipe',(1+Equipe[id-1]),'começou a corrida.')

    while (voltas<3):
        voltas+=1
        tempoVolta = random.randint(70, 185)
        mostrarVolta=criarTempoMin(tempoVolta) 
        tempoTotal+=tempoVolta
        print('Carro',id,'completou a volta',voltas,'em',mostrarVolta)
        time.sleep(espera)
    
    mostrarTotal = criarTempoMin(tempoTotal)
    print('Carro', id,'da equipe',(1+Equipe[id-1]),'Terminou em',mostrarTotal)
    
    resultado[id-1]=round(tempoTotal/3)




def main():
    parametros:int=[0]*14
    resultados=mpro.Array('i', [0]*14)
    for i in range(14):
        parametros[i]=i+1
    equipes:str=['']*14
    j=0
    for i in range(0,14,2):
        equipes[i],equipes[i+1]=j,j
        j+=1


    with mpro.Manager() as ger:
        sems=[mpro.Semaphore(1) for e in range(7)]
        msem=mpro.Semaphore(5)
        with mpro.Pool(processes=14, initializer=init, initargs=(sems,msem,equipes,resultados)) as threads:
            threads.map(carro,parametros)
    
    print('Resultados:')
    c=1
    for e in resultados:

        mostrarMedia=criarTempoMin(e)
        print('Carro',c,'da equipe',(1+equipes[c-1]),'teve média de',mostrarMedia)
        c+=1






    
if __name__ == '__main__':
    main()