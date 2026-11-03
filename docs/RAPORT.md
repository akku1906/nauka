# Raport z sesji: audyt, PWA, wdrożenie

Sesja w chmurze, 3 listopada 2026. Pracowałem sam, według `ZADANIE.md`, faza po fazie. Każda decyzja jest w sekcji „Decyzje”, a każda przeszkoda w sekcji „Ściany”.

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

**Manifest**: `name` i `short_name` „Nauka”, `id`, `start_url` i `scope` równe `./`, `display: standalone`, `lang: pl`, ikony 192 i 512 (`any`) oraz 192 i 512 (`maskable`). Ikony rysuje `narzedzia/ikony.py`: kartka w kratkę z marginesem, żółtym zakreśleniem i zielonym ptaszkiem na granatowym tle, bez tekstu. W wersji maskable kartka mieści się w bezpiecznym kole.

**Narzędzia**: `narzedzia/katalog.py` (katalog z frontmatterów), `narzedzia/wersja.py` (wersja powłoki), `narzedzia/ikony.py`, `narzedzia/zbuduj.py`, `testy/serwer.py` (serwer jak Pages pod `/nauka/`, z `Cache-Control: max-age=600`).

Sprawdzone w tej fazie próbą dymną (pełne testy w fazie 3): wybór klasy, lista z oboma tematami, przejście wstecz o ekran, aktywny service worker i obie pamięci podręczne z kompletem plików, wersja jednoplikowa z pliku, import starego eksportu i eksport w nowym formacie. Zero błędów konsoli.

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

## Ściany

Na razie brak.
