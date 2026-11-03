# Zadanie dla sesji w chmurze: audyt, PWA, wdrożenie

Pracujesz sam, bez zadawania pytań. Każdą decyzję podejmij sam i zapisz w `docs/RAPORT.md` w sekcji „Decyzje” (co, dlaczego, jaka alternatywa). Po każdej fazie commituj i pushuj, bo maszyna wirtualna może zostać zwolniona w trakcie. Jeśli coś się nie da zrobić, zapisz to jako „Ściana” w raporcie, obejdź i idź dalej.

## Stan wejściowy

W katalogu głównym repo leżą pliki wgrane ręcznie:

- `silnik.html`: szablon silnika aplikacji (HTML, CSS i JS w jednym pliku).
- `zbuduj.py`: skrypt, który wstawia plik tematu do silnika i robi z tego jeden plik HTML.
- `aplikacja.html`: zbudowana wersja testowa, ta, którą sprawdzano na Androidzie.
- `mat-e8-liczby.md`: temat „Liczby i działania” (kl. 8), w rozszerzonej składni generatora.
- `mat-e8-figury.md`: temat „Figury płaskie” (kl. 8), ma surowe znaczniki `<svg>` w Markdown i `\sqrt{}`.

Co wiadomo z testów na Androidzie: aplikacja otwarta z pliku działa, zapis postępu działa, numer uruchomienia rośnie, a import tematu z pliku działa. Nie działa skrót na ekranie głównym, bo Chrome dostaje tymczasowy adres `content://`. Dlatego aplikacja ma zamieszkać na GitHub Pages: `https://akku1906.github.io/nauka/`. Pages jest włączone z gałęzi `main`, katalog `/` (root).

## Faza 0: inwentaryzacja (bez zmian w kodzie)

1. Ustal, która wersja silnika jest najnowsza. `aplikacja.html` mogła dostać poprawki (np. przycisk „Dodaj temat z pliku”), których nie ma w `silnik.html`. Zbuduj `zbuduj.py silnik.html + mat-e8-liczby.md` i porównaj logikę JS z `aplikacja.html`. Źródłem prawdy jest nowsza wersja. Jeśli to `aplikacja.html`, wyodrębnij z niej silnik.
2. Opisz w raporcie, co robi silnik: parser Markdown i formuł, typy zadań, ocenianie, model zapisu (klucze, struktura), eksport, import tematu z pliku.

## Faza 1: audyt kodu

Najpierw spisz znaleziska w raporcie z oceną wagi (krytyczne, ważne, kosmetyczne), potem napraw krytyczne i ważne. Sprawdź co najmniej:

- **Klucze zapisu.** Czy postęp jest kluczowany parą temat i identyfikator, czy samym identyfikatorem? Samo `f01` w dwóch tematach oznacza kolizję. Przejdź na `nauka:<temat>:<id>` z migracją starego zapisu.
- **Surowy HTML w Markdown.** Czy parser przepuszcza `<svg>` z pliku figur jako element, czy jako tekst? Dopuść `<svg>` i jego dzieci, a usuwaj `<script>`, atrybuty `on*` i `javascript:`.
- **Pierwiastek.** Czy `\sqrt{...}` renderuje się z kreską nad całym wyrażeniem, także w odpowiedziach quizu i fiszkach?
- **Pola do wpisywania.** Przecinek i kropka dziesiętna mają działać (już działają, nie zepsuj tego). Sprawdź minus i ułamki. Uwaga na `inputmode="decimal"`: na części klawiatur Androida nie ma minusa. Jeśli zadanie może mieć ujemny wynik, użyj klawiatury, która go ma.
- **Zależności zewnętrzne.** Żadnych odwołań do sieci (fonty, CDN). Fonty z fallbackiem do systemowego szeryfowego Androida.
- **Błędy w konsoli** przy każdym widoku i typie zadania.
- **Dostępność dotyku.** Cele dotyku co najmniej 44 px, brak poziomego przewijania strony na szerokości 360 px.

## Faza 2: struktura repo i PWA

Docelowy układ:

```
index.html              silnik (dawny silnik.html), ładuje tematy w czasie działania
manifest.webmanifest    name „Nauka”, start_url "./", scope "./", display standalone, ikony 192, 512 i maskable
sw.js                   service worker
ikony/                  ikony PNG (wygeneruj prostą, czytelną ikonę bez tekstu osobowego)
tematy/index.json       katalog: id, tytuł, przedmiot, klasa, wersja, plik
tematy/*.md             pliki tematów
narzedzia/zbuduj.py     zostaje: buduje wersję jednoplikową do pracy bez hostingu
testy/                  testy Playwright i skrypt run.py
docs/FORMAT.md          opis składni tematów (kontrakt z generatorem PDF)
docs/RAPORT.md          raport z sesji
.nojekyll               obowiązkowo
```

Wymagania:

1. **Wybór klasy przy pierwszym uruchomieniu** (8 albo 4), z możliwością zmiany w ustawieniach. Kl. 4 na razie widzi komunikat „Tematy wkrótce”.
2. **Tematy** pochodzą z `tematy/index.json`. Przycisk „Dodaj temat z pliku” zostaje, a temat z pliku jest oznaczony jako „z pliku” i zapisany lokalnie.
3. **Service worker.** Powłoka aplikacji (index, manifest, ikony) jest zapisywana z góry. Dla `tematy/index.json` i `tematy/*.md` stosuj „najpierw sieć, potem pamięć podręczna”, żeby nowe tematy dochodziły same, a bez internetu działało wszystko, co już było pobrane. Przy każdym starcie z dostępem do sieci service worker pobiera do pamięci wszystkie tematy wymienione w `tematy/index.json`, nie tylko te już otwarte, żeby offline działał też temat, którego uczennica jeszcze nie otwierała. Pamięć podręczna ma wersję. Gdy pojawi się nowa wersja aplikacji, pokaż pasek „Jest nowa wersja, odśwież” zamiast przeładowywać w trakcie zadania.
4. **Trwałość.** Wywołaj `navigator.storage.persist()` i pokaż wynik w pasku stanu obok numeru uruchomienia.
5. **Eksport i import postępu.** Eksport zapisuje plik JSON z wersją formatu. Import pyta „zastąpić czy połączyć” i przyjmuje też stary format z wersji jednoplikowej. To jedyna droga przeniesienia postępu z wersji otwieranej z pliku do wersji z sieci, bo zapis przeglądarki jest przypisany do adresu.
6. Wszystkie ścieżki względne.
7. `docs/FORMAT.md` opisuje pełną składnię: frontmatter, typy zadań `{quiz}`, `{pf}`, `{luka}`, `{kolejnosc}`, `{pary}`, zadania otwarte `[odp: n]`, sekcje `### Rozwiązanie`, fiszki `{#id} pytanie :: odpowiedź`, formuły `$...$` i `$$...$$`, `\sqrt{}`, `\frac{}{}`, surowe `<svg>`, konwencję prefiksów identyfikatorów.

## Faza 3: testy automatyczne

Python i Playwright, Chromium z emulacją telefonu Pixel 7 (dotyk, 412 px). Serwuj repo lokalnie pod ścieżką `/nauka/`, żeby odtworzyć podkatalog z Pages. Testy zapisz w `testy/`, a `testy/run.py` ma je wszystkie uruchamiać i zwracać kod błędu przy porażce.

1. Start bez błędów w konsoli. Wybór klasy 8, lista pokazuje oba tematy.
2. Każdy typ zadania w obu tematach: odpowiedź poprawna i błędna, punktacja, wyjaśnienie konkretnego błędu.
3. Liczby: `2,5` i `2.5` są uznawane. Wynik ujemny da się wpisać.
4. Trwałość: po zrobieniu zadań i przeładowaniu numer uruchomienia rośnie, a błędne zadania są w powtórce błędów.
5. Offline: po rejestracji service workera i jednym starcie online, bez otwierania żadnego tematu, `context.set_offline(True)`, przeładowanie i praca z oboma tematami.
6. Aktualizacja: zmień `wersja` tematu w serwowanej kopii, wróć online, przeładuj. Nowa treść ma się pojawić, a postęp zostać.
7. Eksport, wyczyszczenie pamięci, import: stan po imporcie ma być identyczny (porównanie JSON).
8. Instalowalność: przez CDP wywołaj `Page.getInstallabilityErrors`. Lista ma być pusta. Sprawdź też pola manifestu.
9. Rysunki: temat figur renderuje 10 elementów `<svg>` i żaden znacznik nie wyświetla się jako tekst.
10. Import tematu z pliku działa na `mat-e8-figury.md`.
11. Brak kolizji identyfikatorów między tematami.

## Faza 4: audyt treści

1. Parser nie zgłasza ostrzeżeń dla żadnego tematu, a identyfikatory są unikalne w obrębie tematu.
2. Każdą odpowiedź liczbową z luk i quizów przelicz niezależnie (skryptem albo ręcznie z zapisem obliczeń w raporcie).
3. Dla zadań z rysunkiem (`g03`, `g04`, `g07`, `g12`, `g15`) sprawdź, że rysunek zgadza się z treścią i odpowiedzią: oznaczenia stoją przy właściwych kątach i bokach, proporcje nie przeczą danym.
4. Treść nie wychodzi poza podstawę programową kl. 8. Zgłoś błędy merytoryczne w raporcie i popraw je w pliku tematu.

## Faza 5: wdrożenie i sprawdzenie na żywo

1. Jeśli możesz pushować na `main`, zrób to. Jeśli środowisko narzuca własną gałąź, otwórz PR do `main` i napisz mi jednym zdaniem, że czeka na merge. To jedyny dozwolony przystanek w całej sesji. Po moim „zmergowane” kontynuuj.
2. Gdy strona jest na `main`, poczekaj na zbudowanie Pages. Sprawdź `curl -I` dla `https://akku1906.github.io/nauka/`, manifestu, `sw.js`, `tematy/index.json` i każdego pliku tematu. Wszystkie mają zwracać 200.
3. Uruchom testy 1, 5, 8 i 9 na adresie produkcyjnym.

## Faza 6: raport

`docs/RAPORT.md` po polsku zawiera:

- co zrobiono, w jakiej kolejności, z linkami do commitów,
- znaleziska z audytu i co z nimi zrobiono,
- wyniki testów (co przeszło, czego nie dało się sprawdzić w emulacji),
- decyzje i ściany,
- instrukcję dla rodzica na prawdziwy telefon z Androidem, krok po kroku: eksport postępu ze starej wersji z pliku, otwarcie adresu w Chrome, „Zainstaluj aplikację”, import postępu, test bez internetu (tryb samolotowy), test aktualizacji.

Na koniec napisz mi w czacie krótkie podsumowanie: adres aplikacji, wynik testów, co zostało do sprawdzenia na telefonie.

## Poza zakresem

Tryb kl. 4 z punktami i gwiazdkami, tutor AI, zmiany w generatorze PDF (repo `generator`, osobna sesja), nowe tematy.
