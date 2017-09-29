import socket as s
import sys

PORT,msgToClient=int(sys.argv[1]),sys.argv[2]

soc=s.socket(s.AF_INET, s.SOCK_STREAM) 
soc.bind(('',PORT)) 
soc.listen(1) 
while True:
    connSocket,address=soc.accept() 
    msgFromClient=connSocket.recv(256)
    connSocket.send("Nawiazalem polaczenie")
    for x in xrange(10000):
	pass
    connSocket.send(msgToClient+"\n"+msgFromClient)
    print "Wiadomosc od adresu: %s o tresci: %s"%(address[0],msgFromClient)
    connSocket.close()

    
    

    
