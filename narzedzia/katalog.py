"""Odświeża tematy/index.json na podstawie frontmatterów plików tematy/*.md.

Kolejność tematów z istniejącego katalogu zostaje, nowe pliki trafiają na koniec,
a wpisy bez pliku znikają. Uruchom po dodaniu lub zmianie tematu:

    python3 narzedzia/katalog.py
"""
import json
import sys

from wspolne import KATALOG, TEMATY, frontmatter

POLA = ('id', 'tytul', 'przedmiot', 'klasa', 'wersja')


def wpis(plik):
    meta = frontmatter(plik.read_text(encoding='utf-8'))
    brak = [p for p in POLA if not meta.get(p)]
    if brak:
        sys.exit(f'{plik.name}: brak pól {", ".join(brak)} we frontmatterze')
    w = {p: meta[p] for p in POLA}
    w['klasa'] = int(w['klasa']) if w['klasa'].isdigit() else w['klasa']
    w['plik'] = plik.name
    return w


def zbuduj():
    stare = []
    if KATALOG.exists():
        stare = [t['plik'] for t in json.loads(KATALOG.read_text(encoding='utf-8')).get('tematy', [])]
    pliki = {p.name: p for p in TEMATY.glob('*.md')}
    kolejnosc = [n for n in stare if n in pliki] + sorted(n for n in pliki if n not in stare)
    tematy = [wpis(pliki[n]) for n in kolejnosc]
    ids = [t['id'] for t in tematy]
    if len(set(ids)) != len(ids):
        sys.exit('Powtórzony identyfikator tematu: ' + ', '.join(sorted({i for i in ids if ids.count(i) > 1})))
    return {'format': 1, 'tematy': tematy}


def tekst(kat):
    return json.dumps(kat, ensure_ascii=False, indent=2) + '\n'


if __name__ == '__main__':
    KATALOG.write_text(tekst(zbuduj()), encoding='utf-8')
    print('ok', KATALOG.relative_to(KATALOG.parent.parent))
