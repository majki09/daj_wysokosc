# Wysokość dla każdego punktu w Polsce

![alt text](https://raw.githubusercontent.com/majki09/daj_wysokosc/master/obrazek.jpg "Przykładowy widok w geoportalu.")

## Opis
Skrypt daje wysokość w metrach dla podanego punktu w Polsce. Korzysta z serwera GUGIK, który przyjmuje współrzędne 
jedynie w systemie PUWG-1992. Mając tylko współrzędne wg WGS-84 skrypt konwertuje jednostki za nas i
daje gotowy wynik.


## Parametry

| Parametr | Opis |
|--|--|
| B | szerokość geograficzna wg WGS-84 (stopnie i dziesiąte części) |
| L | długość geograficzna wg WGS-84 (stopnie i dziesiąte części) |

## Przykładowe użycie:

    $ python3 daj_wysokosc.py --B 50.01234567 --L 20.01234567
    222.5

## Podziękowania
- RusheerPL (https://github.com/CrusheerPL/demGenerator)
- Zbigniew Szymanski (z.szymanski@szymanski-net.eu)
