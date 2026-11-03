"""Wspólne narzędzia testów: kopia repozytorium na serwerze, telefon Pixel 7, zbieranie błędów konsoli,
rozwiązywanie zadań dobrze i źle na podstawie danych sparsowanych przez samą aplikację."""
import json
import pathlib
import shutil
import tempfile
import time

from serwer import SerwerTestowy

KORZEN = pathlib.Path(__file__).resolve().parent.parent
DANE = pathlib.Path(__file__).resolve().parent / 'dane'
PLIKI_STRONY = ['index.html', 'sw.js', 'manifest.webmanifest', '.nojekyll', 'ikony', 'tematy']
TEMATY = json.loads((KORZEN / 'tematy' / 'index.json').read_text(encoding='utf-8'))['tematy']
ID_TEMATOW = [t['id'] for t in TEMATY]


class Niepowodzenie(AssertionError):
    pass


def sprawdz(warunek, opis):
    if not warunek:
        raise Niepowodzenie(opis)


def kopia_strony():
    """Kopia plików strony w katalogu tymczasowym, żeby test mógł ją zmieniać."""
    d = pathlib.Path(tempfile.mkdtemp(prefix='nauka-'))
    for n in PLIKI_STRONY:
        z = KORZEN / n
        if z.is_dir():
            shutil.copytree(z, d / n)
        else:
            shutil.copy2(z, d / n)
    return d


class Strona:
    """Jeden kontekst przeglądarki (jak jeden telefon) z jedną kartą i dziennikiem błędów konsoli."""

    def __init__(self, pw, przegladarka, szerokosc=None, **opcje):
        dev = dict(pw.devices['Pixel 7'])
        if szerokosc:
            dev['viewport'] = {'width': szerokosc, 'height': dev['viewport']['height']}
        dev.update(opcje)
        self.ctx = przegladarka.new_context(accept_downloads=True, **dev)
        self.pg = self.ctx.new_page()
        self.bledy = []
        self.pg.on('console', lambda m: self.bledy.append(f'{m.type}: {m.text}') if m.type in ('error', 'warning') else None)
        self.pg.on('pageerror', lambda e: self.bledy.append(f'pageerror: {e}'))
        self.pg.on('dialog', lambda d: d.accept())

    def zamknij(self):
        self.ctx.close()

    def bez_bledow(self, gdzie=''):
        sprawdz(not self.bledy, f'błędy konsoli {gdzie}: {self.bledy}')

    def idz(self, url):
        self.pg.goto(url)
        self.pg.wait_for_selector('main#app > *:not(p.counter)', timeout=15000)

    def ekran(self, adres_hash, baza):
        """Przejście na ekran po adresie (#/...) bez przeładowania strony."""
        self.pg.evaluate("h=>{history.pushState({d:1},'',h);dispatchEvent(new PopStateEvent('popstate',{state:{d:1}}));}", adres_hash)

    def wybierz_klase(self, k='8'):
        self.pg.click(f'[data-klasa="{k}"]')
        self.pg.wait_for_selector('h1:has-text("Tematy")')

    def stan(self):
        return self.pg.evaluate("()=>Object.fromEntries(Object.keys(localStorage).filter(k=>k.startsWith('nauka:')).map(k=>[k,localStorage.getItem(k)]))")

    def wpis(self, temat, id_):
        r = self.pg.evaluate("k=>localStorage.getItem(k)", f'nauka:{temat}:{id_}')
        return json.loads(r) if r else None

    def zadania(self, temat):
        return self.pg.evaluate("""id=>nauka.tematy[id].tasks.filter(t=>['quiz','pf','luka','kolejnosc','pary'].includes(t.typ))
            .map(t=>({id:t.id,typ:t.typ,pkt:t.pkt,options:t.options,statements:t.statements,answers:t.answers,items:t.items,pairs:t.pairs}))""", temat)

    def czekaj(self, js, opis, limit=20.0, arg=None):
        """Odpytuje wyrażenie JS (może być async) aż zwróci prawdę."""
        koniec = time.time() + limit
        while time.time() < koniec:
            try:
                if self.pg.evaluate(js, arg):
                    return
            except Exception:
                pass
            time.sleep(0.2)
        raise Niepowodzenie('nie doczekano się: ' + opis)

    def czekaj_na_sw(self, tematy=None):
        tematy = tematy if tematy is not None else [t['plik'] for t in TEMATY]
        self.czekaj("""async pliki=>{const r=await navigator.serviceWorker.getRegistration();
            if(!r||!r.active||r.active.state!=='activated'||!navigator.serviceWorker.controller)return false;
            const c=await caches.open('nauka-tematy');const ks=(await c.keys()).map(x=>x.url);
            return ks.some(u=>u.endsWith('tematy/index.json'))&&pliki.every(p=>ks.some(u=>u.endsWith('tematy/'+p)));}""",
                    'aktywny service worker i wszystkie tematy w pamięci', arg=tematy)


def otworz_zadanie(s, baza, temat, id_):
    s.ekran(f'#/t/{temat}/zadanie/{id_}', baza)
    s.pg.wait_for_selector(f'.task[data-id="{id_}"]')


def odpowiedz(s, z, dobrze):
    """Rozwiązuje otwarte zadanie z dobrze albo źle. Zwraca fragmenty, które muszą się pojawić w wyjaśnieniu błędu."""
    pg = s.pg
    typ = z['typ']
    oczekiwane = []
    if typ == 'quiz':
        opts = z['options']
        k = next(i for i, o in enumerate(opts) if o['correct']) if dobrze else next(i for i, o in enumerate(opts) if not o['correct'])
        pg.click(f'.opt[data-k="{k}"]')
        if not dobrze:
            fb = opts[k]['fb']
            oczekiwane.append(pg.evaluate('t=>inline(t)', fb) if fb else 'Wybrano')
    elif typ == 'pf':
        for i, st in enumerate(z['statements']):
            v = st['val']
            if not dobrze and i == 0:
                v = 'F' if v == 'P' else 'P'
            pg.click(f'.pf .row[data-k="{i}"] button[data-v="{v}"]')
        if not dobrze:
            st = z['statements'][0]
            oczekiwane += ['Źle ocenione', pg.evaluate('t=>inline(t)', st['text']) + ': to ' + ('prawda' if st['val'] == 'P' else 'fałsz')]
    elif typ == 'luka':
        inputs = pg.query_selector_all('input.gap')
        sprawdz(len(inputs) == len(z['answers']), f"{z['id']}: {len(inputs)} pól, a odpowiedzi {len(z['answers'])}")
        for i, inp in enumerate(inputs):
            inp.fill('12345' if (not dobrze and i == 0) else z['answers'][i][0])
        if not dobrze:
            oczekiwane.append('pisano „12345”, a poprawnie')
    elif typ == 'kolejnosc':
        n = len(z['items'])
        kolej = list(range(n)) if dobrze else list(reversed(range(n)))
        for k in kolej:
            pg.click(f'.pool .chip[data-k="{k}"]')
        if not dobrze:
            oczekiwane += ['Na złym miejscu', 'Dobra kolejność']
    elif typ == 'pary':
        n = len(z['pairs'])
        cel = list(range(n))
        if not dobrze:
            cel[0], cel[1] = cel[1], cel[0]
        for k in range(n):
            pg.click(f'.pairs .col:first-child .chip[data-k="{k}"]')
            pg.click(f'.pairs .col:last-child .chip[data-k="{cel[k]}"]')
        if not dobrze:
            oczekiwane += ['Źle połączone', 'A ' + pg.evaluate('t=>inline(t)', z['pairs'][0][0]) + ': połączono z']
    else:
        raise Niepowodzenie('nieznany typ ' + typ)
    return oczekiwane
