Ma�gorzata Olak - Programowanie sieciowe 2015 - projekt zaliczeniowy
Komunikator
Uruchomienie w konsoli
Serwer:
python server.py <nrPortu>

Klient:
python client.py localhost <nrPortu>

Po uruchomeniu u�ytkownik mo�e si� zalogowa� (L) albo zarejestrowa� (R). 
Po zalogowanu u�ytkownik mo�e: Znale�� znajomych i doda� ch do lsty kontakt�w, napisa� wiadomo��, 
wy�wietli� list� znajomych z opisem i statusem, zmieni� opis, zmieni� status, sprawdzi� czy wiadomo�ci nie odczekuj� na odczytanie oraz wylogowa� si�.
Ka�da z komend zosta�a opisana jako szereg instrukcji w konsoli. Po uruchomieniu programu, a tak�e po zmianach
ustawie� w�asnego profilu (nie w trakcie) u�ytkownik dostaje informacj� o wiadomo�ciach do przeczytania.
Wys�anie wiadomo�ci do innego u�ytkownika jest mo�liwe po wybraniu opcji "Napisz" oraz ustaleniu odbiorcy.
Komunikacja przep�ywa przez serwer. Program w razie konieczno�c informuje nas, �e rozm�wca jest obecnie niedost�pny.
Serwer przechowuje informacj� o adresie gniazd oraz czy�ci je przed zamkni�ciem programu. 
Wyj�cie z trybu pisania - *** 

Wersja poprawiona:
Poczas, gdy u�ytkownik jest aktywny mo�e ca�y czas otrzymywa� wiadomo�ci. Ograniczone zosta�o wy�wietlanie zawarto�ci 
komunikatu od innej osoby. Je�li pojawi� si� nowe wiadomo�ci - serwer poinformuje nas o tym i zach�ca do u�yca komendy *. 
Dzi�ki temu dzia�ania klienta w panelu u�ytkownika nie zostaj� zak��cane poprzez wiadomo�ci od innych,  nie zbieraj� si� one w jednej linii. 
Jest to mo�liwe dzi�ki zastosowaniu flag, kt�re dopiero po przej�ciu w tryb "Napisz" pozwalaj� na swobodn� dyskusj�.
W pozosta�ych trybach flaga jest ustawiona na False. Podczas sprawdzania statusu rozm�wcy doda�am sprawdzenie tej flagi.
Je�li jest ona ustawiona na True to mo�na prowadzi� swobodn� rozmow�. Jest ona przestawiona w trybie "Napisz". Ustawiene false
powoduje, �e u�ytkownik nie b�dzie odczytywa� wiadomo�ci na bie��co, a jedynie po wybraniu *.

Wylogowanie si� z programu odbywa si� za pomoc� trybu "Wyloguj". Mo�na r�wnie� zamkn�� serwer u�ywaj�c koendy ZAMKNIJ.
Informacja o zamkni�ciu serwera zostaje rozes�ana po wszystkich u�ytkownikach, kt�rzy s� zmuszeni zako�czy� swoj� prac�. 
 

