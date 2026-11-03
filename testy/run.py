"""Uruchamia wszystkie testy i zwraca kod 1 przy porażce.

    python3 testy/run.py                     # wszystko, lokalnie, strona pod http://127.0.0.1:PORT/nauka/
    python3 testy/run.py -k 05               # tylko testy, których nazwa zawiera „05”
    python3 testy/run.py --url https://akku1906.github.io/nauka/   # testy 1, 5, 8, 9 na adresie produkcyjnym

Wymaga Pythona 3 i pakietu playwright z Chromium (pip install playwright; playwright install chromium).
"""
import argparse
import pathlib
import sys
import time
import traceback

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
sys.dont_write_bytecode = True

import test_aplikacja  # noqa: E402
import test_statyczne  # noqa: E402
import test_tresc  # noqa: E402


def testy(modul):
    return [(n, getattr(modul, n)) for n in dir(modul) if n.startswith('test_') and callable(getattr(modul, n))]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--url', help='adres produkcyjny; uruchamia tylko testy oznaczone PROD')
    ap.add_argument('-k', default='', help='fragment nazwy testu')
    a = ap.parse_args()
    wyniki = []

    def uruchom(nazwa, fn, *arg):
        t0 = time.time()
        try:
            fn(*arg)
            wyniki.append((nazwa, True, ''))
            print(f'  OK    {nazwa} ({time.time() - t0:.1f} s)', flush=True)
        except Exception as e:  # noqa: BLE001
            opis = str(e) if isinstance(e, AssertionError) else traceback.format_exc()
            wyniki.append((nazwa, False, opis))
            print(f'  BŁĄD  {nazwa} ({time.time() - t0:.1f} s)\n        {opis.strip()[:3000]}', flush=True)

    if not a.url:
        print('Testy statyczne')
        for modul in (test_statyczne, test_tresc):
            for n, fn in testy(modul):
                if a.k in n:
                    uruchom(n, fn)

    from playwright.sync_api import sync_playwright
    print('Testy w przeglądarce' + (f' na {a.url}' if a.url else ''))
    with sync_playwright() as pw:
        try:
            b = pw.chromium.launch(channel='chromium')  # pełne Chromium, bliższe Chrome na telefonie
        except Exception:  # noqa: BLE001
            b = pw.chromium.launch()
        ctx = test_aplikacja.Kontekst(pw, b, a.url)
        try:
            for n, fn in testy(test_aplikacja):
                if a.k not in n or n == 'Kontekst':
                    continue
                if a.url and not getattr(fn, 'PROD', False):
                    continue
                uruchom(n, fn, ctx)
        finally:
            ctx.zamknij()
            b.close()

    zle = [w for w in wyniki if not w[1]]
    print(f'\nWynik: {len(wyniki) - len(zle)} z {len(wyniki)} testów przeszło.')
    return 1 if zle or not wyniki else 0


if __name__ == '__main__':
    sys.exit(main())
