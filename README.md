# Wysokość dla każdego punktu w Polsce

![alt text](https://raw.githubusercontent.com/majki09/daj_wysokosc/master/obrazek.jpg "Przykładowy widok w geoportalu.")

## Opis
Skrypt daje wysokość w metrach dla podanego punktu w Polsce. Korzysta z serwera GUGIK, którego usługa umożliwia pozyskanie informacji o wysokości terenu na podstawie danych z bazy NMT. Baza danych zawiera współrzędne (X,Y,Z) punktów w regularnej siatce o oczku 1 metra. Punkty zostały wyinterpolowane na podstawie chmury punktów z lotniczego skaningu laserowego (błąd średni wysokości zawiera się w przedziale do 0.2 m) lub też z pomiarów na zdjęciach lotniczych, w ramach aktualizacji na potrzeby wykonania ortofotomapy (błąd średni wysokości zawiera się w przedziale 0.8 - 2.0 m).
Usługa przyjmuje współrzędne jedynie w systemie PUWG-1992. Mając tylko współrzędne wg WGS-84 skrypt automatycznie konwertuje jednostki i daje gotowy wynik.

## Parametry

| Parametr | Opis |
|--|--|
| B | szerokość geograficzna wg WGS-84 (stopnie i dziesiąte części) |
| L | długość geograficzna wg WGS-84 (stopnie i dziesiąte części) |

## Przykładowe użycie:

    $ python3 daj_wysokosc.py --B 50.01234567 --L 20.01234567
    222.5

## Linki
* https://services.gugik.gov.pl/nmt/
* http://www.gugik.gov.pl/pzgik/zamow-dane/numeryczny-model-terenu
* https://mapy.geoportal.gov.pl/

## Podziękowania
- RusheerPL (https://github.com/CrusheerPL/demGenerator)
- Zbigniew Szymanski (z.szymanski@szymanski-net.eu)
