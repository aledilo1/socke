import socket
import json
HOST="127.0.0.1"
PORT=22003

with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as s:
#af_inet indica il protocollo che viene utilizzato
#sock_stream indica che tipo di connessione è
    s.connect((HOST,PORT))
    while True:
        primoNumero=input("inserisci il primo numero. exit() per uscire")
        if primoNumero=="exit()":
            break
        primoNumero=float(primoNumero)
        operazione=input("inserisci l operazione (+,-,*,/,%)")
        secondoNumero=float(input("inserisci secondo numero"))
        messaggio={'primoNumero':primoNumero,'operazione':operazione,'secondoNumero':secondoNumero}
        messaggio=json.dumps(messaggio)   #trasformiamo l oggetto in stringa
        s.sendall(messaggio.encode("UTF-8"))#sendall invia il vettore di byte
        #encode traforma la stringa in vettore di byte
        #utf-8 è la famiglia dei caratteri
        data=s.recv(1024)#numero massimo di byte che il server puo inviare
        print("Risultato: ",data.decode())#decode trasforma il vettore di byte in  stringa
#fine parte del client