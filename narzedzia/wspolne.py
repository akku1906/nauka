"""Wspólne funkcje narzędzi: odczyt frontmattera tematu i ścieżki repozytorium."""
import pathlib
import re

KORZEN = pathlib.Path(__file__).resolve().parent.parent
TEMATY = KORZEN / 'tematy'
KATALOG = TEMATY / 'index.json'


def frontmatter(tekst):
    """Pary klucz: wartość między pierwszymi liniami '---', tak jak czyta je silnik."""
    linie = tekst.replace('\r', '').lstrip().split('\n')
    meta = {}
    if linie and linie[0].strip() == '---':
        for l in linie[1:]:
            if l.strip() == '---':
                break
            m = re.match(r'^(\w+):\s*(.*)$', l)
            if m:
                meta[m.group(1)] = m.group(2).strip()
    return meta
