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

## Decyzje

1. **Źródło prawdy dla silnika: `silnik.html`.** Dlaczego: jest identyczny z `aplikacja.html` po zbudowaniu, więc wybór nie ma skutków. Alternatywa: wyodrębnienie z `aplikacja.html`, która dałaby ten sam wynik.

## Ściany

Na razie brak.
