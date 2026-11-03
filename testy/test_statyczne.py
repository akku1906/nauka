"""Testy bez przeglądarki: pliki repozytorium, katalog, wersja powłoki, ścieżki."""
import json
import re
import struct
import sys

from pomoc import KORZEN, sprawdz

sys.path.insert(0, str(KORZEN / 'narzedzia'))
import katalog  # noqa: E402
import wersja  # noqa: E402


def test_nojekyll():
    sprawdz((KORZEN / '.nojekyll').exists(), 'brak pliku .nojekyll')


def test_katalog_zgodny_z_plikami():
    zapisany = json.loads((KORZEN / 'tematy' / 'index.json').read_text(encoding='utf-8'))
    sprawdz(zapisany == katalog.zbuduj(), 'tematy/index.json nie zgadza się z frontmatterami, uruchom python3 narzedzia/katalog.py')
    for t in zapisany['tematy']:
        for pole in ('id', 'tytul', 'przedmiot', 'klasa', 'wersja', 'plik'):
            sprawdz(t.get(pole) not in (None, ''), f'{t}: brak pola {pole}')
        sprawdz(re.fullmatch(r'\d{4}-\d{2}-\d{2}', t['wersja']), f"{t['id']}: wersja nie jest datą RRRR-MM-DD")
        sprawdz(re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9._-]*', t['id']), f"{t['id']}: niedozwolone znaki w id")


def test_wersja_powloki_aktualna():
    s = wersja.skrot()
    for n in ('index.html', 'sw.js'):
        sprawdz((wersja.obecna(n) or '').endswith('.' + s),
                f'{n}: WERSJA {wersja.obecna(n)} nie pasuje do skrótu plików {s}, uruchom python3 narzedzia/wersja.py')


def test_tylko_sciezki_wzgledne_i_bez_sieci():
    for n in ('index.html', 'sw.js', 'manifest.webmanifest'):
        t = (KORZEN / n).read_text(encoding='utf-8')
        for m in re.finditer(r'https?://[^\s"\'<>)]+', t):
            sprawdz(m.group(0) == 'http://www.w3.org/2000/svg', f'{n}: adres sieciowy {m.group(0)}')
        for m in re.finditer(r'(?:src|href)=["\'](/[^"\']*)', t):
            raise AssertionError(f'{n}: ścieżka bezwzględna {m.group(1)}')
        for css in re.findall(r'<style>(.*?)</style>', t, flags=re.S):
            sprawdz('@import' not in css and '@font-face' not in css, f'{n}: zewnętrzne style albo fonty')
    sw = (KORZEN / 'sw.js').read_text(encoding='utf-8')
    for m in re.finditer(r"'(/[^']*)'", sw):
        raise AssertionError(f'sw.js: ścieżka bezwzględna {m.group(1)}')


def test_manifest():
    m = json.loads((KORZEN / 'manifest.webmanifest').read_text(encoding='utf-8'))
    sprawdz(m['name'] == 'Nauka', 'name')
    sprawdz(m['start_url'] == './' and m['scope'] == './', 'start_url i scope muszą być ./')
    sprawdz(m['display'] == 'standalone', 'display')
    rozmiary = {(i['sizes'], i.get('purpose', 'any')) for i in m['icons']}
    for wym in (('192x192', 'any'), ('512x512', 'any'), ('512x512', 'maskable')):
        sprawdz(wym in rozmiary, f'brak ikony {wym}')
    for i in m['icons']:
        p = KORZEN / i['src']
        sprawdz(p.exists(), f'brak pliku {i["src"]}')
        dane = p.read_bytes()
        sprawdz(dane[:8] == b'\x89PNG\r\n\x1a\n', f'{i["src"]} nie jest PNG')
        w, h = struct.unpack('>II', dane[16:24])
        sprawdz(f'{w}x{h}' == i['sizes'], f'{i["src"]} ma {w}x{h}, a manifest mówi {i["sizes"]}')


def test_identyfikatory_unikalne_w_temacie():
    for p in sorted((KORZEN / 'tematy').glob('*.md')):
        t = p.read_text(encoding='utf-8')
        ids = re.findall(r'^## .*\{[^}]*#([^}\s]+)[^}]*\}\s*$', t, flags=re.M) + re.findall(r'^- \{#([^}\s]+)\}', t, flags=re.M)
        powt = sorted({i for i in ids if ids.count(i) > 1})
        sprawdz(not powt, f'{p.name}: powtórzone identyfikatory {powt}')


def test_rysunki_w_figurach():
    t = (KORZEN / 'tematy' / 'mat-e8-figury.md').read_text(encoding='utf-8')
    sprawdz(t.count('<svg') == 10 and t.count('</svg>') == 10, 'temat figur powinien mieć 10 rysunków')
