#Malgorzata Olak
#Programowanie Sieciowe 2015 - Zadanie 5 

import random
import socket
import sys
PORT=12000
class Ships:
    def create_board(self):
        self.board=[[0]*10 for i in xrange(10)]
    
    def print_board(self):
        print "+-"*10+"+"
        print "|"+('|\n|'.join(['|'.join(['{:1}'.format(item) for item in row]) for row in self.board]))+"|"
        print "+-"*10+"+"

    def check(self,size,x,y,o):
            try:
                if o!="H" and o!="V":
                    raise Exception("Okresl prawidlowo kierunek! V-pionowo H-poziomo")                    
                elif x>9 or x<0 or y>9 or y<0:
                    raise Exception("Wybierz liczby z zakresu 0 - 9 aby umiejscowic statek!")        
                elif o=="H":
                    for i in xrange(size):
                        if self.board[x][y+i]!=0:
                            raise Exception("Pozycja zajeta. Wybierz inne koordynaty statku")
                    return True        
                elif o=="V":
                    for i in xrange(size):
                        if self.board[x+i][y]!=0:
                            raise Exception("Pozycja zajeta. Wybierz inne koordynaty statku.")
                    return True         
                else:
                    return True
            except Exception as e:
                print e

    def place_ship(self,size,x,y,o):
        if o=="H":
            for i in xrange(size):
                self.board[x][y+i]=size
        elif o=="V":
            for i in xrange(size):
                self.board[x+i][y]=size
                
    def set_ships(self):
        floats={"Czteromasztowiec":(4,1),
          "Trzymasztowiec":(3,2),
          "Dwumaszgtowiec":(2,3),
          "Jednomasztowiec":(1,4)}
        for ship in floats.keys():
            print ship+" zostanie wstawiony"
            size=floats[ship][0]
            
      #petla dla kazdego z czterech rodzajow statku
            for z in range(floats[ship][1]):
                flag=False
                while flag!=True:
                    rows=raw_input("Podaj rzad: ")
                    columns=raw_input("Podaj kolumne: ")
                    orientation=raw_input("Kierunek: H-poziomo V-pionowo")
                    x=int(rows)
                    y=int(columns)
                    o=orientation.upper()
                    flag=self.check(size,x,y,o)
                    
                self.place_ship(size,x,y,o) #ustawiamy statek
                self.print_board()

    def auto_set(self):
        floats={"Czteromasztowiec":(4,1),
          "Trzymasztowiec":(3,2),
          "Dwumaszgtowiec":(2,3),
          "Jednomasztowiec":(1,4)}
        for ship in floats.keys():
            print ship+" zostanie wstawiony"
            size=floats[ship][0]
            
      #petla dla kazdego z czterech rodzajow statku
            for z in range(floats[ship][1]):
                flag=False
                while flag!=True:
                    x=random.randint(0,9)
                    y=random.randint(0,9)
                    orientation=random.randint(0,1)
                    if orientation==0:
                        o="H"
                    else:
                        o="V"
                    flag=self.check(size,x,y,o)
                    
                self.place_ship(size,x,y,o) #ustawiamy statek
               
    def guess_ship(self,ship_type):
        if ship_type==1:
            return "Jednomasztowiec"
        elif ship_type==2:
            return "Dwumasztowiec"
        elif ship_type==3:
            return "Trzymasztowiec"
        else:
            return "Czteromaszowiec"
    def get_point(self):
        flag3=False
        while flag3!=True:
            rows=raw_input("Podaj rzad: ")
            columns=raw_input("Podaj kolumne: ")
            x=int(rows)
            y=int(columns)
            flag3=self.check(1,x,y,"H")
        return "%s%s"%(x,y)
#sprawdza czy na planszy sa jakies statki
    def check_win(self):
        for i in xrange(0,10):
            for j in xrange(0,10):
                if self.board[i][j]!=0 and self.board[i][j]!="X" and self.board[i][j]!="*":
                    return "nie"
        return "tak"
    
    def play(self,x,y):
        if self.board[x][y]==0:
            self.board[x][y]="*"
            return "pudlo"
        elif self.board[x][y]=="*" or self.board[x][y]=="X":
            return "wrong"
        else:
            self.board[x][y]="X"
            #sprawdz czy wygrana
            if self.check_win()=="tak":
                print "Przeciwnik wygral!"
                return "win"
            else:
                return "play"

class Server():
    def server_play(self):
        print "Tworze plansze serwera"
        #tworze plansze servera
        s_Ship=Ships()
        s_Ship.create_board()
        #stworzenie atrapy do celowania
        s_atrapa=Ships()
        s_atrapa.create_board()
        #tworze polaczenie - oczekuje na klienta
        print "Oczekuje na polaczenie z klientem..."
        my_socket=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        my_socket.bind(('',PORT))
        my_socket.listen(1)
        while True:
            connected_socket,address=my_socket.accept()
            print "Nawiazalem polaczenie z graczem klientem"
            settings=raw_input("Witaj w grze! Wybierz A - automatyczne rozstawianie statkow M - manualne rozstawianie statkow")
            #uzupelnij plansze 
            if settings=="A":
                s_Ship.auto_set()
            else:
                s_Ship.set_ships()
            #graj dopoki statki na planszy 
            while True:
                #pytaj o strzal - dopoki nie ma pudla
                flaga=True
                while flaga:
                    decide=raw_input("Wcisnij G by grac, R by porozmawiac")
                    if decide=="G":
                        print "Twoja plansza"
                        s_Ship.print_board()
                        print "Plansza przeciwnika"
                        s_atrapa.print_board()
                        punkt=s_atrapa.get_point()
                        connected_socket.sendall(punkt)
                        #sprawdz co znajduje sie na planszy klienta w danym punkcie
                        result=connected_socket.recv(1024)
                        if result=="pudlo":
                            s_atrapa.board[int(punkt[0])][int(punkt[1])]="*"
                            print "Pudlo!"
                            flaga=False
                        elif result=="wrong":
                            print "Zajete koordynaty"
                            flaga=True
                        elif result=="win":
                            print "Wygrales! Brawo!"
                            return
                        elif result=="play":
                            s_atrapa.board[int(punkt[0])][int(punkt[1])]="X"
                            print "Trafiony - Ekstra ruch"
                            
                    elif decide=="R":
                        #chat
                        print "Wpisz Z aby zakonczyc i wrocic do trybu gry"
                        
                        #wiadomosc dla przeciwnika zeby nasluchiwal chatu 
                        connected_socket.sendall("W")
                        flag_chat=True
                        while flag_chat:
                            serv_message=raw_input("napisz>>")
                            if serv_message!="Z":
                                connected_socket.sendall(serv_message)
                                client_message=connected_socket.recv(1024)
                                print "Przeciwnik: "+client_message
                            elif serv_message=="Z":
                                connected_socket.sendall(serv_message)
                                flag_chat=False                       
                        
                        
                #po spudlowaniu oddajemy ruch przeciwnikowi
                print "Ruch przeciwnika"
                #Przeciwnik przysyla nam punkty do zrewidowania - rewidujemy razem z nim dopoki nie spudluje
                flaga2=True
                while flaga2:
                    points=connected_socket.recv(1024)
                    if points=="W":
                        flag_chat=True
                        while flag_chat:
                            print "Przeciwnik pisze..."
                            msg_from_client=connected_socket.recv(1024)
                            if msg_from_client!="Z":
                                print "Przeciwnik: "+msg_from_client
                                msg_to_client=raw_input("napisz>>")
                                connected_socket.sendall(msg_to_client)
                            elif msg_from_client=="Z":
                                print "Przeciwnik rozpoczal gre..."
                                flag_chat=False
                    else:
                        answer=s_Ship.play(int(points[0]),int(points[1]))
                        #wysylamy wynik przeprowadzonej operacji
                        connected_socket.sendall(answer)
                        #jesli spudlowal konczymy petle
                        if answer=="pudlo":
                            flaga2=False
                        elif answer=="win":
                            #koncz jesli przeciwnik wygral
                            print "Koniec gry!"
                            return


class Client():
        def client_play(self):
            client_ship=Ships()
            client_ship.create_board()
            serw_atrapa=Ships()
            serw_atrapa.create_board()
            my_socket=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            my_socket.connect(("localhost",PORT))

            settings=raw_input("Witaj w grze! Wybierz A - automatyczne rozstawianie statkow M - manualne rozstawianie statkow")
            if settings=="A":
                client_ship.auto_set()
            else:
                client_ship.set_ships()
            #dopoki jest na czym operowac to graj 
            while True:
                f1=True
                #przygotuj do sprawdzenia swojej planszy i naniesienia poprawek - dopoki nie spudluje
                while f1:
                    
                    points=my_socket.recv(1024)
                    if points=="W":
                        flag_chat=True
                        while flag_chat:
                            print "Przeciwnik pisze..."
                            msg_from_client=my_socket.recv(1024)
                            if msg_from_client!="Z":
                                print "Przeciwnik: "+msg_from_client
                                msg_to_client=raw_input("napisz>>")
                                my_socket.sendall(msg_to_client)
                            elif msg_from_client=="Z":
                                print "Przeciwnik rozpoczal gre..."
                                flag_chat=False
                    else:
                        stan=client_ship.play(int(points[0]),int(points[1]))
                        my_socket.sendall(stan)
                        if stan=="pudlo":
                            f1=False
                        elif stan=="win":
                            print "Koniec gry!"
                            return
                        else:
                            print "Gracz ma kolejny ruch..."
                        print "Czekaj na swoja kolej"
                        
                czyPowrot=True
                while czyPowrot:
                    decide=raw_input("Wcisnij G aby grac R aby chatowac")
                    if decide=="G":
                        print "Twoja plansza"
                        client_ship.print_board()
                        print "Plansza przeciwnika"
                        serw_atrapa.print_board()
                        serwpoints=serw_atrapa.get_point()
                        my_socket.sendall(serwpoints)
                        servresult=my_socket.recv(1024)
                        if servresult=="pudlo":
                            print "Trafiony - zatopiony. Ruch przeciwnika."
                            serw_atrapa.board[int(serwpoints[0])][int(serwpoints[1])]="*"
                            czyPowrot=False
                        elif servresult=="wrong":
                            print "To pole bylo juz zaznaczone przez Ciebie! Zaznacz inne pole."
                            czyPowrot=True
                        elif servresult=="win":
                            print "Wygrales! Brawo!"
                            return
                        elif servresult=="play":
                            serw_atrapa.board[int(serwpoints[0])][int(serwpoints[1])]="X"
                            print "Trafiony - masz dodatkowy ruch"
                    elif decide=="R":
                        print "Wpisz Z aby zakonczyc i wrocic do trybu gry"
                        flag_chat2=True
                        #daj znak przeciwnikowi ze chcesz chatowac
                        my_socket.sendall("W")
                        #zapetlaj dopoki nie wcisnie znaku konca chatu
                        while flag_chat2:
                            serv_message=raw_input("napisz>>")
                            if serv_message!="Z":
                                my_socket.sendall(serv_message)
                                client_message=my_socket.recv(1024)
                                print "Przeciwnik: "+client_message
                            elif serv_message=="Z":
                                my_socket.sendall(serv_message)
                                flag_chat2=False


def main():
    s=Server()
    c=Client()
    answer=raw_input("Wybierz pozycje klienta lub serwera\nWpisz:\nS - Serwer\nC klient")
    if answer=="S":
        #akcje dla serwera
        s.server_play()
    elif answer=="C":
        #akcje dla klienta
        c.client_play()
    else:
        print "Zly znak - wpisz S lub C"

main()

