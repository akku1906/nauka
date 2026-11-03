"""Ustawia WERSJA w sw.js i index.html na podstawie skrótu plików powłoki.

Service worker uznaje aplikację za nową tylko wtedy, gdy zmieni się sw.js.
Dlatego po każdej zmianie index.html, manifestu, ikon albo sw.js uruchom:

    python3 narzedzia/wersja.py

Test testy/test_statyczne.py pilnuje, żeby skrót w sw.js zgadzał się z plikami.
Tematy nie wchodzą do skrótu, bo dochodzą same (najpierw sieć).
"""
import datetime
import hashlib
import re
import sys

from wspolne import KORZEN

POWLOKA = ['index.html', 'sw.js', 'manifest.webmanifest',
           'ikony/ikona-192.png', 'ikony/ikona-512.png',
           'ikony/ikona-maskable-192.png', 'ikony/ikona-maskable-512.png']
WZOR = re.compile(r"const WERSJA='[^']*';")


def skrot():
    h = hashlib.sha256()
    for nazwa in POWLOKA:
        dane = (KORZEN / nazwa).read_bytes()
        if nazwa in ('index.html', 'sw.js'):
            dane = WZOR.sub("const WERSJA='';", dane.decode('utf-8')).encode('utf-8')
        h.update(nazwa.encode() + b'\0' + dane + b'\0')
    return h.hexdigest()[:8]


def obecna(nazwa):
    m = WZOR.search((KORZEN / nazwa).read_text(encoding='utf-8'))
    return m.group(0)[len("const WERSJA='"):-2] if m else None


def main():
    s = skrot()
    if all((obecna(n) or '').endswith('.' + s) for n in ('index.html', 'sw.js')):
        print('bez zmian', obecna('sw.js'))
        return
    nowa = datetime.date.today().isoformat() + '.' + s
    for n in ('index.html', 'sw.js'):
        p = KORZEN / n
        t = p.read_text(encoding='utf-8')
        if not WZOR.search(t):
            sys.exit(f'{n}: nie ma linii const WERSJA')
        p.write_text(WZOR.sub(f"const WERSJA='{nowa}';", t, count=1), encoding='utf-8')
    print('ok', nowa)


if __name__ == '__main__':
    main()
