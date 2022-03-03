#calcolatrice client per calcoServer.py versione multithread
#Di Lorenzo Alessandro
import socket
import sys
import random
import os
import time
import threading
import multiprocessing
import json

SERVER_ADDRESS = '127.0.0.1'
SERVER_PORT = 22003
NUM_WORKERS=2

def genera_richieste(num,address,port):
    start_time_thread= time.time()
    try:
        s=socket.socket()
        s.connect((address,port))
        print(f"\n{threading.current_thread().name} {num+1}) Connessione al server: {address}:{port}")
    except:
        print(f"{threading.current_thread().name} Qualcosa è andato storto, sto uscendo... \n")
        sys.exit()
    #1. rimpiazzare questa parte con la generazione di operazioni e numeri random, non vogliamo inviare sempre 3+5 
    primoNumero=random.randint(0,100)#generiamo dei numeri casuali da 0 a 100
    operazione=""
    secondoNumero=random.randint(0,100)#generiamo dei numeri casuali da 0 a 100
    operaNum=random.randint(0,4)#assegnamo dei valori da 0 a 5 per far generare poi in modo casuale che operazione
    #dovrà essere svolta
    if(operaNum==0):
        operazione="+"
        ris=primoNumero+secondoNumero
    elif(operaNum==1):
        operazione="-"
        ris=primoNumero-secondoNumero
    elif(operaNum==2):
        operazione="*"
        ris=primoNumero*secondoNumero
    elif(operaNum==3):
        operazione="/"
        ris=primoNumero/secondoNumero
    else:
        operazione="%"
        ris=primoNumero%secondoNumero
    
    print(f"il primo numero è:{primoNumero},l'operazione è:{operazione},il secondo numero è:{secondoNumero},il risultato è:{ris}")
    #stampiamo il risultato della generazione casuale dei numeri e dell operazione
    #2. comporre il messaggio, inviarlo come json e ricevere il risultato
    messaggio={
           'primoNumero':primoNumero, 
           'operazione':operazione, 
           'secondoNumero':secondoNumero
       }
    messaggio=json.dumps(messaggio) 
    s.sendall(messaggio.encode("UTF-8"))
    data=s.recv(1024)
    if not messaggio:
        print(f"{threading.current_thread().name}: Server non risponde. Exit")
    else:
        print(f"{threading.current_thread().name}: Risultato: {data.decode()}") # trasforma il vettore di byte in stringa
    s.close()
    end_time_thread=time.time()
    print(f"{threading.current_thread().name} tempo di esecuzione time=", end_time_thread-start_time_thread)

if __name__ == '__main__':
    start_time=time.time()
    # 3 ciclo per chiamare NUM_WORKERS volte la funzione genera richieste alla quale passo i parametri (num,SERVER_ADDRESS, SERVER_PORT)
    for num in range(NUM_WORKERS):
        genera_richieste(num,SERVER_ADDRESS,SERVER_PORT)
    end_time=time.time()
    print("Total SERIAL time=", end_time - start_time)
     
    start_time=time.time()
    threads=[]#creiamo la lista threads
    # 4 ciclo per chiamare NUM_WORKERS volte la funzione genera richieste tramite l'avvio di un thread al quale passo i parametri args=(num,SERVER_ADDRESS, SERVER_PORT,)
    # ad ogni iterazione appendo il thread creato alla lista threads
    for num in (0,NUM_WORKERS):
        threads.append(threading.Thread(target=genera_richieste,args=(num,SERVER_ADDRESS, SERVER_PORT)))

    # 5 avvio tutti i thread
    for i in range (len(threads)):#creimo un ciclo for per applicare lo start a tutti i thread
        threads[i].start()
    # 6 aspetto la fine di tutti i thread 
    for i in range (len(threads)):#creimo un ciclo for per applicare il join a tutti i thread
        threads[i].join()

    end_time=time.time()
    print("Total THREADS time= ", end_time - start_time)
 
    start_time=time.time()
    process=[]#creiamo la lista process
    # 7 ciclo per chiamare NUM_WORKERS volte la funzione genera richieste tramite l'avvio di un processo al quale passo i parametri args=(num,SERVER_ADDRESS, SERVER_PORT,)
    # ad ogni iterazione appendo il thread creato alla lista threads
    for num in range(0,NUM_WORKERS):
        threads.append(threading.Thread(args=(num,SERVER_ADDRESS, SERVER_PORT)))

    # 8 avvio tutti i processi
    for num in range(0,NUM_WORKERS):
        process.append(multiprocessing.Process(target=genera_richieste,args=(num,SERVER_ADDRESS, SERVER_PORT)))

    for i in range (0,NUM_WORKERS):#creiamo un ciclo for per fare in modo che i processi avvenganno tutti
        process[i].start()
    # 9 aspetto la fine di tutti i processi 
    for num in range (0,NUM_WORKERS):#creo un ciclo for per fare in modo che il join avvenga su tutti i thread
        process[num].join()
 
    end_time=time.time()
    print("Total PROCESS time= ", end_time - start_time)
