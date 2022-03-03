
import socket
import json

HOST="127.0.0.1"
PORT=22003

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST,PORT))
    while True:
        stringa=input('Inserire la stringa, "0" per uscire: ')
        messaggio={
            'stringa': stringa
        }
        messaggio=json.dumps(messaggio) #trasforma l'oggetto in  stringa
        s.sendall(messaggio.encode("UTF-8"))
        data=s.recv(1024)
        if stringa=="0":
            print(data.decode())
            break
        else:
            print("Stringa modificata: ", data.decode())
