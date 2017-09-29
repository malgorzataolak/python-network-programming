# -*- coding: cp1250 -*-
#Malgorzata Olak - projekt koncowy - Programowanie sieciowe 2015
import socket
import sys
import threading
import pickle
import os
import time

class User:
    def __init__(self):
        self.login=""
        self.haslo=""
        self.znajomi=set()
        self.opis=""
        self.stan="off"
        self.status="Niepodlaczony"
        self.wiadomosci=""
        
PORT=int(sys.argv[1])
uzytkownik=""
class Server:
    def __init__(self):
        self.users_list={}
        self.blokuj=threading.Lock() #mechanizm blokowania dla operacji na liscie uzytkownikow
        self.load_data() #zaladowanie listy uzytkownikow i wszystkich informacji z pliku 
        self.users_adr={}
        self.users_dost={}
    def save_data(self):
        print "Autozapisywanie w osobnym watku"
        while True:
            time.sleep(15)
            with self.blokuj:
                pickle.dump(self.users_list, open("uzytkownicy.p","wb"))
                print "Autozapis"
        
    def load_data(self):
        if os.path.isfile("uzytkownicy.p"):
            with self.blokuj:
                self.users_list=pickle.load(open("uzytkownicy.p","rb"))
        else:
            print "Pierwsze uzycie programu, baza uzytkownikow pusta."
        

    def serv_start(self):
        #osobny watek na autobackup danych
        watek_zapisu=threading.Thread(target=self.save_data)
        watek_zapisu.daemon=True
        watek_zapisu.start()
        #utworzenie socketa
        server_sock=socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
        server_sock.bind(('',PORT))
        server_sock.listen(1)
        print "Serwer uruchomiony, oczekuje na klientow..."
        watek_polaczen=threading.Thread(target=self.polaczenia, args=(server_sock,))
        watek_polaczen.daemon=True
        watek_polaczen.start()
        while True:
            cloosee=raw_input("Zamknij Serwer: <napisz ZAMKNIJ>")
            if cloosee=="ZAMKNIJ":
                for u in self.users_adr.keys():
                    self.users_adr[u].send("#Serwer zostanie wylaczony za 5 sek. Zegnam!!!")
                    with self.blokuj:
                        self.users_list[u].stan="off"
                        self.users_list[u].status="Niepodlaczony"
                    time.sleep(5)
                    self.users_adr[u].close()
                with self.blokuj:
                    pickle.dump(self.users_list, open("uzytkownicy.p","wb"))
                    print "Ostatni zapis zostal wykonany. Koniec pracy serwera"
                    server_sock.close()
                    return
            else:
                print "napisz ZAMKNIJ aby wylaczyc serwer."
                
                
        
    def polaczenia(self, server_sock):
        while True:
            server, addres=server_sock.accept()
            #podlaczanie klientow  - rozdzielenie watku
            watek_klientow=threading.Thread(target=self.connection, args=(server,))
            watek_klientow.start()

            
    def connection(self,s):
        print "Pojawil sie klient..."
        s.send("Korzystaj z komunikatora!")
        while True:
            s.send("Wpisz L by sie zalogowac, R aby sie zarejestrowac")
            klient_on=s.recv(1024) #klient decyduje czy chce sie zalogowac czy zarejestrowac
            if klient_on=="L":
                log=self.login(s)
                break
            elif klient_on=="R":
                self.rejestracja(s)
                log=self.login(s)
                break
            else:
                s.send("!Blad komendy, wpisz jeszcze raz!")
                continue
        self.users_adr[log]=s
        
        #nasluchuj wiadomosci
        while True:
            self.users_dost[log]=False
            s.send("\nWitamy w komunikatorze! Mozliwe opcje:\nSzukaj - aby znalezc znajomych\n* - sprawdz czy nie nadeszla wiadomosc\n Napisz - aby wyslac wiadomosc\nWyloguj - aby wylogowac\nZS - zmien status\nZO - zmien opis\nZnajomi - aby wyswietlic znajomych\n")
            if self.users_list[log].wiadomosci!="":
                s.send("\n******Masz nieprzeczytane wiadomosci! Wcisnij * by je odczytac*******\n")
            data=s.recv(1024)
                
            if not data:
                print "Uzytkownik %s opuscil komunikator " %(self.users_list[log].login)
                with self.blokuj:
                    self.users_list[log].stan="off"
                    self.users_list[log].status="Niepodlaczony"
                    print self.users_list[log].status
                    print log
                    return
            if data=="*":
                s.send(self.users_list[log].wiadomosci)
                with self.blokuj:
                    self.users_list[log].wiadomosci="" #czysc wiadomosci
            if data=="Szukaj":
                self.znajdz_przyjaciela(self.users_list[log].login,s)
                #powyzsze przekazuje do szukania login wlasny i gniazdo
            if data=="Napisz":
                self.users_dost[log]=True
                s.send("Podaj nazwe rozmowcy ")
                login_rozmowcy=s.recv(1024)
                if login_rozmowcy in self.users_list.keys():
                    
                    if self.users_list[login_rozmowcy].stan=="on": #jesli uzytkownik jest online
                        s.send("Rozmowa nawiazana z uzytkowikiem %s "%(login_rozmowcy))
                        while True:
                            
                            msg=s.recv(1024) #odbior wiadomosci przez serwer - ma byc ona przeslana dalej
                            if msg=="***":
                                break
                            #na wypadek gdyby w trakcie sie wylogowal
            
                            if self.users_list[login_rozmowcy].stan=="off":
                                s.send("Uzytkownik %s jest offline. Mozesz zostawic mu wiadomosc. "%login_rozmowcy)
                                with self.blokuj:
                                    inf="Uzytkownik %s napisal: %s\n"%(log, msg)
                                    self.users_list[login_rozmowcy].wiadomosci+=inf
                            #na wypadek gdyby uzytkownik zmienil status na niewidoczny w trakcie rozmowy
                            elif self.users_list[login_rozmowcy].status=="Niewidoczny" and self.users_dost[login_rozmowcy]==True:
                                s.send("Uzytkownik %s jest offline. Mozesz zostawic mu wiadomosc. "%login_rozmowcy)
                                self.users_adr[login_rozmowcy].send(log+": "+msg)
                            elif self.users_list[login_rozmowcy].status=="Niewidoczny" and self.users_dost[login_rozmowcy]==False:
                                s.send("Uzytkownik %s jest offline. Mozesz zostawic mu wiadomosc. "%login_rozmowcy)
                                with self.blokuj:
                                    inf="Uzytkownik %s napisal: %s\n"%(log, msg)
                                    self.users_list[login_rozmowcy].wiadomosci+=inf
                            elif self.users_dost[login_rozmowcy]==False:
                                with self.blokuj:
                                    inf="Uzytkownik %s napisal: %s\n"%(log, msg)
                                    self.users_list[login_rozmowcy].wiadomosci+=inf
                            else:        
                                #w ramach normalnej rozmowy
                                self.users_adr[login_rozmowcy].send(log+": "+msg)
                            
                    if self.users_list[login_rozmowcy].stan=="off":
                        s.send("Uzytkownik %s jest offline. Mozesz zostawic mu wiadomosc. "%login_rozmowcy)
                        while True:
                            msg=s.recv(1024)
                            if msg=="***":
                                 break
                            #w przypadku gdy jest niewidoczny
                            if self.users_list[login_rozmowcy].status=="Niewidoczny":
                                self.users_adr[login_rozmowcy].send(log+": "+msg)
                            #w przypadku gdy uzytkownik jest online
                            elif self.users_list[login_rozmowcy].stan=="on" and self.users_list[login_rozmowcy].status!="Niewidoczny":
                                s.send("Uzytkonik %s jest dostapny "%(login_rozmowcy))
                                self.users_adr[login_rozmowcy].send(log+": "+msg) 
                            else:
                                with self.blokuj:
                                    inf="Uzytkownik %s napisal: %s\n"%(log, msg)
                                    self.users_list[login_rozmowcy].wiadomosci+=inf

                    
            if data=="ZO":
                #zmien opis
                s.send("Twoj obecny OPIS to: %s . Podaj nowy: "%self.users_list[log].opis)
                nowy_opis=s.recv(1024)
                with self.blokuj:
                    self.users_list[log].opis=nowy_opis
                s.send("Twoj nowy opis to: %s .\n"%self.users_list[log].opis)
                
            if data=="ZS":
                s.send("\nTwoj obecny STATUS to: %s . \nDostepne mozliwosci: \nD -dostepny\nZW - zaraz wracam\nNIE - niewidoczny"%self.users_list[log].status)
                nowy_status=s.recv(1024)
                with self.blokuj:
                    if nowy_status=="D":
                        self.users_list[log].status="Dostepny"
                    if nowy_status=="ZW":
                        self.users_list[log].status="Zaraz wracam"
                    if nowy_status=="NIE":
                        self.users_list[log].status="Niewidoczny"
                    
                s.send("Twoj status: %s\n"%self.users_list[log].status)
                    
            if data=="Znajomi":
                znajomy=[]
                for u in self.users_list[log].znajomi:
                   
                    #oszukujemy uzytkownika ze znajomy jest niepodlaczony 
                    if self.users_list[u].status=="Niewidoczny":
                        seq=(self.users_list[u].login, self.users_list[u].opis, "Niepodlaczony")
                    else:
                        seq=(self.users_list[u].login, self.users_list[u].opis, self.users_list[u].status)
                    
                    info=" ".join(seq)
                    znajomy.append(info)
                
                znajomi="\n".join(znajomy)
                s.send(znajomi)

                
                

    def login(self,s):
        while True:
            s.send("Podaj login ")
            nazwa=s.recv(1024)
            if nazwa not in self.users_list.keys():
                s.send("!Uzytkownik o takim loginie nie istnieje ")
                continue #wroc do podawania loginu 
            else:
                s.send("Podaj haslo ")
                h=s.recv(1024)
                if h==self.users_list[nazwa].haslo:
                    print "Zalogowal sie uzytkownik o loginie: %s "%nazwa
                    s.send("Zalogowales sie do komunikatora\n")
                    with self.blokuj:
                        #dajemy serwerowi znac ze klient jest online
                        #dla uzytkownikow klient moze manualnie zmienic status na dostepny
                        self.users_list[nazwa].stan="on"
                        self.users_list[nazwa].status="Dostepny"
                        return self.users_list[nazwa].login
                        break
                else:
                    s.send("!haslo nie jest prawidlowe - sprobuj jeszcze raz")
                    continue #wszystko od poczatku

        
    
    def rejestracja(self,s):
        
        while True:
            s.send("Podaj login ")
            l=s.recv(1024)
            if l in self.users_list.keys():
                s.send("!Istnieje uzytkownik o takim samym loginie, wpisz inna nazwe. ")
                continue
            else:
                with self.blokuj:
                    self.users_list[l]=User()
                    self.users_list[l].login=l
                s.send("Podaj haslo ")
                h=s.recv(1024)
                with self.blokuj:
                    self.users_list[l].haslo=h
                s.send("Powtorz haslo ")
                hr=s.recv(1024)
                if hr==self.users_list[l].haslo:
                    s.send("Zostales pomyslnie zarejestrowany, teraz mozesz sie zalogowac...")
                    break
                else:
                    s.send("!Hasla roznia sie od siebie! ")
                    continue
    def znajdz_przyjaciela(self,l,s):
        s.send("Podaj login do wyszukania:")
        log=s.recv(1024)
        print self.users_list[l].login
        if log not in self.users_list.keys():
            s.send("Brak uzytkownika o podanym loginie")
            
        else:
            if log not in self.users_list[l].znajomi:
                if log==l:
                    s.send("Nie mozesz dodac siebie do znajomych!")
                else:
                    with self.blokuj:
                        self.users_list[l].znajomi.add(log) #dodaje znajomego do zbioru przyjaciol
                        s.send("Uzytkownik dodany")  
            else:
                s.send("Znajomy jest juz na Twojej liscie!")

                
mojSerwerek=Server()
mojSerwerek.serv_start()

