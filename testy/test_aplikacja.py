"""Testy w Chromium z emulacją Pixel 7 (dotyk, 412 px), strona pod /nauka/ jak na GitHub Pages.

Numery testów odpowiadają punktom fazy 3 w ZADANIE.md. Testy z PROD=True da się też uruchomić
na adresie produkcyjnym: python3 testy/run.py --url https://akku1906.github.io/nauka/
"""
import json
import pathlib
import re
import subprocess
import sys
import tempfile
import time

from pomoc import (DANE, ID_TEMATOW, KORZEN, TEMATY, Strona, kopia_strony, odpowiedz, otworz_zadanie, sprawdz)
from serwer import SerwerTestowy

TEKST_ZNACZNIKOW = re.compile(r'<\s*/?\s*(svg|line|text|polygon|path|circle|g)\b|&lt;')


class Kontekst:
    """Wspólne zasoby testów: Playwright, przeglądarka, serwer z repozytorium albo adres produkcyjny."""

    def __init__(self, pw, przegladarka, url=None):
        self.pw = pw
        self.b = przegladarka
        self.prod = url is not None
        self._srv = None
        self._url = url

    @property
    def url(self):
        if self._url is None:
            self._srv = SerwerTestowy(KORZEN).start()
            self._url = self._srv.url
        return self._url

    def strona(self, **opcje):
        return Strona(self.pw, self.b, **opcje)

    def zamknij(self):
        if self._srv:
            self._srv.stop()


def start_z_klasa(ctx, s, url=None, klasa='8'):
    s.idz(url or ctx.url)
    s.wybierz_klase(klasa)


# ---------------------------------------------------------------- 1
def test_01_start_bez_bledow_i_lista_tematow(ctx):
    s = ctx.strona()
    try:
        s.idz(ctx.url)
        s.pg.wait_for_selector('[data-klasa="8"]')
        sprawdz(s.pg.locator('[data-klasa="4"]').count() == 1, 'brak wyboru klasy 4')
        s.wybierz_klase('8')
        tematy = s.pg.eval_on_selector_all('[data-temat]', 'e=>e.map(x=>x.dataset.temat)')
        for t in ID_TEMATOW:
            sprawdz(t in tematy, f'na liście brak tematu {t}: {tematy}')
        status = s.pg.inner_text('#status')
        sprawdz('uruchomienie nr 1' in status and 'Pamięć trwała' in status, f'pasek stanu: {status}')
        s.bez_bledow('na starcie')
    finally:
        s.zamknij()


test_01_start_bez_bledow_i_lista_tematow.PROD = True


# ---------------------------------------------------------------- 2
def test_02_kazde_zadanie_dobrze_i_zle(ctx):
    s = ctx.strona()
    try:
        start_z_klasa(ctx, s)
        typy = {}
        for temat in ID_TEMATOW:
            for z in s.zadania(temat):
                typy.setdefault(z['typ'], 0)
                typy[z['typ']] += 1
                for dobrze in (True, False):
                    otworz_zadanie(s, ctx.url, temat, z['id'])
                    oczek = odpowiedz(s, z, dobrze)
                    s.pg.click('[data-akcja="sprawdz"]')
                    s.pg.wait_for_selector('.verdict')
                    glowa = s.pg.inner_text('.verdict .head')
                    sprawdz(glowa == ('Dobrze.' if dobrze else 'Nie tym razem.'), f'{temat}/{z["id"]} ({z["typ"]}) dobrze={dobrze}: werdykt „{glowa}”')
                    html = s.pg.inner_html('.verdict')
                    for frag in oczek:
                        sprawdz(frag in html, f'{temat}/{z["id"]} ({z["typ"]}): w wyjaśnieniu brak „{frag}”\n{html[:400]}')
                    w = s.wpis(temat, z['id'])
                    sprawdz(w and w['last'] == (1 if dobrze else 0), f'{temat}/{z["id"]}: zapis {w}')
                    s.pg.click('[data-akcja="dalej"]')
                    wynik = s.pg.inner_text('.summary-score')
                    sprawdz(wynik == (f'{z["pkt"]} / {z["pkt"]}' if dobrze else f'0 / {z["pkt"]}'), f'{temat}/{z["id"]}: wynik „{wynik}”')
        for typ in ('quiz', 'pf', 'luka', 'kolejnosc', 'pary'):
            sprawdz(typy.get(typ), f'żaden temat nie ma zadania typu {typ}')
        # sprawdzian: 10 zadań, 7 dobrze i 3 źle, punkty liczone na końcu
        s.ekran('#/t/mat-e8-liczby/sprawdzian', ctx.url)
        dane = {z['id']: z for z in s.zadania('mat-e8-liczby')}
        oczek_pkt = mx = 0
        for i in range(10):
            s.pg.wait_for_selector(f'.counter:has-text("zadanie {i + 1} z 10")')
            z = dane[s.pg.get_attribute('.task', 'data-id')]
            odpowiedz(s, z, i < 7)
            mx += z['pkt']
            oczek_pkt += z['pkt'] if i < 7 else 0
            s.pg.click('[data-akcja="sprawdz"]')
        s.pg.wait_for_selector('h1:has-text("Wynik sprawdzianu")')
        wynik = s.pg.inner_text('.summary-score')
        sprawdz(wynik == f'{oczek_pkt} / {mx} pkt', f'sprawdzian: „{wynik}”, oczekiwano {oczek_pkt} / {mx} pkt')
        sprawdz(s.pg.locator('.verdict .head.no').count() == 3, 'sprawdzian: powinny być 3 omówione błędy')
        # fiszki: „Umiem” i „Jeszcze nie” trafiają do zapisu
        s.ekran('#/t/mat-e8-figury/fiszki', ctx.url)
        for umiem in (True, False):
            s.pg.click('button:has-text("Pokaż odpowiedź")')
            fid = s.pg.get_attribute('.card', 'data-id')
            s.pg.click('button:has-text("Umiem")' if umiem else 'button:has-text("Jeszcze nie")')
            w = s.wpis('mat-e8-figury', fid)
            sprawdz(w and w['last'] == (1 if umiem else 0), f'fiszka {fid}: zapis {w}')
        s.bez_bledow('w zadaniach')
    finally:
        s.zamknij()


# ---------------------------------------------------------------- 3
def test_03_liczby_przecinek_kropka_minus(ctx):
    s = ctx.strona()
    try:
        start_z_klasa(ctx, s)
        przypadki = [
            ('k18', ['0,375'], True), ('k18', ['0.375'], True), ('k18', [' 0,3750 '], True), ('k18', ['0,38'], False),
            ('k26', ['-4', '2,5', '-2,5'], True), ('k26', ['−4', '2.5', '–2.5'], True), ('k26', ['4', '2,5', '-2,5'], False),
            ('k13', ['11/12'], True), ('k13', ['11 / 12'], True),
            ('k21', ['2700'], True), ('k23', ['1994', 'mmxxvii'], True),
        ]
        for zid, wpisy, ok in przypadki:
            otworz_zadanie(s, ctx.url, 'mat-e8-liczby', zid)
            pola = s.pg.query_selector_all('input.gap')
            for p, w in zip(pola, wpisy):
                p.click()
                s.pg.keyboard.type(w)  # pisanie z klawiatury, jak na telefonie
            s.pg.click('[data-akcja="sprawdz"]')
            glowa = s.pg.inner_text('.verdict .head')
            sprawdz(glowa == ('Dobrze.' if ok else 'Nie tym razem.'), f'{zid} {wpisy}: „{glowa}”')
            if zid == 'k26' and wpisy[0][0] in '-−–':
                sprawdz(s.pg.input_value('input.gap[data-k="0"]').lstrip().startswith(('-', '−', '–')), 'minus nie został wpisany')
        # klawiatura: z minusem albo ułamkiem pełna, przy nieujemnych liczbach numeryczna
        for zid, tryb in (('k26', 'text'), ('k13', 'text'), ('k23', 'text'), ('k18', 'decimal'), ('k11', 'decimal')):
            otworz_zadanie(s, ctx.url, 'mat-e8-liczby', zid)
            tryby = set(s.pg.eval_on_selector_all('input.gap', 'e=>e.map(x=>x.inputMode)'))
            sprawdz(tryby == {tryb}, f'{zid}: inputmode {tryby}, oczekiwano {tryb}')
        s.bez_bledow()
    finally:
        s.zamknij()


# ---------------------------------------------------------------- 4
def test_04_trwalosc_i_powtorka_bledow(ctx):
    s = ctx.strona()
    try:
        start_z_klasa(ctx, s)
        nr1 = int(re.search(r'uruchomienie nr (\d+)', s.pg.inner_text('#status')).group(1))
        zle = {'mat-e8-liczby': ['k01', 'k03'], 'mat-e8-figury': ['g07']}
        dobre = {'mat-e8-liczby': ['k04'], 'mat-e8-figury': ['g03']}
        for temat in ID_TEMATOW:
            dane = {z['id']: z for z in s.zadania(temat)}
            for zid, ok in [(z, False) for z in zle[temat]] + [(z, True) for z in dobre[temat]]:
                otworz_zadanie(s, ctx.url, temat, zid)
                odpowiedz(s, dane[zid], ok)
                s.pg.click('[data-akcja="sprawdz"]')
                s.pg.wait_for_selector('.verdict')
        s.pg.reload()
        s.pg.wait_for_selector('main#app > *:not(p.counter)')
        s.ekran('#/', ctx.url)
        nr2 = int(re.search(r'uruchomienie nr (\d+)', s.pg.inner_text('#status')).group(1))
        sprawdz(nr2 == nr1 + 1, f'numer uruchomienia {nr1} -> {nr2}')
        for temat in ID_TEMATOW:
            s.ekran(f'#/t/{temat}', ctx.url)
            s.pg.wait_for_selector('[data-w="bledy"]')
            txt = s.pg.inner_text('[data-w="bledy"]')
            sprawdz(f'{len(zle[temat])} do poprawy' in txt, f'{temat}: „{txt}”')
            s.pg.click('[data-w="bledy"]')
            s.pg.wait_for_selector('.task')
            licznik = s.pg.inner_text('.counter')
            pierwsze = s.pg.get_attribute('.task', 'data-id')
            sprawdz(licznik.endswith(f'z {len(zle[temat])}') and pierwsze in zle[temat], f'{temat}: powtórka „{licznik}”, zadanie {pierwsze}')
            s.pg.click('.back')
            sesja = s.pg.evaluate("t=>{const p=nauka.tematy[t];return p.tasks.filter(x=>{const w=nauka.stan.items[t+':'+x.id];return w&&w.last===0}).map(x=>x.id)}", temat)
            sprawdz(sorted(sesja) == sorted(zle[temat]), f'{temat}: błędne w zapisie {sesja}')
        s.bez_bledow()
    finally:
        s.zamknij()


# ---------------------------------------------------------------- 5
def test_05_offline_po_jednym_starcie(ctx):
    srv = None
    if ctx.prod:
        url = ctx.url
    else:
        srv = SerwerTestowy(kopia_strony()).start()
        url = srv.url
    s = ctx.strona()
    try:
        start_z_klasa(ctx, s, url)
        s.czekaj_na_sw()  # ani jeden temat nie był otwierany
        s.ctx.set_offline(True)
        if srv:
            srv.stop()  # prawdziwy brak sieci, także dla service workera
        s.pg.reload()
        s.pg.wait_for_selector('[data-temat]')
        for temat in ID_TEMATOW:
            s.ekran('#/', url)
            s.pg.click(f'[data-temat="{temat}"]')
            s.pg.click('[data-w="kompendium"]')
            s.pg.wait_for_selector('.doc h2')
            z = s.zadania(temat)[0]
            otworz_zadanie(s, url, temat, z['id'])
            odpowiedz(s, z, True)
            s.pg.click('[data-akcja="sprawdz"]')
            sprawdz(s.pg.inner_text('.verdict .head') == 'Dobrze.', f'{temat}: zadanie offline')
        figury = s.pg.evaluate("nauka.tematy['mat-e8-figury'].src.length")
        sprawdz(figury > 1000, 'temat figur nie wczytał się offline')
        s.bez_bledow('offline')
    finally:
        s.zamknij()
        if srv:
            srv.stop()


test_05_offline_po_jednym_starcie.PROD = True


# ---------------------------------------------------------------- 6
def test_06_aktualizacja_tematu_i_aplikacji(ctx):
    kat = kopia_strony()
    srv = SerwerTestowy(kat).start()
    s = ctx.strona()
    try:
        start_z_klasa(ctx, s, srv.url)
        s.czekaj_na_sw()
        z = s.zadania('mat-e8-figury')[0]
        otworz_zadanie(s, srv.url, 'mat-e8-figury', z['id'])
        odpowiedz(s, z, True)
        s.pg.click('[data-akcja="sprawdz"]')
        przed = s.wpis('mat-e8-figury', z['id'])
        # bez sieci
        s.ctx.set_offline(True)
        srv.stop()
        s.pg.reload()
        s.ekran('#/', srv.url)
        s.pg.wait_for_selector('[data-temat]')
        # nowa wersja tematu na serwerze, sieć wraca
        plik = kat / 'tematy' / 'mat-e8-figury.md'
        t = plik.read_text(encoding='utf-8')
        t = t.replace('wersja: ', 'wersja: 2099-01-01\nstara_wersja: ', 1).replace('## Kąty\n', '## Kąty po aktualizacji\n', 1)
        plik.write_text(t, encoding='utf-8')
        idx = json.loads((kat / 'tematy' / 'index.json').read_text(encoding='utf-8'))
        for w in idx['tematy']:
            if w['id'] == 'mat-e8-figury':
                w['wersja'] = '2099-01-01'
        (kat / 'tematy' / 'index.json').write_text(json.dumps(idx, ensure_ascii=False), encoding='utf-8')
        srv.start()
        s.ctx.set_offline(False)
        s.pg.reload()
        s.ekran('#/', srv.url)
        s.pg.wait_for_selector('[data-temat]')
        s.ekran('#/t/mat-e8-figury/kompendium', srv.url)
        s.pg.wait_for_selector('.doc h2')
        sprawdz('Kąty po aktualizacji' in s.pg.inner_text('.doc'), 'nowa treść tematu się nie pojawiła')
        sprawdz(s.pg.evaluate("nauka.tematy['mat-e8-figury'].meta.wersja") == '2099-01-01', 'stara wersja tematu')
        sprawdz(s.wpis('mat-e8-figury', z['id']) == przed, 'postęp zmienił się po aktualizacji tematu')
        # nowa wersja aplikacji: pasek zamiast przeładowania
        stara = s.pg.evaluate('nauka.wersja')
        for n in ('index.html', 'sw.js'):
            p = kat / n
            p.write_text(p.read_text(encoding='utf-8').replace(f"const WERSJA='{stara}';", "const WERSJA='test-nowa';"), encoding='utf-8')
        s.pg.reload()
        s.pg.wait_for_selector('main#app > *:not(p.counter)')
        s.ekran('#/t/mat-e8-liczby/zadanie/k01', srv.url)
        s.pg.wait_for_selector('.task[data-id="k01"]')
        s.pg.click('.opt[data-k="1"]')  # zadanie w trakcie
        s.czekaj("!document.getElementById('aktualizacja').hidden", 'pasek nowej wersji', limit=30)
        sprawdz('Jest nowa wersja, odśwież' in s.pg.inner_text('#aktualizacja'), 'treść paska')
        sprawdz(s.pg.locator('.opt.sel').count() == 1 and s.pg.evaluate('nauka.wersja') == stara, 'strona przeładowała się sama')
        with s.pg.expect_navigation():
            s.pg.click('#aktualizacja button')
        s.pg.wait_for_selector('main#app > *:not(p.counter)')
        sprawdz(s.pg.evaluate('nauka.wersja') == 'test-nowa', 'po odświeżeniu nadal stara wersja')
        sprawdz(s.wpis('mat-e8-figury', z['id']) == przed, 'postęp zmienił się po aktualizacji aplikacji')
        s.bez_bledow()
    finally:
        s.zamknij()
        srv.stop()


# ---------------------------------------------------------------- 7
def test_07_eksport_czyszczenie_import(ctx):
    s = ctx.strona()
    try:
        start_z_klasa(ctx, s)
        for temat, zid, ok in (('mat-e8-liczby', 'k02', True), ('mat-e8-liczby', 'k05', False), ('mat-e8-figury', 'g16', True)):
            z = {x['id']: x for x in s.zadania(temat)}[zid]
            otworz_zadanie(s, ctx.url, temat, zid)
            odpowiedz(s, z, ok)
            s.pg.click('[data-akcja="sprawdz"]')
        s.ekran('#/', ctx.url)
        with s.pg.expect_download() as d:
            s.pg.click('.links button:has-text("Zapisz postęp do pliku")')
        a = json.loads(pathlib.Path(d.value.path()).read_text(encoding='utf-8'))
        sprawdz(a['format'] == 'nauka-postep' and a['wersja'] == 2, 'format eksportu')
        sprawdz(len(a['postep']) == 3, f'eksport ma {len(a["postep"])} wpisów')
        plik = pathlib.Path(tempfile.mkdtemp()) / 'postep.json'
        plik.write_text(json.dumps(a), encoding='utf-8')
        s.pg.evaluate('localStorage.clear()')
        s.pg.reload()
        s.wybierz_klase('8')
        sprawdz(s.pg.evaluate("Object.keys(nauka.stan.items).length") == 0, 'pamięć nie została wyczyszczona')
        s.pg.set_input_files('#plik-postep', str(plik))
        s.pg.wait_for_selector('text=Połączyć z obecnym postępem czy go zastąpić?')
        s.pg.click('button:has-text("Zastąp")')
        s.pg.wait_for_selector('.note')
        with s.pg.expect_download() as d:
            s.pg.click('.links button:has-text("Zapisz postęp do pliku")')
        b = json.loads(pathlib.Path(d.value.path()).read_text(encoding='utf-8'))
        a.pop('eksport')
        b.pop('eksport')
        sprawdz(a == b, f'stan po imporcie różni się:\n{a}\n{b}')
        # stary format z wersji jednoplikowej, łączony z obecnym
        stary = {'eksport': '2026-10-31T10:00:00.000Z', 'stan': {'items': {
            'mat-e8-liczby/k01': {'n': 1, 'ok': 0, 'box': 0, 'last': 0, 't': 1},
            'mat-e8-liczby/f:f02': {'n': 2, 'ok': 2, 'box': 2, 'last': 1, 't': 2},
            'mat-e8-liczby/k02': {'n': 9, 'ok': 0, 'box': 0, 'last': 0, 't': 1}}, 'launches': 50, 'first': '2026-09-01T10:00:00.000Z'}}
        plik.write_text(json.dumps(stary), encoding='utf-8')
        przed_k02 = s.wpis('mat-e8-liczby', 'k02')
        s.pg.set_input_files('#plik-postep', str(plik))
        s.pg.wait_for_selector('text=stary format')
        s.pg.click('button:has-text("Połącz")')
        s.pg.wait_for_selector('.note')
        sprawdz(s.wpis('mat-e8-liczby', 'f02')['box'] == 2, 'fiszka ze starego formatu')
        sprawdz(s.wpis('mat-e8-liczby', 'k01')['n'] == 1, 'zadanie ze starego formatu')
        sprawdz(s.wpis('mat-e8-liczby', 'k02') == przed_k02, 'połączenie nadpisało nowszy wpis starszym')
        status = s.pg.inner_text('#status')
        sprawdz('uruchomienie nr 50' in status and '1.09.2026' in status, f'licznik po połączeniu: {status}')
        s.bez_bledow()
    finally:
        s.zamknij()


# ---------------------------------------------------------------- 8
def test_08_instalowalnosc(ctx):
    """Chrome sam ocenia instalowalność: lista błędów pusta i zdarzenie beforeinstallprompt.
    Wymaga pełnego Chromium (channel="chromium"); zwykły headless shell zwraca pustą listę nawet bez manifestu."""
    profil = tempfile.mkdtemp(prefix='nauka-profil-')
    pc = ctx.pw.chromium.launch_persistent_context(profil, channel='chromium', args=['--bypass-app-banner-engagement-checks'])
    try:
        pg = pc.pages[0] if pc.pages else pc.new_page()
        pg.add_init_script("window.__bip=0;addEventListener('beforeinstallprompt',()=>{window.__bip++;});")
        bledy = []
        pg.on('console', lambda m: bledy.append(m.text) if m.type == 'error' else None)
        pg.goto(ctx.url)
        pg.wait_for_selector('[data-klasa]')
        cdp = pc.new_cdp_session(pg)
        koniec = time.time() + 15
        while time.time() < koniec and not pg.evaluate('window.__bip'):
            time.sleep(0.2)
        bl = cdp.send('Page.getInstallabilityErrors')['installabilityErrors']
        sprawdz(bl == [], f'błędy instalowalności: {bl}')
        sprawdz(pg.evaluate('window.__bip') >= 1, 'Chrome nie zgłosił beforeinstallprompt')
        app = cdp.send('Page.getAppId')
        sprawdz(app.get('appId', '').endswith('/nauka/'), f'identyfikator aplikacji {app} powinien kończyć się na /nauka/, bo domena jest wspólna')
        man = cdp.send('Page.getAppManifest')
        sprawdz(not man.get('errors'), f'błędy manifestu: {man.get("errors")}')
        sprawdz(man['url'].startswith(ctx.url) and man['url'].endswith('manifest.webmanifest'), f'adres manifestu {man["url"]}')
        m = json.loads(man['data'])
        sprawdz(m['name'] == 'Nauka' and m['start_url'] == './' and m['scope'] == './' and m['display'] == 'standalone', f'pola manifestu {m}')
        for ik in m['icons']:
            r = pg.request.get(ctx.url + ik['src'])
            sprawdz(r.status == 200 and r.headers['content-type'].startswith('image/png'), f'ikona {ik["src"]}: {r.status}')
        sprawdz(not bledy, f'błędy konsoli: {bledy}')
    finally:
        pc.close()


test_08_instalowalnosc.PROD = True


# ---------------------------------------------------------------- 9
def test_09_rysunki_w_figurach(ctx):
    s = ctx.strona()
    try:
        start_z_klasa(ctx, s)
        razem = 0
        s.ekran('#/t/mat-e8-figury/kompendium', ctx.url)
        s.pg.wait_for_selector('.doc h2')
        n = s.pg.locator('main svg').count()
        sprawdz(n == 5, f'kompendium: {n} rysunków zamiast 5')
        razem += n
        sprawdz(not TEKST_ZNACZNIKOW.search(s.pg.inner_text('main')), 'kompendium: znacznik wyświetlony jako tekst')
        for zid in ('g03', 'g04', 'g07', 'g12', 'g15'):
            otworz_zadanie(s, ctx.url, 'mat-e8-figury', zid)
            n = s.pg.locator('.task svg').count()
            sprawdz(n == 1, f'{zid}: {n} rysunków')
            bb = s.pg.locator('.task svg').bounding_box()
            sprawdz(bb and bb['width'] > 100 and bb['height'] > 60, f'{zid}: rysunek ma rozmiar {bb}')
            sprawdz(not TEKST_ZNACZNIKOW.search(s.pg.inner_text('main')), f'{zid}: znacznik jako tekst')
            razem += n
        sprawdz(razem == 10, f'razem {razem} rysunków zamiast 10')
        s.bez_bledow()
    finally:
        s.zamknij()


test_09_rysunki_w_figurach.PROD = True


# ---------------------------------------------------------------- 10
def test_10_import_tematu_z_pliku(ctx):
    kat = kopia_strony()
    idx = json.loads((kat / 'tematy' / 'index.json').read_text(encoding='utf-8'))
    idx['tematy'] = [t for t in idx['tematy'] if t['id'] != 'mat-e8-figury']
    (kat / 'tematy' / 'index.json').write_text(json.dumps(idx, ensure_ascii=False), encoding='utf-8')
    (kat / 'tematy' / 'mat-e8-figury.md').unlink()
    srv = SerwerTestowy(kat).start()
    s = ctx.strona()
    try:
        start_z_klasa(ctx, s, srv.url)
        sprawdz(s.pg.locator('[data-temat="mat-e8-figury"]').count() == 0, 'figury nie powinny być w katalogu')
        s.pg.set_input_files('#plik', str(KORZEN / 'tematy' / 'mat-e8-figury.md'))
        s.pg.wait_for_selector('h1:has-text("Figury płaskie")')
        sprawdz('Dodano temat' in s.pg.inner_text('.note'), 'brak komunikatu o dodaniu')
        sprawdz('z pliku' in s.pg.inner_text('.subject'), 'brak oznaczenia „z pliku” na ekranie tematu')
        s.pg.click('[data-w="kompendium"]')
        sprawdz(s.pg.locator('main svg').count() == 5, 'rysunki tematu z pliku')
        s.pg.reload()
        s.pg.wait_for_selector('main#app > *:not(p.counter)')
        s.ekran('#/', srv.url)
        s.pg.wait_for_selector('[data-temat="mat-e8-figury"]')
        sprawdz('z pliku' in s.pg.inner_text('[data-temat="mat-e8-figury"]'), 'brak znaczka „z pliku” na liście')
        sprawdz(s.pg.evaluate("localStorage.getItem('nauka:_plik:mat-e8-figury')||''").startswith('---'), 'temat nie zapisany lokalnie')
        s.bez_bledow()
    finally:
        s.zamknij()
        srv.stop()
    # to samo w wersji jednoplikowej otwieranej z pliku (tak jak testowano na Androidzie)
    d = pathlib.Path(tempfile.mkdtemp())
    subprocess.run([sys.executable, str(KORZEN / 'narzedzia' / 'zbuduj.py'), str(KORZEN / 'tematy' / 'mat-e8-liczby.md'), str(d / 'nauka.html')], check=True, capture_output=True)
    s = ctx.strona()
    try:
        start_z_klasa(ctx, s, (d / 'nauka.html').as_uri())
        sprawdz(s.pg.locator('[data-temat]').count() == 1, 'wersja jednoplikowa: tylko liczby')
        s.pg.set_input_files('#plik', str(KORZEN / 'tematy' / 'mat-e8-figury.md'))
        s.pg.wait_for_selector('h1:has-text("Figury płaskie")')
        s.pg.click('[data-w="kompendium"]')
        sprawdz(s.pg.locator('main svg').count() == 5, 'jednoplikowa: rysunki tematu z pliku')
        s.ekran('#/', '')
        s.pg.wait_for_selector('[data-temat="mat-e8-figury"]')
        sprawdz('jednoplikowa' in s.pg.inner_text('#status'), 'pasek stanu wersji jednoplikowej')
        s.bez_bledow('w wersji jednoplikowej')
    finally:
        s.zamknij()


# ---------------------------------------------------------------- 11
def test_11_brak_kolizji_identyfikatorow(ctx):
    s = ctx.strona()
    try:
        start_z_klasa(ctx, s)
        s.pg.set_input_files('#plik', str(DANE / 'test-kolizja.md'))
        s.pg.wait_for_selector('h1:has-text("Temat testowy")')
        z = {x['id']: x for x in s.zadania('mat-e8-liczby')}['k01']
        otworz_zadanie(s, ctx.url, 'mat-e8-liczby', 'k01')
        odpowiedz(s, z, False)
        s.pg.click('[data-akcja="sprawdz"]')
        sprawdz(s.wpis('mat-e8-liczby', 'k01')['last'] == 0, 'zapis k01 w liczbach')
        sprawdz(s.wpis('test-kolizja', 'k01') is None, 'odpowiedź w liczbach zapisała się w innym temacie')
        z2 = s.zadania('test-kolizja')[0]
        otworz_zadanie(s, ctx.url, 'test-kolizja', 'k01')
        odpowiedz(s, z2, True)
        s.pg.click('[data-akcja="sprawdz"]')
        sprawdz(s.wpis('test-kolizja', 'k01')['last'] == 1 and s.wpis('mat-e8-liczby', 'k01')['last'] == 0, 'kolizja zapisów k01')
        s.ekran('#/t/mat-e8-liczby', ctx.url)
        sprawdz('1 do poprawy' in s.pg.inner_text('[data-w="bledy"]'), 'powtórka błędów liczb')
        s.ekran('#/t/test-kolizja', ctx.url)
        sprawdz('0 do poprawy' in s.pg.inner_text('[data-w="bledy"]'), 'powtórka błędów tematu testowego')
        for k in s.stan():
            sprawdz(re.fullmatch(r'nauka:(_(licznik|ustawienia|migracja)|_plik:[\w.-]+|[A-Za-z0-9][\w.-]*:[^:\s]+)', k), f'klucz poza schematem: {k}')
        # identyfikatory zadań i fiszek nie powtarzają się w żadnym temacie
        for t in ID_TEMATOW:
            ids = s.pg.evaluate("t=>[...nauka.tematy[t].tasks,...nauka.tematy[t].cards].map(x=>x.id)", t)
            sprawdz(len(ids) == len(set(ids)), f'{t}: powtórzone identyfikatory')
        s.bez_bledow()
    finally:
        s.zamknij()


# ---------------------------------------------------------------- dodatkowe
def test_12_dotyk_44px_i_szerokosc_360(ctx):
    s = ctx.strona(szerokosc=360)
    try:
        start_z_klasa(ctx, s)
        widoki = ['#/', '#/ustawienia', '#/t/mat-e8-liczby', '#/t/mat-e8-figury', '#/t/mat-e8-figury/kompendium',
                  '#/t/mat-e8-liczby/kompendium', '#/t/mat-e8-liczby/kartka', '#/t/mat-e8-figury/fiszki']
        widoki += [f'#/t/{t}/zadanie/{z["id"]}' for t in ID_TEMATOW for z in s.zadania(t)]
        problemy = []
        for w in widoki:
            s.ekran(w, ctx.url)
            s.pg.wait_for_selector('main#app > *')
            for runda in range(2):
                male = s.pg.evaluate("""()=>[...document.querySelectorAll('main button,main input,main select,main summary,main a')]
                  .filter(e=>e.offsetParent).map(e=>{const r=e.getBoundingClientRect();return [e.tagName,(e.innerText||e.className||'').trim().slice(0,30),Math.round(r.width),Math.round(r.height)]})
                  .filter(x=>x[2]<44||x[3]<44)""")
                szer = s.pg.evaluate('document.documentElement.scrollWidth')
                if male:
                    problemy.append(f'{w}: małe cele {male}')
                if szer > 360:
                    problemy.append(f'{w}: szerokość strony {szer} px')
                if '/zadanie/' not in w or runda == 1:
                    break
                # drugi pomiar po sprawdzeniu, z wyjaśnieniem i rozwiązaniem
                t, zid = w.split('/')[2], w.split('/')[4]
                z = {x['id']: x for x in s.zadania(t)}[zid]
                odpowiedz(s, z, False)
                s.pg.click('[data-akcja="sprawdz"]')
        sprawdz(not problemy, '\n'.join(problemy[:15]))
        s.bez_bledow()
    finally:
        s.zamknij()


def test_13_migracja_starego_zapisu(ctx):
    s = ctx.strona()
    try:
        s.idz(ctx.url)
        stary = {'v': 1, 'launches': 7, 'first': '2026-10-30T10:00:00.000Z', 'current': 'mat-e8-figury', 'packages': {},
                 'items': {'mat-e8-liczby/k01': {'n': 2, 'ok': 1, 'box': 0, 'last': 0, 't': 5},
                           'mat-e8-figury/f:gf01': {'n': 1, 'ok': 1, 'box': 1, 'last': 1, 't': 6}}}
        s.pg.evaluate("o=>{localStorage.clear();localStorage.setItem('nauka:v1',JSON.stringify(o));localStorage.setItem('nauka:probe','1')}", stary)
        s.pg.reload()
        s.wybierz_klase('8')
        sprawdz(s.wpis('mat-e8-liczby', 'k01') == stary['items']['mat-e8-liczby/k01'], 'migracja zadania')
        sprawdz(s.wpis('mat-e8-figury', 'gf01') == stary['items']['mat-e8-figury/f:gf01'], 'migracja fiszki')
        sprawdz('uruchomienie nr 8' in s.pg.inner_text('#status'), 'licznik po migracji')
        sprawdz(s.pg.evaluate("localStorage.getItem('nauka:v1')") is not None, 'kopia nauka:v1 powinna zostać')
        sprawdz(s.pg.evaluate("localStorage.getItem('nauka:probe')") is None, 'stary klucz próbny')
        s.pg.reload()
        sprawdz(s.wpis('mat-e8-liczby', 'k01')['n'] == 2, 'druga migracja nadpisała dane')
        s.bez_bledow()
    finally:
        s.zamknij()


def test_14_sanityzacja_svg(ctx):
    s = ctx.strona()
    try:
        start_z_klasa(ctx, s)
        s.pg.set_input_files('#plik', str(DANE / 'zly-svg.md'))
        s.pg.wait_for_selector('h1:has-text("Rysunek z pułapkami")')
        s.pg.click('[data-w="kompendium"]')
        s.pg.wait_for_selector('.doc svg')
        for el in s.pg.locator('main svg').first.locator('circle').all():
            el.click(force=True)
        sprawdz(s.pg.evaluate('window.__xss') is None, f'wykonał się kod z pliku: {s.pg.evaluate("window.__xss")}')
        zle = s.pg.evaluate("""()=>{const r=[];document.querySelectorAll('main svg, main svg *').forEach(e=>{
            if(['script','foreignobject','image','a','style','animate','img'].includes(e.localName))r.push(e.localName);
            for(const a of e.attributes){if(/^on/i.test(a.name)||/javascript:|url\\((?!#)/i.test(a.value))r.push(e.localName+'@'+a.name);}});return r}""")
        sprawdz(not zle, f'zostały niebezpieczne elementy: {zle}')
        sprawdz(s.pg.locator('main svg line').count() == 1, 'bezpieczna część rysunku zniknęła')
        sprawdz('<b>' in s.pg.inner_text('.doc'), 'znacznik <b> poza rysunkiem powinien być tekstem')
        sprawdz(s.pg.evaluate("nauka.tematy['test-zly-svg'].warn.some(w=>w.includes('<b>'))"), 'brak ostrzeżenia o znaczniku')
        s.bez_bledow()
    finally:
        s.zamknij()


def test_15_pierwiastek_kreska_nad_calym(ctx):
    s = ctx.strona()
    try:
        start_z_klasa(ctx, s)

        def zmierz(gdzie):
            r = s.pg.evaluate("""()=>[...document.querySelectorAll('main .sq')].map(q=>{const a=q.querySelector('.rs').getBoundingClientRect(),
                b=q.querySelector('.rad').getBoundingClientRect(),st=getComputedStyle(q.querySelector('.rad'));
                return {rs:[a.top,a.bottom,a.right],rad:[b.top,b.bottom,b.left,b.right],kreska:parseFloat(st.borderTopWidth)}})""")
            sprawdz(r, f'{gdzie}: brak pierwiastka')
            for q in r:
                sprawdz(q['kreska'] >= 1, f'{gdzie}: brak kreski')
                sprawdz(abs(q['rs'][0] - q['rad'][0]) <= 1, f'{gdzie}: znak i kreska nie zaczynają się na tej samej wysokości {q}')
                sprawdz(q['rs'][1] >= q['rad'][1] - 1, f'{gdzie}: znak krótszy niż argument {q}')
                sprawdz(abs(q['rs'][2] - q['rad'][2]) <= 1, f'{gdzie}: przerwa między znakiem a kreską {q}')
            return len(r)

        s.ekran('#/t/mat-e8-figury/kompendium', ctx.url)
        s.pg.wait_for_selector('.doc h2')
        zmierz('kompendium')
        otworz_zadanie(s, ctx.url, 'mat-e8-figury', 'g11')
        sprawdz(zmierz('odpowiedzi quizu g11') >= 2, 'quiz g11 powinien mieć pierwiastki w odpowiedziach')
        s.ekran('#/t/mat-e8-figury/fiszki', ctx.url)
        for _ in range(14):
            fid = s.pg.get_attribute('.card', 'data-id')
            s.pg.click('button:has-text("Pokaż odpowiedź")')
            if fid in ('gf06', 'gf07', 'gf08'):
                zmierz('fiszka ' + fid)
            s.pg.click('button:has-text("Umiem")')
        s.bez_bledow()
    finally:
        s.zamknij()


def test_16_parser_bez_ostrzezen(ctx):
    s = ctx.strona()
    try:
        start_z_klasa(ctx, s)
        for t in ID_TEMATOW:
            w = s.pg.evaluate('t=>nauka.tematy[t].warn', t)
            sprawdz(not w, f'{t}: ostrzeżenia parsera {w}')
        s.bez_bledow()
    finally:
        s.zamknij()


def test_17_klasa_4_i_zmiana_klasy(ctx):
    s = ctx.strona()
    try:
        start_z_klasa(ctx, s, klasa='4')
        sprawdz('Tematy wkrótce' in s.pg.inner_text('main'), 'kl. 4 powinna widzieć „Tematy wkrótce”')
        sprawdz(s.pg.locator('[data-temat]').count() == 0, 'kl. 4 widzi tematy kl. 8')
        s.pg.click('.links button:has-text("Ustawienia")')
        s.pg.click('.seg [data-klasa="8"]')
        s.pg.click('.back')
        s.pg.wait_for_selector('[data-temat]')
        sprawdz(s.pg.locator('[data-temat]').count() == len(ID_TEMATOW), 'po zmianie na kl. 8')
        s.pg.reload()
        s.pg.wait_for_selector('[data-temat]')
        s.bez_bledow()
    finally:
        s.zamknij()


def test_18_wstecz_cofa_o_ekran(ctx):
    s = ctx.strona()
    try:
        start_z_klasa(ctx, s)
        s.pg.click('[data-temat="mat-e8-figury"]')
        s.pg.click('[data-w="cwiczenia"]')
        s.pg.wait_for_selector('.task')
        s.pg.go_back()
        s.pg.wait_for_selector('[data-w="kompendium"]')
        s.pg.go_back()
        s.pg.wait_for_selector('[data-temat]')
        s.bez_bledow()
    finally:
        s.zamknij()


def test_19_wybor_pliku_bez_filtra_i_komunikaty(ctx):
    """Android filtruje okno wyboru pliku po typie MIME z atrybutu accept, a .json w Pobranych bywa
    application/octet-stream i wtedy znika z listy. Pola nie mają więc filtra, a zawartość jest sprawdzana po wczytaniu."""
    def plik(nazwa, dane, mime='application/octet-stream'):
        return {'name': nazwa, 'mimeType': mime, 'buffer': dane if isinstance(dane, bytes) else dane.encode('utf-8')}

    s = ctx.strona()
    try:
        start_z_klasa(ctx, s)
        for pole in ('#plik', '#plik-postep'):
            sprawdz(s.pg.get_attribute(pole, 'accept') is None, f'{pole} ma filtr accept')
        z = {x['id']: x for x in s.zadania('mat-e8-liczby')}['k02']
        otworz_zadanie(s, ctx.url, 'mat-e8-liczby', 'k02')
        odpowiedz(s, z, True)
        s.pg.click('[data-akcja="sprawdz"]')
        s.ekran('#/', ctx.url)
        with s.pg.expect_download() as d:
            s.pg.click('.links button:has-text("Zapisz postęp do pliku")')
        postep = pathlib.Path(d.value.path()).read_bytes()
        temat = (KORZEN / 'tematy' / 'mat-e8-figury.md').read_bytes()
        png = (KORZEN / 'ikony' / 'ikona-192.png').read_bytes()
        stary = json.dumps({'eksport': '2026-10-31T10:00:00.000Z', 'stan': {'items': {'mat-e8-liczby/k01': {'n': 1, 'ok': 1, 'box': 1, 'last': 1, 't': 1}}, 'launches': 3, 'first': '2026-10-01T10:00:00.000Z'}})

        # dobre pliki z typem, jaki może nadać Android, albo bez rozszerzenia
        for nazwa, dane, mime in (('postep-2026-11-04.json', postep, 'application/octet-stream'), ('postep', postep, ''),
                                  ('postep-2026-10-31.json', stary, 'application/octet-stream'), ('postep.txt', postep, 'text/plain')):
            s.ekran('#/', ctx.url)
            s.pg.set_input_files('#plik-postep', plik(nazwa, dane, mime))
            s.pg.wait_for_selector('text=Połączyć z obecnym postępem czy go zastąpić?')
            s.pg.click('button:has-text("Anuluj")')
        s.ekran('#/', ctx.url)
        s.pg.set_input_files('#plik', plik('test-kolizja.md', (DANE / 'test-kolizja.md').read_bytes()))
        s.pg.wait_for_selector('h1:has-text("Temat testowy")')

        # złe pliki: czytelny komunikat, nazwa pliku w komunikacie, stan bez zmian
        zle = [
            ('#plik-postep', plik('zdjecie.jpg', png, 'image/jpeg'), 'nie jest plikiem tekstowym'),
            ('#plik-postep', plik('pusty.json', b''), 'jest pusty'),
            ('#plik-postep', plik('mat-e8-figury.md', temat), 'to plik tematu, a nie postęp'),
            ('#plik-postep', plik('inny.json', '{"a": 1}'), 'brakuje w nim danych postępu'),
            ('#plik-postep', plik('notatka.txt', 'lista zakupów: mleko, chleb'), 'nie jest plikiem z postępem'),
            ('#plik-postep', plik('film.mp4', b'x' * (6 * 1024 * 1024)), 'jest za duży'),
            ('#plik', plik('zdjecie.png', png, 'image/png'), 'nie jest plikiem tekstowym'),
            ('#plik', plik('postep.json', postep), 'wygląda na plik z postępem'),
            ('#plik', plik('notatka.txt', 'lista zakupów: mleko, chleb'), 'nie jest plikiem tematu'),
            ('#plik', plik('pusty.md', b''), 'jest pusty'),
        ]
        for widok in ('#/', '#/ustawienia'):
            for pole, dane, oczek in zle:
                s.ekran(widok, ctx.url)
                s.pg.wait_for_selector('#status')
                przed = s.stan()
                s.pg.set_input_files(pole, dane)
                s.pg.wait_for_selector('.note.blad')
                tekst = s.pg.inner_text('.note.blad')
                sprawdz(oczek in tekst and dane['name'] in tekst, f'{pole} {dane["name"]} ({widok}): komunikat „{tekst}”')
                sprawdz(s.pg.get_attribute('.note.blad', 'role') == 'alert', 'komunikat błędu bez role=alert')
                sprawdz(s.stan() == przed, f'{pole} {dane["name"]}: zły plik zmienił zapis')
                sprawdz(s.pg.locator('#status').count() == 1, f'{pole} {dane["name"]}: komunikat nie na tym samym ekranie')
        # wklejony tekst też dostaje czytelny komunikat
        s.ekran('#/ustawienia', ctx.url)
        s.pg.click('summary:has-text("Wklej postęp jako tekst")')
        s.pg.fill('#postep-tekst', 'to nie jest postęp')
        s.pg.click('button:has-text("Wczytaj tekst")')
        sprawdz('Wklejony tekst nie jest plikiem z postępem' in s.pg.inner_text('.note.blad'), 'komunikat dla wklejonego tekstu')
        s.bez_bledow()
    finally:
        s.zamknij()


test_19_wybor_pliku_bez_filtra_i_komunikaty.PROD = True
