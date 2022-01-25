import socket
import json


HOST='127.0.0.1'
PORT=65432

with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as s:
    s.bind((HOST,PORT))#indica all host su che porta deve essere in ascolto
    s.listen()
    print("[*] in ascolto su %s:%d"%(HOST,PORT))
    clientsocket, address=s.accept()    #ritorna client socket e address
    with clientsocket as cs:
        print("connessione da ",address)
        while True:
            data=cs.recv(1024)
            if not data:    #se data è un vettore vuoto risulta false
                break
            data=data.decode()
            data=json.loads(data)
            #prendiamo le 3 variabili
            primoNumero=data['primoNumero']
            operazione=data['operazione']
            secondoNumero=data['secondoNumero']
            ris=""
            if operazione=="+":
                ris=primoNumero+secondoNumero
            elif operazione=="-":
                ris=primoNumero-secondoNumero
            elif operazione=="*":
                ris=primoNumero*secondoNumero
            elif operazione=="/":
                if secondoNumero==0:
                    ris="non puoi dividere per 0"
                else:
                    ris=primoNumero/secondoNumero
            elif operazione=="%":
                ris=primoNumero%secondoNumero
            else:
                ris="operazione non riconosciuta"
            ris=str(ris)#trasforma tutto in stringa con un casting
            cs.sendall(ris.encode("UTF-8"))#mandiamo il vettore di byte in risposta al client
#fine parte del server



