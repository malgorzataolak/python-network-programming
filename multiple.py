import socket
import sys
import threading
import time

PORT=int(sys.argv[1])

def action(opt, a, b):
    if opt=="dodaj":
        s=a+b
        return s
    elif opt=="odejmij":
        return a-b
    elif opt=="pomnoz":
        return a*b
    elif opt=="podziel":
        return a/b
    elif opt=="mod":
        return a%b
    elif opt=="dodajwolno":
        time.sleep(15)
        return a+b
    elif opt=="pomnozwolno":
        time.sleep(15)
        return a*b
    
#Proces podporzadkowany
def run_TCP(TCP_client):
    message=TCP_client.recv(1024)
    msg=message.split()
    result=action(msg[2], float(msg[0]),float(msg[1]))
    print "Wysylam wynik: %s"%(result)
    TCP_client.sendall(str(result))
    TCP_client.close()
    
def something(UDP_sock,msg,address):
    result=action(msg[2], float(msg[0]),float(msg[1]))
    print "Wysylam wynik: %s"%(result)
    UDP_sock.sendto(str(result),address)

def run_UDP(UDP_sock):
    while True:
        message, address=UDP_sock.recvfrom(1024)
        msg=message.split()
        watek_obsluz=threading.Thread(target=something, args=(UDP_sock,msg,address,))
        watek_obsluz.start()
            
#Proces glowny 
TCP_sock=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
TCP_sock.bind(('',PORT))
TCP_sock.listen(1)
print "Oczekuje klienta TCP"

UDP_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
UDP_sock.bind(('', PORT))
print "Oczekuje na klienta UDP"

watek_UDP=threading.Thread(target=run_UDP, args=(UDP_sock,)) #Tworze proces podporzadkowany
watek_UDP.start()

while True:
    TCP_client, TCP_address=TCP_sock.accept()
    watek_TCP=threading.Thread(target=run_TCP, args=(TCP_client,)) #Tworze proces podporzadkowany odpowiedzialny za obsluge tego polaczenia
    watek_TCP.start()

    
