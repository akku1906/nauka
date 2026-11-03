"""Audyt treści: każda odpowiedź liczbowa z luk, quizów, zdań P/F i par przeliczona niezależnie w Pythonie,
a rysunki do zadań g03, g04, g07, g12 i g15 zmierzone ze współrzędnych SVG.

Obliczenia są zapisane wprost, tak żeby dało się je przeczytać jak notatki z rachunków.
Po zmianie treści zadania trzeba tu zmienić także oczekiwaną odpowiedź, inaczej test nie przejdzie.
"""
import math
import re
from decimal import ROUND_HALF_UP, Decimal
from fractions import Fraction as F

from pomoc import KORZEN, sprawdz


# ---------------------------------------------------------------- odczyt plików tematów
def zadania(plik):
    t = (KORZEN / 'tematy' / plik).read_text(encoding='utf-8')
    sekcja = t.split('\n# Zadania\n', 1)[1].split('\n# Fiszki\n', 1)[0]
    out = {}
    for blok in re.split(r'\n(?=## )', '\n' + sekcja):
        m = re.match(r'\n?## (.*?)\s*\{(\w+) #([^}\s]+)\}\s*\n', blok)
        if not m:
            continue
        tresc = blok[m.end():].split('### Rozwiązanie', 1)[0]
        out[m.group(3)] = {'typ': m.group(2), 'tresc': tresc}
    return out


def luki(z):
    return [x.split('|')[0].strip() for x in re.findall(r'___\[([^\]]*)\]', z['tresc'])]


def quiz_dobra(z):
    return [m.strip() for m in re.findall(r'^- \[[xX]\]\s*(.*)$', z['tresc'], flags=re.M)]


def pf(z):
    return [(m[1].strip(), m[0] == 'P') for m in re.findall(r'^- \[(P|F)\]\s*(.*)$', z['tresc'], flags=re.M)]


def pary(z):
    w = [[c.strip() for c in l.strip().strip('|').split('|')] for l in z['tresc'].splitlines() if l.strip().startswith('|')]
    return [r for r in w[1:] if not all(re.fullmatch(r':?-{2,}:?', c) for c in r)]


def kroki(z):
    return re.findall(r'^\d+\.\s+(.*)$', z['tresc'], flags=re.M)


def svg(z):
    return re.search(r'<svg.*?</svg>', z['tresc'], flags=re.S).group(0)


def liczba(s):
    """'2,5' -> Fraction(5, 2), '−4' -> -4, '11/12' -> Fraction(11, 12)."""
    s = s.replace('$', '').replace(' ', '').replace(',', '.').replace('−', '-').replace('°', '')
    if '/' in s:
        a, b = s.split('/')
        return F(a) / F(b)
    return F(s)


def rzymska(n):
    w = [(1000, 'M'), (900, 'CM'), (500, 'D'), (400, 'CD'), (100, 'C'), (90, 'XC'), (50, 'L'), (40, 'XL'), (10, 'X'), (9, 'IX'), (5, 'V'), (4, 'IV'), (1, 'I')]
    out = ''
    for v, r in w:
        while n >= v:
            out += r
            n -= v
    return out


def z_rzymskiej(s):
    v = {'I': 1, 'V': 5, 'X': 10, 'L': 50, 'C': 100, 'D': 500, 'M': 1000}
    return sum(-v[a] if i + 1 < len(s) and v[a] < v[s[i + 1]] else v[a] for i, a in enumerate(s))


def poprawna_rzymska(s):
    return rzymska(z_rzymskiej(s)) == s


def pierwsza(n):
    return n > 1 and all(n % d for d in range(2, int(n ** .5) + 1))


def rozwiniecie(licznik, mianownik):
    """Rozwinięcie dziesiętne z okresem w nawiasie, np. 1/6 -> '0,1(6)'."""
    calk, r = divmod(licznik, mianownik)
    cyfry, gdzie = '', {}
    while r and r not in gdzie:
        gdzie[r] = len(cyfry)
        r *= 10
        cyfry += str(r // mianownik)
        r %= mianownik
    if not r:
        return f'{calk},{cyfry}' if cyfry else str(calk)
    i = gdzie[r]
    return f'{calk},{cyfry[:i]}({cyfry[i:]})'


def zaokr(x, miejsca):
    return Decimal(x).quantize(Decimal(1).scaleb(-miejsca), rounding=ROUND_HALF_UP)


# ---------------------------------------------------------------- liczby i działania
def test_tresc_liczby():
    Z = zadania('mat-e8-liczby.md')
    # k01: 20 − 12 : 4 · 3, dzielenie i mnożenie od lewej
    sprawdz(liczba(quiz_dobra(Z['k01'])[0]) == 20 - F(12, 4) * 3 == 11, 'k01')
    sprawdz(20 - F(12, 4 * 3) == 19 and (20 - 12) / F(4) * 3 == 6 and (20 - F(12, 4)) * 3 == 51, 'k01: dystraktory')
    # k02: znaki
    prawda = [(-3) * (-4) == 12, (-2) * 5 == 10, 5 - (-3) == 8, F(-12, -3) == -4]
    sprawdz([v for _, v in pf(Z['k02'])] == prawda, 'k02')
    # k26: liczby ujemne
    sprawdz([liczba(x) for x in luki(Z['k26'])] == [F(-12, 3), F('-2.5') + 5, 1 - F('3.5')] == [-4, F(5, 2), F(-5, 2)], 'k26')
    # k03: wartość bezwzględna
    sprawdz([liczba(x) for x in luki(Z['k03'])] == [abs(-7), abs(0)], 'k03')
    # k04: suma cyfr 7524 = 18, a pozostałe nie dzielą się przez 9
    sprawdz(quiz_dobra(Z['k04']) == ['7524'] and 7524 % 9 == 0 and all(n % 9 for n in (1999, 7526, 9001)), 'k04')
    # k05: cechy podzielności sprawdzone na wszystkich liczbach do 10 000
    cechy = {2: lambda n: n % 10 in (0, 2, 4, 6, 8), 3: lambda n: sum(map(int, str(n))) % 3 == 0,
             4: lambda n: (n % 100) % 4 == 0, 5: lambda n: n % 10 in (0, 5), 9: lambda n: sum(map(int, str(n))) % 9 == 0}
    sprawdz(sorted(int(p[0]) for p in pary(Z['k05'])) == sorted(cechy), 'k05: zestaw dzielników')
    sprawdz(all(cechy[d](n) == (n % d == 0) for d in cechy for n in range(1, 10000)), 'k05: cecha nie działa')
    # k06: liczby pierwsze
    sprawdz([v for _, v in pf(Z['k06'])] == [pierwsza(1), [p for p in range(1, 100) if pierwsza(p) and p % 2 == 0] == [2], pierwsza(51), pierwsza(97)], 'k06')
    # k07: 360 = 2^3 · 3^2 · 5
    sprawdz(2 ** 3 * 3 ** 2 * 5 == 360 and [int(x) for x in luki(Z['k07'])] == [3, 2], 'k07')
    # k08, k09: NWD i NWW liczb 72 i 60
    sprawdz(liczba(quiz_dobra(Z['k08'])[0]) == math.gcd(72, 60) == 12, 'k08')
    sprawdz(72 * 60 == 4320 == 12 * 360 and math.lcm(72, 60) == 360, 'k08: dystraktory')
    sprawdz(int(luki(Z['k09'])[0]) == math.lcm(72, 60), 'k09')
    # k10: NWW(12, 18) = 36
    sprawdz('$NWW(12, 18) = 36$' == kroki(Z['k10'])[-1] and math.lcm(12, 18) == 36 == 2 ** 2 * 3 ** 2, 'k10')
    # k11: 47 = 6 · 7 + 5
    sprawdz([int(x) for x in luki(Z['k11'])] == list(divmod(47, 6)), 'k11')
    # k12: poniedziałek + 100 dni
    dni = ['poniedziałek', 'wtorek', 'środa', 'czwartek', 'piątek', 'sobota', 'niedziela']
    sprawdz(quiz_dobra(Z['k12']) == [dni[100 % 7]], 'k12')
    # k13–k16: ułamki
    sprawdz(liczba(luki(Z['k13'])[0]) == F(2, 3) + F(1, 4), 'k13')
    sprawdz(liczba(quiz_dobra(Z['k14'])[0]) == F(3, 4) / F(3, 8) and F(3, 4) * F(3, 8) == F(9, 32) and F(4, 3) * F(3, 8) == F(1, 2), 'k14')
    sprawdz(liczba(luki(Z['k15'])[0]) == 2 + F(1, 3), 'k15')
    sprawdz(liczba(quiz_dobra(Z['k16'])[0]) == 24 / F(3, 5) and F(3, 5) * 24 == F('14.4'), 'k16')
    # k17: ułamki i rozwinięcia dziesiętne
    sprawdz(all(liczba(a.replace('\\frac{', '').replace('}{', '/').replace('}', '')) == liczba(b) for a, b in pary(Z['k17'])), 'k17')
    # k18: 3/8
    sprawdz(liczba(luki(Z['k18'])[0]) == F(3, 8), 'k18')
    # k19: rozwinięcia okresowe
    zd = pf(Z['k19'])
    sprawdz([v for _, v in zd] == [rozwiniecie(1, 3) == '0,(3)', rozwiniecie(1, 6) == '0,(6)', rozwiniecie(2, 11) == '0,(18)', rozwiniecie(1, 9) == '0,9'], 'k19')
    # k20, k21: zaokrąglanie
    sprawdz(quiz_dobra(Z['k20']) == [str(zaokr('3.146', 2)).replace('.', ',')], 'k20')
    sprawdz(int(luki(Z['k21'])[0]) == int(zaokr('2748', -2)), 'k21')
    # k22–k25: system rzymski
    sprawdz(all(z_rzymskiej(a) == int(b) for a, b in pary(Z['k22'])), 'k22')
    l23 = luki(Z['k23'])
    sprawdz(int(l23[0]) == z_rzymskiej('MCMXCIV') == 1994 and l23[1] == rzymska(2027), 'k23')
    sprawdz(quiz_dobra(Z['k24']) == ['CXC'] and poprawna_rzymska('CXC') and not any(map(poprawna_rzymska, ['IIII', 'VV', 'IC'])), 'k24')
    sprawdz(z_rzymskiej('MCMXCIV') == 1000 + 900 + 90 + 4, 'k25')


# ---------------------------------------------------------------- figury płaskie
def test_tresc_figury():
    Z = zadania('mat-e8-figury.md')
    st = lambda z: liczba(quiz_dobra(z)[0])  # noqa: E731
    sprawdz(st(Z['g01']) == 180 - 65, 'g01')
    sprawdz(int(luki(Z['g03'])[0]) == 180 - 70, 'g03')
    sprawdz(st(Z['g04']) == 40 + 75 == 180 - (180 - 40 - 75), 'g04')
    trojkat = lambda a, b, c: max(a, b, c) < a + b + c - max(a, b, c)  # noqa: E731
    sprawdz(quiz_dobra(Z['g05']) == ['4, 5, 8'] and trojkat(4, 5, 8) and not any(trojkat(*t) for t in [(2, 3, 5), (1, 2, 4), (5, 5, 11)]), 'g05')
    sprawdz(int(luki(Z['g06'])[0]) == (180 - 40) / 2, 'g06')
    sprawdz(st(Z['g07']) == F(10 * 6, 2) and (10 * 6, 10 * 8 / 2, 8 * 6 / 2) == (60, 40, 24), 'g07')
    sprawdz(int(luki(Z['g08'])[0]) == math.isqrt(6 ** 2 + 8 ** 2) and 6 ** 2 + 8 ** 2 == 10 ** 2, 'g08')
    sprawdz(st(Z['g09']) == 12 and 13 ** 2 - 5 ** 2 == 144 == 12 ** 2 and 13 ** 2 + 5 ** 2 == 194, 'g09')
    sprawdz(quiz_dobra(Z['g11']) == ['$5\\sqrt{2}$'] and 5 ** 2 + 5 ** 2 == 50 == 5 ** 2 * 2, 'g11')
    sprawdz(int(luki(Z['g12'])[0]) == 12 / 2 and abs(math.sqrt(12 ** 2 - 6 ** 2) - 6 * math.sqrt(3)) < 1e-9, 'g12')
    sprawdz(quiz_dobra(Z['g13']) == ['$3\\sqrt{3}$'] and abs(math.sqrt(6 ** 2 - 3 ** 2) - 3 * math.sqrt(3)) < 1e-9
            and abs(6 ** 2 * math.sqrt(3) / 4 - 9 * math.sqrt(3)) < 1e-9, 'g13')
    sprawdz(int(luki(Z['g15'])[0]) == (10 + 6) * 4 / 2, 'g15')
    sprawdz([int(x) for x in luki(Z['g16'])] == [6 * 8 / 2, math.isqrt(3 ** 2 + 4 ** 2)], 'g16')
    sprawdz(quiz_dobra(Z['g17']) == ['10 000'] and 100 * 100 == 10000 and 1000 * 1000 == 1000000, 'g17')
    h = math.isqrt(10 ** 2 - 6 ** 2)
    sprawdz(h == 8 and 12 * h / 2 == 48 and kroki(Z['g18'])[-1] == '$P = \\frac{12 * 8}{2} = 48$', 'g18')
    sprawdz([int(x) for x in luki(Z['g19'])] == [(6 - 2) * 180, (6 - 2) * 180 // 6], 'g19')
    sprawdz([v for _, v in pf(Z['g20'])] == [(4 - 2) * 180 == 360, (5 - 2) * 180 == 450, (8 - 2) * 180 / 8 == 135, False], 'g20')
    sprawdz(quiz_dobra(Z['g21']) == ['$25π$'] and 5 ** 2 == 25, 'g21')
    sprawdz(int(luki(Z['g22'])[0]) == 2 * (8 // 2), 'g22')
    sprawdz(int(luki(Z['g23'])[0]) == 6 ** 2 / 4, 'g23')
    sprawdz([int(x) for x in luki(Z['g25'])] == [(2 + 8) / 2, (3 + (-1)) / 2], 'g25')
    sprawdz([v for _, v in pf(Z['g26'])] == [True, math.hypot(5, 12) == 17, math.hypot(9, 12) == 15, math.sqrt(10 ** 2 - 6 ** 2) == 4], 'g26')
    sprawdz('g10' not in Z, 'g10 korzystało z twierdzenia odwrotnego do twierdzenia Pitagorasa, które jest poza podstawą')


# ---------------------------------------------------------------- rysunki
def kat(P, Q, R):
    """Kąt QPR w stopniach."""
    v1, v2 = (Q[0] - P[0], Q[1] - P[1]), (R[0] - P[0], R[1] - P[1])
    return math.degrees(math.acos((v1[0] * v2[0] + v1[1] * v2[1]) / math.hypot(*v1) / math.hypot(*v2)))


def punkty(s, el='polygon'):
    m = re.search(rf'<{el} points="([^"]+)"', s)
    return [tuple(map(float, p.split(','))) for p in m.group(1).split()]


def napisy(s):
    return {t: (float(x), float(y)) for x, y, t in re.findall(r'<text x="([\d.]+)" y="([\d.]+)">([^<]+)</text>', s)}


def test_rysunki_zgodne_z_trescia():
    Z = zadania('mat-e8-figury.md')
    # g03: sieczna nachylona pod kątem 70°, łuk 70° przy prostej a po prawej stronie u góry, β przy b po lewej u góry
    s = svg(Z['g03'])
    (x1, y1, x2, y2) = map(float, re.search(r'<line x1="([\d.]+)" y1="([\d.]+)" x2="([\d.]+)" y2="([\d.]+)"/>\n<path d="M212', s).groups())
    sprawdz(abs(math.degrees(math.atan2(y1 - y2, x2 - x1)) - 70) < 1.5, 'g03: sieczna nie ma 70°')
    xa = x1 + (x2 - x1) * (y1 - 50) / (y1 - y2)
    xb = x1 + (x2 - x1) * (y1 - 130) / (y1 - y2)
    n = napisy(s)
    sprawdz(n['70°'][0] > xa and n['70°'][1] < 50, 'g03: 70° nie stoi w prawym górnym kącie przy a')
    sprawdz(n['β'][0] < xb and n['β'][1] < 130, 'g03: β nie stoi w lewym górnym kącie przy b')
    # g04: kąty trójkąta 40°, 65°, 75°, a kąt zewnętrzny przy B ma 115°
    A, B, C = punkty(svg(Z['g04']))
    sprawdz(abs(kat(A, B, C) - 40) < 1 and abs(kat(C, A, B) - 75) < 1 and abs(kat(B, A, C) - 65) < 1,
            f'g04: kąty rysunku {kat(A, B, C):.0f}, {kat(B, A, C):.0f}, {kat(C, A, B):.0f} zamiast 40, 65, 75')
    n = napisy(svg(Z['g04']))
    sprawdz(math.dist(n['40°'], A) < math.dist(n['40°'], B) and math.dist(n['75°'], C) < math.dist(n['75°'], A) and n['x'][0] > B[0], 'g04: oznaczenia przy złych wierzchołkach')
    # g07: podstawa 10, wysokość 6, bok 8 w jednej skali
    A, B, C = punkty(svg(Z['g07']))
    sk = (B[0] - A[0]) / 10
    sprawdz(abs((A[1] - C[1]) / sk - 6) < 0.1 and abs(math.dist(A, C) / sk - 8) < 0.1, 'g07: proporcje')
    # g12: kąt 30° przy wierzchołku naprzeciw x, przeciwprostokątna dwa razy dłuższa od x, napis 30° nie nachodzi na bok
    A, B, C = punkty(svg(Z['g12']))  # A kąt prosty, B kąt 30°, C góra
    sprawdz(abs(kat(A, B, C) - 90) < 0.5 and abs(kat(B, A, C) - 30) < 0.5, 'g12: kąty')
    sprawdz(abs(math.dist(B, C) / math.dist(A, C) - 2) < 0.02, 'g12: przeciwprostokątna nie jest dwa razy dłuższa od x')
    n = napisy(svg(Z['g12']))
    x30, y30 = n['30°']
    prawa_krawedz = x30 + 14
    y_boku = B[1] - (B[1] - C[1]) * (B[0] - prawa_krawedz) / (B[0] - A[0])  # przeciwprostokątna nad prawą krawędzią napisu
    sprawdz(y30 - 12 > y_boku, f'g12: napis 30° nachodzi na przeciwprostokątną ({y30 - 12:.0f} vs {y_boku:.0f})')
    sprawdz(n['x'][0] < A[0] and C[1] < n['x'][1] < A[1], 'g12: x nie stoi przy przyprostokątnej naprzeciw 30°')
    # g15: podstawy 10 i 6, wysokość 4 w jednej skali
    D1, D2, G2, G1 = punkty(svg(Z['g15']))
    sk = (D2[0] - D1[0]) / 10
    sprawdz(abs((G2[0] - G1[0]) / sk - 6) < 0.1 and abs((D1[1] - G1[1]) / sk - 4) < 0.1, 'g15: proporcje podstaw i wysokości')
