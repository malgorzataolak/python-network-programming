Ma³gorzata Olak - Programowanie sieciowe 2015 - projekt zaliczeniowy
Komunikator
Uruchomienie w konsoli
Serwer:
python server.py <nrPortu>

Klient:
python client.py localhost <nrPortu>

Po uruchomeniu u¿ytkownik mo¿e siê zalogowaæ (L) albo zarejestrowaæ (R). 
Po zalogowanu u¿ytkownik mo¿e: ZnaleŸæ znajomych i dodaæ ch do lsty kontaktów, napisaæ wiadomoœæ, 
wyœwietliæ listê znajomych z opisem i statusem, zmieniæ opis, zmieniæ status, sprawdziæ czy wiadomoœci nie odczekuj¹ na odczytanie oraz wylogowaæ siê.
Ka¿da z komend zosta³a opisana jako szereg instrukcji w konsoli. Po uruchomieniu programu, a tak¿e po zmianach
ustawieñ w³asnego profilu (nie w trakcie) u¿ytkownik dostaje informacjê o wiadomoœciach do przeczytania.
Wys³anie wiadomoœci do innego u¿ytkownika jest mo¿liwe po wybraniu opcji "Napisz" oraz ustaleniu odbiorcy.
Komunikacja przep³ywa przez serwer. Program w razie koniecznoœc informuje nas, ¿e rozmówca jest obecnie niedostêpny.
Serwer przechowuje informacjê o adresie gniazd oraz czyœci je przed zamkniêciem programu. 
Wyjœcie z trybu pisania - *** 

Wersja poprawiona:
Poczas, gdy u¿ytkownik jest aktywny mo¿e ca³y czas otrzymywaæ wiadomoœci. Ograniczone zosta³o wyœwietlanie zawartoœci 
komunikatu od innej osoby. Jeœli pojawi¹ siê nowe wiadomoœci - serwer poinformuje nas o tym i zachêca do u¿yca komendy *. 
Dziêki temu dzia³ania klienta w panelu u¿ytkownika nie zostaj¹ zak³ócane poprzez wiadomoœci od innych,  nie zbieraj¹ siê one w jednej linii. 
Jest to mo¿liwe dziêki zastosowaniu flag, które dopiero po przejœciu w tryb "Napisz" pozwalaj¹ na swobodn¹ dyskusjê.
W pozosta³ych trybach flaga jest ustawiona na False. Podczas sprawdzania statusu rozmówcy doda³am sprawdzenie tej flagi.
Jeœli jest ona ustawiona na True to mo¿na prowadziæ swobodn¹ rozmowê. Jest ona przestawiona w trybie "Napisz". Ustawiene false
powoduje, ¿e u¿ytkownik nie bêdzie odczytywa³ wiadomoœci na bie¿¹co, a jedynie po wybraniu *.

Wylogowanie siê z programu odbywa siê za pomoc¹ trybu "Wyloguj". Mo¿na równie¿ zamkn¹æ serwer u¿ywaj¹c koendy ZAMKNIJ.
Informacja o zamkniêciu serwera zostaje rozes³ana po wszystkich u¿ytkownikach, którzy s¹ zmuszeni zakoñczyæ swoj¹ pracê. 
 

