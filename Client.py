import socket as s
import sys

HOST,PORT=sys.argv[1],int(sys.argv[2])

soc=s.socket(s.AF_INET, s.SOCK_STREAM) 
soc.connect((HOST,PORT)) 


msgToServer=raw_input("Write a message:")
soc.send(msgToServer)
msgFromServer=soc.recv(1024) 
print "Wiadomosc od serwera o tresci: %s"%(msgFromServer)
soc.close()
    
    

    
