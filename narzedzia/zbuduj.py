"""Buduje wersję jednoplikową: index.html z wklejonymi tematami, do pracy bez hostingu.

    python3 narzedzia/zbuduj.py wynik.html                  # wszystkie tematy z tematy/index.json
    python3 narzedzia/zbuduj.py tematy/a.md tematy/b.md wynik.html

Wersja jednoplikowa nie rejestruje service workera, nie pobiera katalogu
i nie ma odnośników do manifestu ani ikon (otwarta z pliku nie mogłaby ich wczytać).
Jej zapis postępu jest przypisany do adresu pliku, więc do wersji z sieci
przenosi się go eksportem i importem postępu.
"""
import json
import pathlib
import re
import sys

from wspolne import KATALOG, KORZEN, TEMATY


def zbuduj(pliki):
    silnik = (KORZEN / 'index.html').read_text(encoding='utf-8')
    paczki = []
    for p in pliki:
        src = pathlib.Path(p).read_text(encoding='utf-8').replace('</script', '<\\/script')
        paczki.append('<script type="text/markdown" class="paczka">\n' + src + '\n</script>')
    if '<!-- PACZKI -->' not in silnik or "const TRYB='siec';" not in silnik:
        sys.exit('index.html nie ma znacznika <!-- PACZKI --> albo linii const TRYB')
    out = silnik.replace('<!-- PACZKI -->', '\n'.join(paczki), 1)
    out = out.replace("const TRYB='siec';", "const TRYB='plik';", 1)
    out = re.sub(r'<!-- PWA -->.*?<!-- /PWA -->\n?', '', out, count=1, flags=re.S)
    return out


def main(argv):
    if not argv:
        sys.exit(__doc__)
    wynik = argv[-1]
    pliki = argv[:-1]
    if not pliki:
        kat = json.loads(KATALOG.read_text(encoding='utf-8'))
        pliki = [TEMATY / t['plik'] for t in kat['tematy']]
    out = zbuduj(pliki)
    pathlib.Path(wynik).write_text(out, encoding='utf-8')
    print('ok', wynik, len(out))


if __name__ == '__main__':
    main(sys.argv[1:])
