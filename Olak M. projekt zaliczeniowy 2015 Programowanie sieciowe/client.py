#Malgorzata Olak - projekt koncowy - Programowanie sieciowe 2015
import socket
import sys
import threading
import select
HOST=sys.argv[1]
PORT=int(sys.argv[2])
poslaniec=True
class Client:
    def odbierz_wiadomosc(self,s):
        global poslaniec
        while True:
	    if select.select([s], [], [], 60)[0]:
	    	msg=s.recv(1024)
	    	print msg
		if not msg:
                	print "Serwer przestal dzialac"
		    	return
		if msg[0]=="#":
                    poslaniec=False
                    return
		
    def client_start(self):
        client=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((HOST, PORT))
        watek_wiadomosci=threading.Thread(target=self.odbierz_wiadomosc, args=(client,))
        watek_wiadomosci.daemon=True
        watek_wiadomosci.start()
        while True:
               send_msg=raw_input("")
               if poslaniec==False:
                   return
               
               if send_msg=="Wyloguj":
                   client.close()
                   return
               else:
                   client.send(send_msg)
                   
               
         
mojKlient=Client()
mojKlient.client_start()
            
            
                
        
