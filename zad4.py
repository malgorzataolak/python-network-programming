#!/usr/bin/env python
"""
Malgorzata Olak - Zadanie 4
uruchomienie programu:
python zad4.py <nazwa/adres> <protokol> <port START> <port KONIEC>
"""
import sys
import socket
import select

address=sys.argv[1]
protocol=sys.argv[2]
start=int(sys.argv[3])
end=int(sys.argv[4])

if protocol=="TCP":
    for port in range(start, end+1):
        soc=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        soc.settimeout(1)
        result=soc.connect_ex((address,port))
        if result==0:
            print "Port: %s jest otwarty" %(port)
            soc.close()

if protocol=="UDP":
    soc=socket.socket(socket.AF_INET, socket.SOCK_DGRAM) #gniazdo udp
    icmpSoc=socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
    for port in range(start, end+1):
        soc.sendto("wiadomosc", (address, port))
        answerUDP=select.select([soc],[],[],1)[0]
        if not answerUDP:
            answer=select.select([icmpSoc],[],[],1)[0]

            if answer:

                icmpSoc.recv(1024)
                print "Port %s jest zamkniety"%(port)
            else:
                print "Port: %s nie odpowiada" %(port)
        else:
            print "Port %s jest otwarty"%(port)
            soc.recv(1024)
    soc.close()
    icmpSoc.close()
            
        
        
    
