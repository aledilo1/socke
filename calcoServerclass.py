import socket
from threading import Thread
import json

from calcoloClientMultithreading import SERVER_ADDRESS
SERVER_ADDRESS="127.0.0.1"
SERVER_PORT=22003
class Server():
    def __init__(self,address,port):
        self.address=address
        self.port=port

    def avvia_server(self):
        sock_listen=socket.socket()
        sock_listen.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
        sock_listen.bind((self.address,self.port))
        sock_listen.listen(5)
        print("server in ascolto su %s."%str((self.address,self.port)))
        return sock_listen

    def accetta_connessioni(self,sock_listen):
        while True:
            sock_service,addr_client=sock_listen.accept()
            print("\nConnesssione ricevuta da"+str(addr_client))
            print("\nCreo un thread per servire le richieste")
            try:
                Thread(target=self.ricevi_comandi,args=(sock_service,addr_client)).start()
            except:
                print("il thread non si avvia")
                sock_listen.close()
                
    def ricevi_comandi(self,sock_service, addr_client):
        print("avviato")
        while True:
            data=sock_service.recv(1024)
            if not data:
                print("fine dati dal client.Reset")
                break
            data=data.decode()
            data=json.loads(data)
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
            elif operazione==":":
                if secondoNumero==0:
                    ris="Non puoi dividere per 0"
                else:
                    ris=primoNumero/secondoNumero
            elif operazione=="%":
                ris=primoNumero%secondoNumero
            else:
                ris="Operazione non riconosciuta"
            ris=str(ris)
            sock_service.sendall(ris.encode("UTF-8"))
        sock_service.close()
   
s1=Server(SERVER_ADDRESS,SERVER_PORT)
sock_list=s1.avvia_server()
s1.accetta_connessioni(sock_list)