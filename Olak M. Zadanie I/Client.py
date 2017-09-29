import socket as s
import sys

HOST,PORT=sys.argv[1],int(sys.argv[2])

soc=s.socket(s.AF_INET, s.SOCK_STREAM) 
soc.connect((HOST,PORT)) 

msgToServer=raw_input("Napisz wiadomosc:")
soc.send(" "+msgToServer)
newMsg=soc.recv(256)
print newMsg
msgFromServer=soc.recv(256) 
print "Wiadomosc od serwera: "+msgFromServer
soc.close()
    
    

    
