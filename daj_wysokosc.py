import argparse
import math
import requests


def wgs84_do_puwg92(B_stopnie, L_stopnie):
    """
    Original C++ code from:  :
        Author: Zbigniew Szymanski
        E-mail: z.szymanski@szymanski-net.eu
        Version: 1.1
        Changelog (PL):
                        1.1 dodano przeksztalcenie odwrotne PUWG 1992 ->WGS84
                        1.0 przeksztalcenie WGS84 -> PUWG 1992
        Data modyfikacji: 2012-11-27
        Uwagi: Oprogramowanie darmowe. Dozwolone jest wykorzystanie i modyfikacja
               niniejszego oprogramowania do wlasnych celow pod warunkiem
               pozostawienia wszystkich informacji z naglowka. W przypadku
               wykorzystania niniejszego oprogramowania we wszelkich projektach
               naukowo-badawczych, rozwojowych, wdrozeniowych i dydaktycznych prosze
               o zacytowanie nastepujacego artykulu:

               Zbigniew Szymanski, Stanislaw Jankowski, Jan Szczyrek,
               "Reconstruction of environment model by using radar vector field histograms.",
               Photonics Applications in Astronomy, Communications, Industry, and
               High-Energy Physics Experiments 2012, Proc. of SPIE Vol. 8454, pp. 845422 - 1-8,
               doi:10.1117/12.2001354

        Literatura:
               Uriasz, J., “Wybrane odwzorowania kartograficzne”, Akademia Morska w Szczecinie,
               http://uriasz.am.szczecin.pl/naw_bezp/odwzorowania.html

    To Python3 translated by: RusheerPL – 2019-10-27
    https://github.com/CrusheerPL/demGenerator/
    """

    # konwersja współrzednych z układu WGS 84 do układu PUWG 1992
    # Parametry elipsoidy GRS-80
    e = 0.0818191910428  # pierwszy mimośród elipsoidy
    R0 = 6367449.14577  # promień sfery Lagrange'a
    Snorm = 0.000002  # parametr normujący
    xo = 5760000.0  # parametr centrujący

    # Współczynniki wielomianu
    a0 = 5765181.11148097
    a1 = 499800.81713800
    a2 = -63.81145283
    a3 = 0.83537915
    a4 = 0.13046891
    a5 = -0.00111138
    a6 = -0.00010504

    # Parametry odwzorowania Gaussa-Kruegera dla układu PUWG92
    L0_stopnie = 19.0  # Początek układu współrzędnych PUWG92 (długość)
    m0 = 0.9993
    x0 = -5300000.0
    y0 = 500000.0

    B = B_stopnie * math.pi / 180.0
    # dL = (L_stopnie - 19.0) * math.pi / 180.0   # - niepotrzebne?

    # etap I - elipsoida na kulę
    U = 1.0 - e * math.sin(B)
    V = 1.0 + e * math.sin(B)
    K = math.pow((U / V), (e / 2.0))
    C = K * math.tan(B / 2.0 + math.pi / 4.0)
    fi = 2.0 * math.atan(C) - math.pi / 2.0
    d_lambda = (L_stopnie - 19.0) * math.pi / 180.0

    # etap II - kula na walec
    p = math.sin(fi)
    q = math.cos(fi) * math.cos(d_lambda)
    r = 1.0 + math.cos(fi) * math.sin(d_lambda)
    s = 1.0 - math.cos(fi) * math.sin(d_lambda)
    XMERC = R0 * math.atan(p / q)
    YMERC = 0.5 * R0 * math.log(r / s)

    # etap III - walec na płaszczyznę
    Z = complex((XMERC - xo) * Snorm, YMERC * Snorm)
    Zgk = complex(a0 + Z * (a1 + Z * (a2 + Z * (a3 + Z * (a4 + Z * (a5 + Z * a6))))))
    Xgk = Zgk.real
    Ygk = Zgk.imag

    Xpuwg = m0 * Xgk + x0
    Ypuwg = m0 * Ygk + y0
    return Xpuwg, Ypuwg


def get_elevation(B: float, L: float):
    """
    Funkcja pobiera wysokość nad poziomem morza w metrach. Pobiera dane z serwera GUGIK.
    Serwer przyjmuje współrzędne jedynie w systemie odniesienia PUWG-1992. Mając współrzędne w systemie WGS-84 należy
    je przekonwertować.
    Obecnie działa tylko dla pozycji na terytorium Polski.
    :param B: (float) szerokość geograficzna wg WGS-84.
    :param L: (float) długość geograficzna wg WGS-84.
    :return: (str) wysokość nad poziomem morza [m] dla podanego punktu.
    """

    X, Y = wgs84_do_puwg92(B, L)

    server_address = "https://services.gugik.gov.pl/nmt/?request=GetHByXY&x={x}&y={y}".format(x=X, y=Y)
    response = requests.get(server_address)

    if response.status_code != 200:
        raise ConnectionError("Cannot connect.")
    elif response.content in [b"", b"0"]:
        raise ValueError("Bad response value. Check request.")
    else:
        elevation = response.content.decode(response.encoding)
        return elevation


def run_me():
    parser = argparse.ArgumentParser(description="Pozyskiwanie wysokości n.p.m. danego punktu.")
    parser.add_argument('--B', help='szerokość geograficzna wg WGS-84 (stopnie i dziesiąte części)', required=True)
    parser.add_argument('--L', help='długość geograficzna wg WGS-84 (stopnie i dziesiąte części)', required=True)
    args = parser.parse_args()

    try:
        B = float(args.B)
        L = float(args.L)
    except ValueError:
        print("Nieprawidłowe dane wejściowe")
        exit(1)

    print(get_elevation(B, L))


if __name__ == "__main__":
    run_me()
