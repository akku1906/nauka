# Raport z sesji: audyt, PWA, wdrożenie

Sesja w chmurze, 3 listopada 2026. Pracowałem sam, według `ZADANIE.md`, faza po fazie. Każda decyzja jest w sekcji „Decyzje”, a każda przeszkoda w sekcji „Ściany”.

## Podsumowanie

- Aplikacja działa pod adresem **https://akku1906.github.io/nauka/** jako instalowalna PWA. Wszystkie pliki zwracają 200, a ich zawartość jest identyczna z repozytorium.
- Testy lokalne: **28 z 28** (`python3 testy/run.py`). Testy na adresie produkcyjnym: **4 z 4** (1, 5, 8, 9).
- Najważniejsze naprawy: rysunki SVG wyświetlały się jako tekst; nie było importu postępu; przycisk wstecz zamykał aplikację; klucze zapisu niezgodne z `CLAUDE.md` (teraz `nauka:<temat>:<id>`, z migracją); identyfikator aplikacji w manifeście byłby wspólny dla całej domeny; temat figur uczył twierdzenia odwrotnego do Pitagorasa, wyłączonego z podstawy; rysunek w `g04` przeczył danym.
- Do sprawdzenia na telefonie: klawiatura z minusem w zadaniu `k26`, instalacja i ikona, import postępu ze starej wersji przez systemowy wybór pliku, pamięć trwała, tryb samolotowy, przycisk wstecz. Instrukcja krok po kroku jest niżej.

## Przebieg i commity

| kolejność | commit | co |
|---|---|---|
| 1 | [`62e5693`](https://github.com/akku1906/nauka/commit/62e569366cadee50acb00532ae24a67146f0239b) | faza 0: inwentaryzacja, opis silnika |
| 2 | [`52d9b35`](https://github.com/akku1906/nauka/commit/52d9b35719d3adad37f293e2bd5c199f0595f878) | faza 1: audyt i poprawki w `silnik.html` |
| 3 | [`b4b2a36`](https://github.com/akku1906/nauka/commit/b4b2a36c3d5c7b918442f7edc38e6af510cf6a62) | faza 2: nowy układ repozytorium, PWA, import i eksport, `docs/FORMAT.md` |
| 4 | [`33cdba6`](https://github.com/akku1906/nauka/commit/33cdba6a09160a0297d1480d5ad4c0816d343aa2) | sprzątanie: `__pycache__` i `.gitignore` |
| 5 | [`5626d37`](https://github.com/akku1906/nauka/commit/5626d37acc747ec9776c04705227f12ee83404fb) | faza 3: testy, poprawki znalezione przez testy (ostrzeżenia parsera, `id` manifestu) |
| 6 | [`0212844`](https://github.com/akku1906/nauka/commit/0212844f9ab03dc2ce5fbc6db2d4aba01cfc5593) | faza 4: audyt treści, poprawki w temacie figur, test treści |
| 7 | [`8d7fb81`](https://github.com/akku1906/nauka/commit/8d7fb81e235503b273bfc5287f069c32c8e8100a) | instrukcja dla rodzica; ten stan poszedł na `main` |
| 8 | ostatni commit z tym raportem | faza 6: raport końcowy |

Praca szła na gałęzi `claude/amazing-wozniak-huup95`, wypychanej po każdej fazie. Wdrożenie: zwykły push tej gałęzi na `main` (przewinięcie, bez merge commita), bo `main` był jej przodkiem.

## Faza 0: inwentaryzacja

### Która wersja silnika jest najnowsza

Zbudowałem `python3 zbuduj.py mat-e8-liczby.md wynik.html` i porównałem z `aplikacja.html`. Pliki są identyczne bajt w bajt (md5 `064cd6423f8a84170ee43183ff94dc3c` w obu). Silnik wycięty z obu plików jest taki sam, a wbudowany temat to dokładnie `mat-e8-liczby.md`. Przycisk „Dodaj temat z pliku” jest już w `silnik.html`. Wniosek: `silnik.html` jest aktualnym źródłem prawdy, nie trzeba niczego wyodrębniać z `aplikacja.html`.

### Co robi silnik (stan wejściowy)

Cały silnik to jeden plik HTML z CSS i JS, bez zależności. Tematy są wklejane przez `zbuduj.py` jako `<script type="text/markdown" class="paczka">` w miejsce znacznika `<!-- PACZKI -->`.

**Parser pliku tematu** (`parsePackage`). Frontmatter między `---` to pary `klucz: wartość`, bez cudzysłowów i list. Potem sekcje `# Kompendium`, `# Zadania`, `# Fiszki` (nazwy sekcji porównywane małymi literami). Kompendium dzieli się na działy po `## `. Zadanie zaczyna się od `## Tytuł [n pkt] {typ #id}`, a `### Rozwiązanie` przełącza zbieranie linii do rozwiązania. Fiszka to linia `- {#id} przód :: tył`. Brakujące pola, puste rozwiązania, złe quizy i powtórzone identyfikatory trafiają do listy ostrzeżeń, którą ekran tematu pokazuje na dole.

**Bloki Markdown** (`parseBlocks`): akapit (kolejne linie sklejane spacją), wzór blokowy `$$ ... $$` w jednej linii, tabela `| a | b |` z separatorem `|---|`, cytat `>`, lista `- ` i lista numerowana `1. `. Wewnątrz tekstu: `**pogrubienie**`, `*kursywa*`, ` - ` zamieniane na półpauzę. Cały tekst jest najpierw escapowany, więc surowy HTML wyświetla się jako tekst.

**Formuły** (`formula`): własny mały parser, bez KaTeX. `$...$` w tekście i `$$...$$` jako blok. Obsługuje `\frac{a}{b}` (ułamek piętrowy z kreską), `\sqrt{x}` (znak √ i kreska `border-top` nad argumentem), `\pi`, `^` i `_` z grupą `{}` albo jednym znakiem, `*` jako `·`, `-` jako `−`, pojedyncze litery kursywą, a słowa wieloliterowe (NWD) prosto. Dwie i więcej spacji dają szeroką spację.

**Typy zadań** i ocenianie:

| typ | jak się odpowiada | kiedy dobrze | co mówi przy błędzie |
|---|---|---|---|
| `quiz` | wybór jednej z przetasowanych odpowiedzi | wybrana jest oznaczona `[x]` | wyjaśnienie `>` przypięte do błędnej odpowiedzi |
| `pf` | Prawda albo Fałsz przy każdym zdaniu | wszystkie zdania dobrze, punkt za komplet | lista wszystkich zdań z poprawną oceną |
| `luka` | pola tekstowe w miejscu `___[odp]` | każde pole pasuje do jednej z odpowiedzi `a\|b` po normalizacji | lista wszystkich poprawnych odpowiedzi |
| `kolejnosc` | stukanie kroków w kolejności | kolejność jak w pliku | pełna dobra kolejność |
| `pary` | stuknięcie lewego, potem prawego | wszystkie pary dobre | lista wszystkich dobrych par |
| `pisemne` | brak, zadanie „Na kartce” z rozwinięciem rozwiązania | nie jest oceniane | nie dotyczy |

Normalizacja odpowiedzi w lukach: małe litery, usunięcie wszystkich spacji, kropka zamieniana na przecinek, znak `−` na `-`. Dzięki temu `2.5` i `2,5` oraz `10 000` i `10000` są równoważne.

**Tryby**: „Ćwiczenia” (10 zadań, najpierw błędne i nieruszane, potem te z najniższym pudełkiem), „Powtórka błędów”, „Sprawdzian” (10 losowych, ocena na końcu, punkty z `[n pkt]`), „Fiszki” (Umiem / Jeszcze nie), „Kompendium”, „Na kartce”.

**Model zapisu**. Jeden klucz `localStorage` `nauka:v1`, w nim cały stan jako JSON:

```
{ v:1, launches:N, first:ISO, current:"<id tematu>",
  items:   { "<temat>/<id>": {n, ok, box, last, t} },
  packages:{ "<temat>": "<pełny tekst pliku .md>" } }
```

`n` to liczba podejść, `ok` liczba dobrych, `box` pudełko Leitnera 0–5 (dobrze +1, źle 0), `last` 1 lub 0 dla ostatniej odpowiedzi, `t` znacznik czasu. Fiszki mają w kluczu przedrostek `f:`, np. `mat-e8-liczby/f:f01`. „Opanowane” to `box ≥ 2`. Przy każdym starcie `launches` rośnie o jeden, a pasek stanu pokazuje numer uruchomienia i datę pierwszego. Klucz próbny `nauka:probe` sprawdza, czy zapis w ogóle działa.

**Eksport**: „Zapisz postęp do pliku” pobiera `postep-RRRR-MM-DD.json` w postaci `{eksport, stan:{items, launches, first}}`. Gdy pobieranie się nie uda, pokazuje tekst do skopiowania. **Importu postępu nie ma**, choć `CLAUDE.md` o nim wspomina.

**Import tematu z pliku**: ukryte `<input type="file">`, plik jest parsowany, jego tekst trafia do `S.packages[id]`, temat staje się bieżący. Przy dwóch tematach o tym samym `id` wygrywa wyższa `wersja` (porównanie tekstowe). Przy więcej niż jednym temacie ekran główny pokazuje listę rozwijaną.

### Tematy

| temat | quiz | pf | luka | kolejnosc | pary | pisemne | fiszki | `<svg>` |
|---|---|---|---|---|---|---|---|---|
| `mat-e8-liczby` | 8 | 3 | 9 | 2 | 3 | 1 | 14 | 0 |
| `mat-e8-figury` | 9 | 3 | 10 | 1 | 2 | 1 | 14 | 10 |

W figurach jest 5 rysunków w kompendium i 5 w zadaniach (`g03`, `g04`, `g07`, `g12`, `g15`).

## Faza 1: audyt kodu

Metoda: zbudowałem wersję jednoplikową z oboma tematami i przeszedłem ją w Chromium z emulacją Pixel 7 przy szerokości 412 i 360 px. Mierzyłem wymiary każdego widocznego przycisku, pola i linku, szerokość przewijania strony, błędy konsoli i to, czy w tekście strony pojawiają się znaczniki. Pierwiastek oceniłem na zrzutach ekranu przed i po.

### Znaleziska

| nr | waga | znalezisko | co zrobiłem |
|---|---|---|---|
| A1 | krytyczne | Surowy `<svg>` z pliku figur wyświetla się jako tekst (parser escapuje wszystko). Zero rysunków na ekranie, a zadania `g03`, `g04`, `g07`, `g12`, `g15` są bez rysunku nierozwiązywalne. Przy 360 px tekst znaczników rozpychał „Pole trapezu” do 401 px. | Nowy typ bloku `svg`: linia zaczynająca się od `<svg` otwiera blok, który trwa do `</svg>`. Sanityzacja przez `DOMParser` i białą listę elementów SVG (`svg`, `g`, `line`, `polygon`, `path`, `circle`, `text` i kilka innych). Usuwane są: wszystko spoza listy (`script`, `foreignObject`, `image`, `a`, `style`, `animate`), atrybuty `on*`, wartości z `javascript:`, `data:`, `expression(`, `@import`, `url(` innym niż `url(#…)`, a `href` tylko w postaci `#kotwica`. Wynik przechodzi sanityzację drugi raz i musi wyjść identyczny, inaczej rysunek jest odrzucany (obrona przed mutacją przy ponownym parsowaniu). Rysunki działają w kompendium, treści zadań, rozwiązaniach i zadaniach „Na kartce”, także w lukach. |
| A2 | krytyczne | Nie ma importu postępu, choć `CLAUDE.md` zakłada, że jest. Bez niego postępu z wersji otwieranej z pliku nie da się przenieść do wersji z sieci. | Format eksportu 2 już w tej fazie. Import z wyborem „zastąp albo połącz” dochodzi w fazie 2. |
| A3 | ważne | Klucze zapisu. Postęp był kluczowany parą temat i identyfikator (`mat-e8-liczby/k01`), więc kolizji między tematami nie było. Ale cały stan, łącznie z pełnym tekstem tematów wgranych z pliku, siedział w jednym kluczu `nauka:v1` i był przepisywany przy każdej odpowiedzi. Uszkodzenie tego jednego JSON-a kasuje wszystko. Format nie zgadzał się też z kontraktem z `CLAUDE.md`. | Osobny klucz na element: `nauka:<temat>:<id>`. Dane aplikacji pod `nauka:_licznik`, `nauka:_ustawienia`, `nauka:_plik:<temat>`, `nauka:_migracja`. Fiszki tracą wewnętrzny przedrostek `f:` (parser i tak pilnuje unikalności identyfikatorów w temacie). Migracja: przy pierwszym starcie stary `nauka:v1` jest przepisywany na nowe klucze, a sam zostaje nietknięty jako kopia. Sprawdzone: licznik 7 po migracji i starcie daje 8, data pierwszego uruchomienia i bieżący temat zostają. |
| A4 | ważne | Pierwiastek. Kreska jest nad całym argumentem, także w odpowiedziach quizu i fiszkach (wszędzie idzie przez ten sam `inline`). Ale to `border-top` nad glifem √, więc kreska wisi wyżej niż haczyk znaku i między nimi jest przerwa. | Znak pierwiastka rysowany maską CSS (SVG w `data:`, bez sieci), rozciąganą do wysokości argumentu. Kreska jest górną krawędzią argumentu, więc łączy się ze znakiem także nad ułamkiem. Przeglądarka bez masek dostaje zwykły glif √. Odpowiedzi z luk pokazywane w wyjaśnieniu błędu przechodzą przez parser wzorów, jeśli mają `\`, `^` albo `_`. |
| A5 | ważne | Pola luk nie mają `inputmode`, więc Android otwiera pełną klawiaturę na literach. Żadne zadanie nie miało ujemnej odpowiedzi do wpisania, więc minusa nie dało się nawet sprawdzić. Normalizacja nie znała półpauzy ani twardej spacji, a „0,50” nie równało się „0,5”. | Klawiatura dobierana na całe zadanie: `decimal`, gdy wszystkie odpowiedzi są nieujemnymi liczbami dziesiętnymi, a pełna `text`, gdy jest minus, ułamek albo litery. Liczby porównywane jako liczby, każdy rodzaj myślnika to minus, twarde spacje usuwane. Enter w luce sprawdza zadanie. Pole luki ma stałą szerokość startową i rośnie przy pisaniu (wcześniej szerokość zdradzała długość odpowiedzi). Nowe zadanie `k26` z ujemnymi wynikami w temacie liczb. |
| A6 | ważne | Cele dotyku poniżej 44 px: linki w stopce 21 px, „‹ Wróć” 35 px, Prawda/Fałsz 37 px, pola luk 33 px, lista tematów 36 px, linki spisu treści i „Rozwiązanie” niższe niż 44 px. | Wszystkie mają teraz co najmniej 44 px. Po poprawce skrypt nie znajduje żadnego mniejszego celu na żadnym widoku. |
| A7 | ważne | Wyjaśnienie błędu w `pf`, `luka`, `kolejnosc` i `pary` było ogólne: zawsze pełna lista poprawnych odpowiedzi, bez wskazania, co dokładnie jest źle. | `pf`: tylko źle ocenione zdania z tym, co zaznaczono. `luka`: „Luka 2: wpisano „x”, a poprawnie „y””. `kolejnosc`: które kroki są na złym miejscu i pełna dobra kolejność. `pary`: które połączenie jest złe i co pasuje. `quiz` bez wyjaśnienia przy odpowiedzi podaje wybraną i poprawną. |
| A8 | ważne | Przycisk wstecz na Androidzie zamyka aplikację, bo silnik nie używa historii przeglądarki. W trybie zainstalowanym dziecko jednym ruchem wychodzi z zadania. | Naprawione w fazie 2 razem z nowym układem ekranów. |
| A9 | kosmetyczne | `rPairs` miał pusty warunek na nagłówki kolumn, więc nagłówki tabeli par nie były pokazywane. | Nagłówki kolumn nad parami. |
| A10 | kosmetyczne | Wersje tematów porównywane tekstowo. Działa tylko dla dat `RRRR-MM-DD`. | Zostaje, opisane w `docs/FORMAT.md` jako wymóg. Przy remisie wersji wygrywa temat wbudowany lub z katalogu. |
| A11 | kosmetyczne | „Powtórka błędów” przy błędnych zadaniach pomija błędne fiszki, pokazuje je dopiero, gdy błędnych zadań nie ma. | Bez zmian. Fiszki i tak są sortowane od najniższego pudełka. |
| A12 | kosmetyczne | Parser nie ostrzegał o znacznikach HTML poza `<svg>`, niezamkniętym `<svg>`, dwukropku w identyfikatorze ani złym `id` tematu. | Cztery nowe ostrzeżenia. |

**Zależności zewnętrzne**: brak. Nie ma `@font-face`, CDN ani analityki. Fonty: treść `system-ui, Roboto, "Segoe UI", sans-serif`, nagłówki i wzory `"Noto Serif", Georgia, serif`. Na Androidzie ogólna rodzina `serif` to systemowy Noto Serif, więc fallback jest właściwy. Atrybut `xmlns` w rysunkach to przestrzeń nazw, nie żądanie sieciowe.

**Błędy konsoli**: zero, przed i po poprawkach, na ekranie głównym, w kompendium, w dziesięciu losowych zadaniach z każdym typem i w fiszkach.

**Poziome przewijanie przy 360 px**: po poprawce A1 zero na wszystkich sprawdzonych widokach.

`testy/run.py` jeszcze nie istniał, więc zmiany w tej fazie sprawdzałem skryptami doraźnymi (pomiary jak wyżej, migracja ze starego zapisu, sanityzacja złośliwego SVG, wpisywanie `-4`, `2.5`, `−2,5`). Pełny zestaw testów powstaje w fazie 3.

## Faza 2: struktura repozytorium i PWA

Układ jest taki jak w zadaniu. `silnik.html` przeniosłem do `index.html` (`git mv`, historia zostaje), `zbuduj.py` do `narzedzia/`, tematy do `tematy/`. `aplikacja.html` usunąłem, bo była identyczna z tym, co buduje skrypt, i jest w historii gita.

**Silnik w działaniu** (`index.html`):

- Przy starcie pobiera `tematy/index.json`, a potem wszystkie wymienione tam pliki `.md`, i parsuje je w przeglądarce. Temat, którego nie udało się pobrać, jest na liście jako „niedostępny bez internetu”.
- Przy pierwszym uruchomieniu pyta o klasę (8 albo 4). Zmiana w „Ustawieniach”. Kl. 4 widzi „Tematy wkrótce”, bo w katalogu nie ma jej tematów.
- Ekrany mają adresy po `#` (`#/t/mat-e8-figury/kompendium`, `#/ustawienia`), a każde przejście dokłada wpis historii. Systemowy przycisk wstecz cofa więc o jeden ekran, zamiast zamykać aplikację (znalezisko A8). Spis treści kompendium przewija stronę przyciskami, a nie linkami `#r1`, które kolidowałyby z adresami ekranów. Adres `#/t/<temat>/zadanie/<id>` otwiera jedno zadanie (przydaje się w testach i kiedyś w kodzie QR na wydruku).
- „Dodaj temat z pliku” zostaje. Temat z pliku leży w `nauka:_plik:<id>`, ma na liście znaczek „z pliku” i jest widoczny w każdej klasie. Można go usunąć w ustawieniach, postęp zostaje.
- Pasek stanu: „Zapis postępu działa. To uruchomienie nr N, pierwsze D. Pamięć trwała: tak/nie. Wersja RRRR-MM-DD.skrót.” Przy starcie aplikacja woła `navigator.storage.persisted()`, a jeśli zwróci `false`, to `persist()`.
- Eksport zapisuje `nauka-postep-RRRR-MM-DD.json` w formacie 2 (opis w `docs/FORMAT.md`), razem z tematami z pliku. Import (stopka i ustawienia, a w ustawieniach także wklejenie tekstu) rozpoznaje format 2, stary eksport `{eksport, stan:{items, launches, first}}` i surowy stan `nauka:v1`, pokazuje podsumowanie i pyta „Połącz” albo „Zastąp”.
- Wersja jednoplikowa (`python3 narzedzia/zbuduj.py wynik.html`) ma te same funkcje poza katalogiem i service workerem. Skrypt podmienia `const TRYB='siec'` na `'plik'` i wycina odnośniki do manifestu i ikon, których z pliku nie da się wczytać.

**Service worker** (`sw.js`):

- Instalacja zapisuje powłokę (`index.html`, manifest, cztery ikony) z pominięciem pamięci HTTP (`cache:'reload'`) i od razu pobiera katalog oraz wszystkie tematy.
- Nawigacja do `./` i `./index.html` dostaje powłokę z pamięci. Inne pliki pod `/nauka/` (np. `docs/RAPORT.md`) idą do sieci.
- `tematy/index.json` i `tematy/*.md`: najpierw sieć z rewalidacją (`cache:'no-cache'`, więc 10-minutowa pamięć HTTP Pages nie opóźnia nowych tematów), odpowiedź trafia do pamięci `nauka-tematy`. Bez sieci albo gdy sieć nie odpowie w 4 sekundy, temat przychodzi z pamięci, a pobieranie trwa dalej w tle. Każde pobranie katalogu z sieci uruchamia pobranie wszystkich tematów z katalogu, także tych, których uczennica nie otwierała.
- Pamięć powłoki ma wersję w nazwie (`nauka-powloka-<WERSJA>`). Nowy `sw.js` instaluje się w tle i czeka. Aplikacja pokazuje wtedy na dole pasek „Jest nowa wersja, odśwież.” z przyciskiem. Dopiero stuknięcie aktywuje nową wersję i przeładowuje stronę. Zamknięcie i ponowne otwarcie aplikacji też ją aktywuje. Stare pamięci powłoki są kasowane przy aktywacji.
- `WERSJA` w `sw.js` i `index.html` ustawia `narzedzia/wersja.py`: data i skrót SHA-256 plików powłoki. Test sprawdza, że skrót zgadza się z plikami, więc zmiana `index.html` bez nowej wersji nie przejdzie testów.

**Manifest**: `name` i `short_name` „Nauka”, `start_url` i `scope` równe `./`, `id` równe `nauka/` (poprawione w fazie 3, decyzja 17), `display: standalone`, `lang: pl`, ikony 192 i 512 (`any`) oraz 192 i 512 (`maskable`). Ikony rysuje `narzedzia/ikony.py`: kartka w kratkę z marginesem, żółtym zakreśleniem i zielonym ptaszkiem na granatowym tle, bez tekstu. W wersji maskable kartka mieści się w bezpiecznym kole.

**Narzędzia**: `narzedzia/katalog.py` (katalog z frontmatterów), `narzedzia/wersja.py` (wersja powłoki), `narzedzia/ikony.py`, `narzedzia/zbuduj.py`, `testy/serwer.py` (serwer jak Pages pod `/nauka/`, z `Cache-Control: max-age=600`).

Sprawdzone w tej fazie próbą dymną (pełne testy w fazie 3): wybór klasy, lista z oboma tematami, przejście wstecz o ekran, aktywny service worker i obie pamięci podręczne z kompletem plików, wersja jednoplikowa z pliku, import starego eksportu i eksport w nowym formacie. Zero błędów konsoli.

## Faza 3: testy automatyczne

`python3 testy/run.py` uruchamia wszystko i zwraca 1 przy porażce. Testy przeglądarkowe biegną w pełnym Chromium (Playwright `channel="chromium"`) z emulacją Pixel 7 (dotyk, 412 px, Android w nagłówku przeglądarki). `testy/serwer.py` serwuje stronę pod `http://127.0.0.1:<port>/nauka/` z nagłówkami jak na Pages. Testy, które zmieniają serwowane pliki albo wyłączają sieć, dostają własną kopię strony i własny serwer. Każdy test sprawdza na końcu, że w konsoli nie było ani jednego błędu ani ostrzeżenia.

| test | co sprawdza | wynik |
|---|---|---|
| statyczne (7) | `.nojekyll`, katalog zgodny z frontmatterami, `WERSJA` zgodna ze skrótem powłoki, brak adresów sieciowych i ścieżek bezwzględnych, pola manifestu i rozmiary PNG, unikalne identyfikatory, 10 rysunków w pliku figur | przeszły |
| 01 | start bez błędów konsoli, wybór klasy, kl. 8 widzi oba tematy, pasek stanu z numerem uruchomienia i pamięcią trwałą | przeszedł |
| 02 | każde z 51 zadań sprawdzanych w obu tematach rozwiązane dobrze i źle: werdykt, konkretne wyjaśnienie (dokładnie to wyjaśnienie odpowiedzi w quizie, źle ocenione zdanie w pf, wpisana i poprawna wartość w luce, źle ułożone kroki, złe połączenie w parach), zapis, wynik „1 / 1” albo „0 / 1”. Sprawdzian 7 z 10 dobrze daje „7 / 10 pkt” i trzy omówione błędy. Fiszki „Umiem” i „Jeszcze nie” trafiają do zapisu | przeszedł |
| 03 | `0,375`, `0.375`, ` 0,3750 ` uznane; `-4`, `−4`, `2.5`, `–2.5` uznane; `4` zamiast `-4` nie; `11/12` i `11 / 12`; `mmxxvii`. Minus wpisywany z klawiatury. `inputmode`: pełna klawiatura w `k26`, `k13`, `k23`, numeryczna w `k18`, `k11` | przeszedł |
| 04 | trzy błędne i dwa dobre zadania w dwóch tematach, przeładowanie: numer uruchomienia +1, „Powtórka błędów” pokazuje dokładnie błędne zadania | przeszedł |
| 05 | jeden start online bez otwierania tematu, czekanie na service worker i komplet tematów w pamięci, potem `set_offline(True)` **i zatrzymanie serwera**, przeładowanie, kompendium i zadanie w obu tematach | przeszedł |
| 06 | postęp w figurach, przeładowanie bez sieci, na serwerze nowa `wersja` i zmieniony nagłówek działu, powrót sieci, przeładowanie: nowa treść widoczna, postęp bez zmian. Potem nowa `WERSJA` powłoki: w trakcie zadania pojawia się pasek „Jest nowa wersja, odśwież”, strona się nie przeładowuje, wybrana odpowiedź zostaje. Stuknięcie przeładowuje do nowej wersji, postęp zostaje | przeszedł |
| 07 | eksport, `localStorage.clear()`, przeładowanie, import „Zastąp”, eksport: oba pliki identyczne poza datą eksportu. Potem stary format z wersji jednoplikowej „Połącz”: fiszka `f:f02` trafia pod `f02`, nowszy wpis nie jest nadpisany starszym, licznik 50 i data 1.09.2026 przejęte | przeszedł |
| 08 | `Page.getInstallabilityErrors` zwraca pustą listę, Chrome wysyła `beforeinstallprompt`, `Page.getAppId` kończy się na `/nauka/`, manifest bez błędów, pola manifestu, ikony 200 i `image/png` | przeszedł |
| 09 | kompendium figur 5 rysunków, zadania `g03`, `g04`, `g07`, `g12`, `g15` po jednym, razem 10, każdy większy niż 100×60 px, żaden znacznik nie widnieje jako tekst | przeszedł |
| 10 | serwer bez figur w katalogu, import `mat-e8-figury.md` z pliku: komunikat, oznaczenie „z pliku”, 5 rysunków, temat zostaje po przeładowaniu w `nauka:_plik:mat-e8-figury`. To samo w wersji jednoplikowej otwartej z `file://` | przeszedł |
| 11 | temat testowy z identyfikatorami `k01` i `f01` jak w liczbach: odpowiedź w jednym nie zmienia drugiego, każdy klucz w `localStorage` pasuje do schematu | przeszedł |
| 12 | szerokość 360 px, 8 widoków i każde z 51 zadań przed sprawdzeniem i po nim: wszystkie przyciski, pola i podsumowania co najmniej 44×44 px, strona nie szersza niż 360 px | przeszedł |
| 13 | migracja `nauka:v1`: zadanie i fiszka pod nowymi kluczami, licznik 7 → 8, kopia `nauka:v1` zostaje, druga migracja nic nie nadpisuje | przeszedł |
| 14 | temat z pułapkami w SVG (`onload`, `<script>`, `javascript:`, `onclick`, `url(https://…)`, `<image>`, `<foreignObject>`, `<style>@import`, `<animate>`): nic się nie wykonuje, nic niebezpiecznego nie zostaje w DOM, bezpieczna linia zostaje, `<b>` poza rysunkiem jest tekstem z ostrzeżeniem | przeszedł |
| 15 | pierwiastek: znak i kreska zaczynają się na tej samej wysokości, bez przerwy w poziomie, znak nie krótszy od argumentu. W kompendium, w odpowiedziach quizu `g11` i w fiszkach `gf06`–`gf08` | przeszedł |
| 16 | zero ostrzeżeń parsera w obu tematach | przeszedł |
| 17 | kl. 4 widzi „Tematy wkrótce”, zmiana na kl. 8 w ustawieniach pokazuje tematy | przeszedł |
| 18 | wstecz z ćwiczeń wraca do tematu, a dalej do listy | przeszedł |

**Wynik: 25 z 25** po fazie 3. Po fazie 4 doszły trzy testy treści (`testy/test_tresc.py`: przeliczone odpowiedzi w obu tematach i proporcje rysunków), razem **28 z 28**. Czas całości około 90 sekund.

Sprawdziłem też, czy testy nie są puste, psując celowo dane. Manifest bez ikon i `start_url` przy teście 08 dał `start-url-not-valid` i `manifest-missing-suitable-icon`. Samo `set_offline(True)` (bez zatrzymywania serwera) też odcina service workera od sieci, więc test 05 na produkcji jest wiarygodny.

Test 14 złapał błąd, który wprowadziłem w fazie 1: sprawdzanie znaczników HTML zaczynało od końca pliku, więc nigdy niczego nie zgłaszało. Poprawione. Test 08 złapał błąd manifestu: `"id": "./"` jest rozwiązywane względem początku domeny, nie katalogu, więc aplikacja miałaby identyfikator `akku1906.github.io/`, wspólny z każdą przyszłą stroną z tego konta. Teraz `"id": "nauka/"`.

**Czego nie da się sprawdzić w emulacji**: czy prawdziwa klawiatura Androida przy `inputmode="text"` i `"decimal"` wygląda tak, jak zakładam (test sprawdza tylko atrybut); jak wygląda ikona na ekranie głównym i okno instalacji; czy Chrome na telefonie przyzna pamięć trwałą (w emulacji `persist()` zwraca `false`); fizyczny przycisk wstecz (emulowany przez historię przeglądarki); systemowy wybór pliku `.md` i `.json` na Androidzie; gdzie trafia pobrany plik postępu w trybie zainstalowanym; tryb samolotowy zamiast emulowanego braku sieci; tryb ciemny. To wszystko jest w instrukcji dla rodzica na końcu.

## Faza 4: audyt treści

### Parser i identyfikatory

Zero ostrzeżeń parsera w obu tematach (test 16). Identyfikatory unikalne w obrębie tematu (test statyczny i test 11).

### Przeliczenie odpowiedzi

Każdą odpowiedź liczbową z luk i quizów, każde zdanie P/F z liczbami i każdą parę z liczbami przeliczyłem niezależnie w Pythonie: `testy/test_tresc.py`. Obliczenia są tam zapisane wprost (np. `20 - F(12, 4) * 3 == 11`, `math.gcd(72, 60) == 12`, `rozwiniecie(1, 6) == '0,1(6)'`) i są częścią `testy/run.py`, więc późniejsza zmiana odpowiedzi bez zmiany obliczenia nie przejdzie. Sprawdziłem też dystraktory z wyjaśnieniami (np. w `k01`: `20 − 12 : 12 = 19`, `8 : 4 · 3 = 6`, `17 · 3 = 51`). Cechy podzielności z `k05` sprawdziłem na wszystkich liczbach od 1 do 9999, a zapisy rzymskie z `k24` przez konwersję w obie strony.

Wynik: **wszystkie odpowiedzi w obu tematach są poprawne.** Żadna liczba nie wymagała zmiany. Test na pewno nie jest pusty: podmiana `___[2700]` na `___[2800]` w `k21` daje błąd.

### Rysunki

Współrzędne SVG zmierzyłem skryptem (kąty z iloczynu skalarnego, długości w jednej skali), a potem obejrzałem zrzuty.

| zadanie | co sprawdziłem | stan zastany | co zrobiłem |
|---|---|---|---|
| `g03` | sieczna 69,8° (dane: 70°), łuk „70°” przy prostej *a* między prawą półprostą a sieczną w górę, łuk β przy *b* między lewą półprostą a sieczną w górę, więc β = 180° − 70° | zgodny | bez zmian |
| `g04` | kąty trójkąta i kąt zewnętrzny | **przeczył danym**: narysowane 51°, 48°, 81° przy opisanych 40°, 65°, 75°, kąt przy B wyglądał na mniejszy od kąta 40°, a kąt zewnętrzny na 132° zamiast 115° | wierzchołek przeniesiony do (152,2; 37,5): kąty 40,0°, 65,0°, 75,0°, łuk kąta zewnętrznego 115°, napisy przy swoich wierzchołkach. Zdanie „Rysunek jest poglądowy” usunięte, bo rysunek jest teraz w skali |
| `g07` | podstawa 10, wysokość 6, bok 8 | zgodny co do 0,1% (bok 8,006) | bez zmian |
| `g12` | kąt 29,9° naprzeciw *x*, przeciwprostokątna 2,006 raza dłuższa od *x*, kąt prosty w dobrym wierzchołku | zgodny, ale „30°” nachodził znakiem stopnia na przeciwprostokątną | napis przesunięty, test mierzy odstęp |
| `g15` | podstawy 10 i 6, wysokość 4 | trzy różne skale (26, 20 i 22,5 px na jednostkę) | trapez narysowany w jednej skali 26 px. „Rysunek jest poglądowy” usunięte |

Te pomiary też są w `testy/test_tresc.py`. Na starej wersji pliku test pada na `g04`.

Rysunki w kompendium (kąty, pole trójkąta, Pitagoras, trapez, koło) mają oznaczenia ogólne (α, β, a, b, h, r) i sprawdziłem je wzrokowo: α stoją w kątach ostrych, β w rozwartych, kąt prosty jest tam, gdzie ma być.

### Zgodność z podstawą programową

Źródło: tekst rozporządzenia MEN z 28 czerwca 2024 r. (Dz.U. 2024 poz. 996), część „Matematyka”, pobrany z dziennikustaw.gov.pl, oraz informator CKE „o egzaminie ósmoklasisty z matematyki od roku szkolnego 2024/2025”, który mówi, że egzamin sprawdza wymagania tej podstawy. Nowa podstawa od 1 września 2026 r. obejmuje na razie klasę 4, więc kl. 8 w roku 2026/2027 uczy się według podstawy z 2024 r. (to wiem z jednego źródła wtórnego, IBE, i nie sprawdziłem w rozporządzeniu).

Błędy merytoryczne względem podstawy, poprawione:

1. **Twierdzenie odwrotne do twierdzenia Pitagorasa.** Podstawa, kl. VII–VIII, VIII.7: „zna i stosuje w sytuacjach praktycznych twierdzenie Pitagorasa (bez twierdzenia odwrotnego)”. Kompendium figur miało zdanie „Działa też w drugą stronę…”, a zadanie `g10` („Czy trójkąt jest prostokątny?”) w całości opierało się na twierdzeniu odwrotnym. Zdanie usunąłem, `g10` zastąpiłem zadaniem `g26` „Pitagoras: prawda czy fałsz” (przeciwprostokątna najdłuższa; 5 i 12 dają 13, nie 17; 9 i 12 dają 15; przy 10 i 6 druga przyprostokątna to 8, nie 4). Nowy identyfikator, bo to inne zadanie i stary postęp by do niego nie pasował.
2. **Wycinek koła.** Dział XIV „Długość okręgu i pole koła” obejmuje tylko długość okręgu, pole koła i odwrotne zadania (promień z długości lub pola). Ogólny wzór „wycinek o kącie α to α/360 koła” to materiał liceum. Kompendium mówi teraz o półkolu i ćwierci koła, a `g23` pyta o pole jednej z czterech części koła podzielonego dwiema prostopadłymi średnicami. Odpowiedź (9π) i identyfikator zostały.

Na granicy, zostawione (decyzja 24):

- `g17` i tabela jednostek pola: podstawa IV–VI, XI.4 „stosuje jednostki pola: mm², cm², dm², m², km², ar, hektar (bez zamiany jednostek w trakcie obliczeń)”. Zostawiłem, bo XI.3 każe liczyć pola „dla danych wymagających zamiany jednostek”, a 1 m² = 10 000 cm² to dokładnie ta pułapka.
- `g19`, `g20` i kompendium „Wielokąty”: podstawa VII–VIII IX.1 mówi tylko „zna pojęcie wielokąta foremnego”, ale IV–VI XI.1 każe obliczać miary kątów z własności wielokątów, a szkolne wymagania dla kl. 8 (podręcznikowe, nie podstawa) zawierają kąty wielokątów foremnych.
- `g04` kąt zewnętrzny i `g12` trójkąt 30°, 60°, 90°: nie ma ich wprost w podstawie, ale wynikają z sumy kątów, kątów przyległych i twierdzenia Pitagorasa, a przykład z podstawy (XI.2) sam używa trójkąta o kątach 45°, 45°, 90°.
- Środek symetrii (kompendium, `g24`): dział XV „Symetrie” podstawa pozwala zrealizować po egzaminie. Osie symetrii są też w IV–VI (IX.5), więc `g24` zostaje.

Potwierdzone w podstawie bez zastrzeżeń: system rzymski do 3000 (IV–VI I.5), cechy podzielności przez 2, 3, 4, 5, 9, 10, 100 (II.6), NWD i NWW metodą rozkładu (II.11), dzielenie z resztą w postaci a = b · q + r (II.15), wartość bezwzględna (III.3), rozwinięcia dziesiętne nieskończone (IV.10), całość z części (IV.13), kąty wierzchołkowe i przyległe (VIII.6 oraz VII–VIII VIII.1), kąty odpowiadające i naprzemianległe (VII–VIII VIII.3), cechy przystawania (VIII.4), nierówność trójkąta (VIII.5), wzory na pola (IX.2), środek odcinka (X.4), długość okręgu i pole koła (XIV.1, XIV.3). Przykład „23 + 49 + 77” z kompendium liczb pochodzi wprost z warunków realizacji podstawy.

Temat figur ma wersję 2026-11-03, temat liczb też (zadanie `k26` z fazy 1).

## Faza 5: wdrożenie i sprawdzenie na żywo

Push na `main` był możliwy (`63e5371..8d7fb81`), więc nie było przystanku na merge. GitHub Pages zbudował stronę w około 30 sekund.

`curl -I` na produkcji:

| adres | kod | typ |
|---|---|---|
| `/nauka/` | 200 | `text/html; charset=utf-8` |
| `/nauka` | 301 na `/nauka/` | |
| `/nauka/index.html` | 200 | `text/html; charset=utf-8` |
| `/nauka/manifest.webmanifest` | 200 | `application/manifest+json; charset=utf-8` |
| `/nauka/sw.js` | 200 | `application/javascript; charset=utf-8` |
| `/nauka/tematy/index.json` | 200 | `application/json; charset=utf-8` |
| `/nauka/tematy/mat-e8-liczby.md` | 200 | `text/markdown; charset=utf-8` |
| `/nauka/tematy/mat-e8-figury.md` | 200 | `text/markdown; charset=utf-8` |
| `/nauka/ikony/*.png` (4 pliki) | 200 | `image/png` |
| `/nauka/.nojekyll` | 200 | |

Wszystkie z `Cache-Control: max-age=600`. Skróty MD5 plików `index.html`, `sw.js`, manifestu, katalogu, obu tematów i ikony 512 są identyczne z repozytorium, więc Jekyll niczego nie przerobił.

Testy na produkcji (`python3 testy/run.py --url https://akku1906.github.io/nauka/`): **4 z 4**.

| test | wynik |
|---|---|
| 01 start bez błędów, wybór klasy, oba tematy | przeszedł |
| 05 offline po jednym starcie bez otwierania tematu (`set_offline`, które, jak sprawdziłem w fazie 3, odcina też service workera) | przeszedł |
| 08 instalowalność: pusta lista błędów, `beforeinstallprompt`, identyfikator aplikacji `/nauka/` | przeszedł |
| 09 dziesięć rysunków w temacie figur, żaden znacznik jako tekst | przeszedł |

## Instrukcja dla rodzica: prawdziwy telefon z Androidem

Potrzebne: telefon z Chrome, internet na czas instalacji, stara wersja aplikacji otwierana z pliku (ta, na której jest dotychczasowy postęp).

**1. Zapisz postęp ze starej wersji.**
Otwórz starą aplikację z pliku, tak jak dotąd. Przewiń ekran na sam dół i stuknij „Zapisz postęp do pliku”. Plik `postep-RRRR-MM-DD.json` trafi do folderu Pobrane. Jeśli zamiast pobierania pojawi się tekst, zaznacz go w całości, skopiuj i wklej do notatki albo wyślij sobie wiadomością.

**2. Otwórz aplikację z internetu.**
W Chrome wpisz adres `https://akku1906.github.io/nauka/`. Wybierz „Klasa 8”. Na liście powinny być „Liczby i działania” i „Figury płaskie”. Odczekaj kilka sekund na liście, żeby aplikacja pobrała tematy do pamięci.

**3. Zainstaluj.**
Menu Chrome (trzy kropki w prawym górnym rogu), potem „Zainstaluj aplikację” (w części telefonów: „Dodaj do ekranu głównego”, a potem „Zainstaluj”). Na ekranie głównym pojawi się ikona „Nauka”: zielony ptaszek na kartce w kratkę. Od teraz otwieraj aplikację tą ikoną. Otwiera się bez paska adresu.

**4. Wczytaj postęp.**
W zainstalowanej aplikacji przewiń na dół i stuknij „Wczytaj postęp z pliku”. Wybierz plik z kroku 1 z folderu Pobrane. Aplikacja pokaże, ile wpisów jest w pliku. Stuknij „Zastąp” (w świeżej instalacji nie ma czego łączyć). Sprawdź pasek stanu na dole: numer uruchomienia powinien kontynuować liczenie ze starej wersji, a w temacie „Powtórka błędów” powinny być dawne błędy.
Jeśli telefon nie pozwala wybrać pliku `.json` (jest wyszarzony): „Ustawienia”, „Wklej postęp jako tekst”, wklej tekst z kroku 1, „Wczytaj tekst”.

**5. Sprawdź pasek stanu.**
Na dole listy tematów: „Zapis postępu działa. To uruchomienie nr …, pierwsze …. Pamięć trwała: tak/nie. Wersja ….” Po instalacji Chrome zwykle przyznaje pamięć trwałą („tak”). Przy „nie” postęp i tak się zapisuje, ale przeglądarka mogłaby go usunąć, gdy w telefonie skończy się miejsce. Wtedy warto co jakiś czas robić „Zapisz postęp do pliku”.

**6. Test bez internetu.**
Otwórz aplikację raz z internetem i zamknij ją. Włącz tryb samolotowy. Otwórz aplikację ikoną. Lista ma pokazać oba tematy. Otwórz „Figury płaskie”, potem „Kompendium”: rysunki mają być widoczne. Zrób po jednym zadaniu w każdym temacie. Wyłącz tryb samolotowy.

**7. Test przycisku wstecz.**
W zadaniu stuknij systemowe „wstecz”: aplikacja ma wrócić do ekranu tematu, a nie się zamknąć.

**8. Test aktualizacji.**
Aktualizacja tematu: gdy w repozytorium zmieni się plik tematu (np. w nowej sesji poproszę o drobną poprawkę), otwórz aplikację z internetem. Nowa treść pojawi się od razu albo, przy słabym zasięgu, przy następnym otwarciu. Postęp zostaje.
Aktualizacja aplikacji: gdy zmieni się sama aplikacja, na dole ekranu pojawi się pasek „Jest nowa wersja, odśwież.” z przyciskiem „Odśwież”. Aplikacja nie przeładuje się sama w trakcie zadania. Po stuknięciu „Odśwież” numer wersji w pasku stanu się zmieni, a postęp zostanie. Zamknięcie i ponowne otwarcie aplikacji też wczytuje nową wersję.

Stara wersja z pliku dalej działa, ale ma swój osobny postęp. Po przeniesieniu najlepiej z niej nie korzystać, żeby postęp się nie rozjechał.

## Decyzje

1. **Źródło prawdy dla silnika: `silnik.html`.** Dlaczego: jest identyczny z `aplikacja.html` po zbudowaniu, więc wybór nie ma skutków. Alternatywa: wyodrębnienie z `aplikacja.html`, która dałaby ten sam wynik.
2. **Osobny klucz `localStorage` na każdy element postępu**, zamiast jednego obiektu z kluczami `temat:id` w środku. Dlaczego: tak brzmi kontrakt w `CLAUDE.md`, zapis jednej odpowiedzi nie przepisuje całego stanu, a uszkodzony wpis psuje tylko jeden element. Alternatywa: jeden klucz `nauka:v2` z mapą, prostszy w eksporcie, ale z tymi samymi wadami co `nauka:v1`.
3. **Dane aplikacji pod `nauka:_…`**, a identyfikator tematu nie może zaczynać się od podkreślnika ani mieć dwukropka. Dlaczego: inaczej `nauka:_plik:x` dałoby się pomylić z postępem tematu `_plik`. Alternatywa: osobny prefiks, np. `nauka-app:`, ale wtedy nie wszystko byłoby pod `nauka:`.
4. **Stary klucz `nauka:v1` zostaje po migracji.** Dlaczego: to kopia na wypadek błędu migracji, a waży kilka kilobajtów. Migracja biegnie raz, pilnuje jej `nauka:_migracja`, i nie nadpisuje wpisów, które już są w nowym formacie. Alternatywa: usunięcie, które zwolniłoby miejsce, ale odebrało drogę odwrotu.
5. **Fiszki bez przedrostka `f:` w kluczu.** Dlaczego: przykład z `CLAUDE.md` (`nauka:mat-e8-figury:g07`) ma gołe identyfikatory, a unikalność w obrębie tematu jest pilnowana przez parser. Alternatywa: `nauka:temat:f:f01`, zgodne ze starym silnikiem, ale z dodatkowym dwukropkiem.
6. **Klawiatura per zadanie, nie per luka.** Pełna klawiatura dla całego zadania, jeśli choć jedna odpowiedź ma minus, ułamek albo litery. Dlaczego: klawiatura per luka zdradzałaby, która odpowiedź jest ujemna, a tylko pełna klawiatura na pewno ma minus i `/` na każdym Androidzie. Alternatywa: `type="number"` (ma minus, ale gubi przecinek w części lokalizacji i nie przyjmie `11/12`) albo własny przycisk ±, który zaśmieca zdanie z luką. Koszt: klawiatura numeryczna nadal zdradza, że odpowiedź jest nieujemna.
7. **Liczby w lukach porównywane jako liczby**, ułamki zwykłe dosłownie. `0,50` = `0,5`, ale `22/24` ≠ `11/12`. Dlaczego: zero na końcu ułamka dziesiętnego nie zmienia odpowiedzi, a przy ułamkach zwykłych skracanie bywa częścią zadania. Alternatywa: porównanie wartości ułamków, które przyjęłoby też nieskrócone wyniki.
8. **Nowe zadanie `k26` „Liczby ujemne”** w temacie liczb (wersja tematu 2026-11-03). Dlaczego: kompendium uczy znaków, a żadne zadanie nie wymagało wpisania liczby ujemnej, więc ani uczennica tego nie ćwiczyła, ani test nie mógł sprawdzić minusa. Alternatywa: osobny temat testowy tylko w `testy/`, który sprawdziłby mechanizm, ale nie prawdziwą treść.
9. **Znak pierwiastka jako maska CSS**, a nie element `<svg>`. Dlaczego: rysunek rozciąga się do wysokości argumentu niezależnie od fontu, a liczba elementów `<svg>` na stronie nadal odpowiada liczbie rysunków z tematu (test 9). Alternatywa: inline SVG w każdym pierwiastku albo sam glif √ z ręcznie dobranym przesunięciem, zależnym od fontu.

10. **Tematy z katalogu wczytywane wszystkie przy starcie**, a nie dopiero przy otwarciu. Dlaczego: lista pokazuje postęp „opanowane X z Y”, do którego trzeba sparsować temat, a pliki mają po kilkanaście kilobajtów. Alternatywa: postęp liczony z samego katalogu, co wymagałoby dopisywania liczby zadań do `index.json`.
11. **Nawigacja tematów z pamięci po 4 sekundach bez odpowiedzi sieci.** Dlaczego: „najpierw sieć” na słabym zasięgu oznacza czekanie na limit czasu przeglądarki, nawet minutę. Po 4 s uczennica dostaje temat z pamięci, a nowa wersja wchodzi przy następnym starcie. Alternatywa: czysta „najpierw sieć”, zgodna z literą zadania, ale z długim startem w autobusie.
12. **Powłoka „najpierw pamięć”, nowa wersja tylko przez nowy `sw.js`.** Dlaczego: start bez sieci jest natychmiastowy, a aktualizacja nie przerywa zadania. Alternatywa: `index.html` „najpierw sieć”, która dawałaby nowy silnik od razu, ale mogła go podmienić w połowie pracy i spowalniała start.
13. **Wersja powłoki jako skrót plików**, ustawiany skryptem i pilnowany testem. Dlaczego: zapomniana zmiana wersji to najczęstszy błąd PWA, po którym nikt nie dostaje poprawki. Alternatywa: ręczny numer wersji.
14. **Temat z pliku widoczny w każdej klasie i wygrywa tylko nowszą wersją.** Dlaczego: skoro ktoś go świadomie wgrał, nie powinien zniknąć przez filtr klasy. Przy tej samej wersji co w katalogu zostaje wersja z katalogu, bo ta jest aktualizowana. Aplikacja mówi to wprost po wgraniu pliku. Alternatywa: plik zawsze wygrywa, ale wtedy stary plik blokowałby poprawki z sieci.
15. **Import: „Połącz” bierze nowszy wpis** (po czasie ostatniej odpowiedzi), licznik uruchomień jako większy z dwóch, datę pierwszego jako wcześniejszą. **„Zastąp”** przyjmuje stan z pliku w całości, z licznikiem i ustawieniami. Bez dodatkowego `confirm`, bo wybór jest już na osobnym ekranie z opisem skutków. Alternatywa: sumowanie liczników podejść, które dublowałoby wpisy przy dwukrotnym imporcie tego samego pliku.
16. **Usunięcie `aplikacja.html` z repozytorium.** Dlaczego: to wynik budowania, identyczny ze źródłem, i leżałby pod adresem Pages jako druga, nieaktualna aplikacja. Alternatywa: zostawić jako archiwum, ale historia gita już nim jest.

17. **`"id": "nauka/"` w manifeście.** Dlaczego: `id` rozwiązuje się względem początku domeny, więc `./` dawało `akku1906.github.io/`, wspólne dla wszystkich przyszłych stron z konta, a Chrome uznaje aplikacje o tym samym `id` za jedną. `nauka/` daje `/nauka/`, czyli to, co Chrome sam podpowiada. Zapis jest względny. Alternatywa: brak `id` (wtedy identyfikatorem jest `start_url`, też `/nauka/`), ale każda późniejsza zmiana `start_url` tworzyłaby drugą aplikację.
18. **Testy w pełnym Chromium (`channel="chromium"`)**, a nie w domyślnym „headless shell”. Dlaczego: tylko pełne Chromium ocenia instalowalność, a przy okazji jest bliżej Chrome z telefonu. `run.py` wraca do domyślnej przeglądarki, gdyby pełnej nie było.
19. **Własny prosty program uruchamiający testy** zamiast pytest. Dlaczego: na komputerze rodzica wystarczy Python i Playwright. Alternatywa: pytest, wygodniejszy w raportach, ale jako dodatkowa zależność.
20. **Testy znajdują elementy po atrybutach `data-*`** (`data-k`, `data-temat`, `data-w`, `data-akcja`) i biorą poprawne odpowiedzi z tematu sparsowanego przez samą aplikację (`window.nauka`). Dlaczego: odpowiedzi są tasowane, a testy nie mogą zależeć od kolejności ani od kopii parsera w Pythonie. Alternatywa: osobny parser w Pythonie, który mógłby rozjechać się z silnikiem.

21. **`g10` usunięte, nowe `g26`.** Dlaczego: zadanie uczyło treści wyłączonej z podstawy, a wymiana treści pod tym samym identyfikatorem zostawiłaby uczennicy postęp za inne zadanie. Alternatywa: zostawić z dopiskiem „poza egzaminem”, ale to szum w krótkim temacie powtórkowym.
22. **`g23` ten sam identyfikator mimo nowego brzmienia.** Dlaczego: liczy dokładnie to samo (ćwierć koła o promieniu 6, 9π), zmienił się tylko opis, więc postęp nadal ma sens.
23. **Rysunki `g04` i `g15` przerysowane w skali, bez dopisku „Rysunek jest poglądowy”.** Dlaczego: dopisek nie usprawiedliwia rysunku, na którym kąt 65° wygląda na mniejszy niż kąt 40°, a dla ósmoklasistki rysunek w skali jest dodatkową kontrolą wyniku. Alternatywa: zostawić rysunek i dopisek, jak w części arkuszy CKE.
24. **Treści na granicy podstawy zostawione** (jednostki pola, kąty wielokątów foremnych, kąt zewnętrzny, trójkąt 30°, 60°, 90°, środek symetrii). Dlaczego: każda wynika z wymagań podstawy albo jest w szkolnych wymaganiach dla kl. 8, a usunięcie zubożyłoby powtórkę. Usuwałem tylko to, co podstawa wyłącza wprost albo czego nie ma w odpowiednim dziale.
25. **Audyt treści jako stały test** (`testy/test_tresc.py`), a nie jednorazowy rachunek w raporcie. Dlaczego: treść będzie się zmieniać, a test pilnuje odpowiedzi i proporcji rysunków przy każdej zmianie. Koszt: przy zmianie zadania trzeba poprawić też oczekiwany wynik w teście.
26. **Wiersz Prawda/Fałsz może zawinąć przyciski pod zdanie.** Dlaczego: przy 360 px długie słowo („przeciwprostokątna”) i dwa przyciski 64 px nie mieszczą się w jednej linii, a strona robiła się szersza od ekranu (wykrył to test 12 na nowym `g26`).

## Ściany

1. **`Page.getInstallabilityErrors` w domyślnym trybie headless Playwrighta zwraca pustą listę zawsze**, także dla strony bez manifestu (sprawdzone na trzech zepsutych wariantach). Test oparty na nim nic by nie sprawdzał. Obejście: test 08 uruchamia pełne Chromium w nowym trybie headless z flagą `--bypass-app-banner-engagement-checks`. Tam lista działa (każda mutacja daje konkretny błąd) i dodatkowo przychodzi `beforeinstallprompt`.
