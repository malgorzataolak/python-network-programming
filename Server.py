import socket as s
import sys

PORT,msgToClient=int(sys.argv[1]),sys.argv[2]

soc=s.socket(s.AF_INET, s.SOCK_STREAM) 
soc.bind(('',PORT)) 
soc.listen(1) 
while True:
    print "Oczekuje na polaczenie..."
    connSocket,address=soc.accept() 
    msgFromClient=connSocket.recv(1024)
    connSocket.send(msgToClient)
    connSocket.send(msgFromClient)
    print "Wiadomosc od adresu: %s o tresci: %s"%(address[0],msgFromClient)
    connSocket.close()

    
    

    
