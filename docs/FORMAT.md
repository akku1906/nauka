# Format pliku tematu

Ten dokument jest kontraktem między aplikacją a osobnym generatorem PDF. Oba czytają te same pliki `tematy/*.md`. Zmiany formatu muszą być wstecznie zgodne: stary plik ma działać w nowej aplikacji bez zmian.

Plik jest w UTF-8. Znak BOM i końce linii `\r\n` są dopuszczalne.

## Układ pliku

```
---
id: mat-e8-figury
tytul: Figury płaskie
...
---

# Kompendium
...
# Zadania
...
# Fiszki
...
```

Najpierw frontmatter, potem trzy sekcje pierwszego poziomu. Nagłówki sekcji porównywane są bez względu na wielkość liter. Każda sekcja może być pusta albo jej może nie być. Tekst przed pierwszą sekcją jest pomijany.

## Frontmatter

Linia `---`, pary `klucz: wartość` po jednej w linii, linia `---`. Wartości są dosłowne: bez cudzysłowów, list i wielu linii. Klucze to litery łacińskie, cyfry i `_`.

| klucz | wymagany | znaczenie |
|---|---|---|
| `id` | tak | identyfikator tematu, stały na zawsze, bo pod nim leży postęp. Litery łacińskie, cyfry, `.`, `-`, `_`; bez dwukropka; nie zaczyna się od `_`. Konwencja: `<przedmiot>-<etap><klasa>-<nazwa>`, np. `mat-e8-liczby` (matematyka, egzamin ósmoklasisty) |
| `tytul` | tak | tytuł tematu na liście |
| `przedmiot` | tak | np. `Matematyka` |
| `klasa` | tak | `8` albo `4`. Aplikacja pokazuje temat tylko uczennicy wybranej klasy |
| `wersja` | tak | data `RRRR-MM-DD`. Porównywana tekstowo, więc zawsze z zerami (`2026-11-03`, nie `2026-11-3`). Podnoś przy każdej zmianie treści |
| `tematyka` | nie | podtytuł na ekranie tematu |
| `czas` | nie | czas pracy, np. `30 min` (używa generator PDF) |

Inne klucze są dozwolone i pomijane przez aplikację.

Gdy brakuje `id`, aplikacja nada identyfikator zastępczy ze skrótu tytułu i pokaże ostrzeżenie. Gdy brakuje `tytul`, też ostrzeże.

## Kompendium

`# Kompendium`, potem działy `## Tytuł działu`. Treść działu to bloki opisane niżej w „Treść: bloki i wzory”.

## Zadania

`# Zadania`, potem zadania. Każde zaczyna się nagłówkiem:

```
## Tytuł zadania [1 pkt] {typ #id}
```

- `[n pkt]` jest opcjonalne, domyślnie 1 punkt. Liczy się w sprawdzianie.
- `{typ #id}`: typ i identyfikator, w dowolnej kolejności, rozdzielone spacją. Identyfikator jest obowiązkowy dla wszystkich typów sprawdzanych automatycznie.
- Treść zadania to linie aż do `### Rozwiązanie`.
- `### Rozwiązanie` (dalszy tekst w tej linii jest pomijany) rozpoczyna rozwiązanie, które trwa do następnego `## `. Brak rozwiązania daje ostrzeżenie.

Bez `{typ}` typ jest zgadywany: `[odp:` daje zadanie otwarte, `- [x]` albo `- [ ]` quiz, `___[` lukę, a wszystko inne zadanie otwarte.

### `{quiz}`: jedna dobra odpowiedź

```
## Kolejność działań [1 pkt] {quiz #k01}
Ile wynosi $20 - 12 : 4 * 3$?
- [x] $11$
- [ ] $19$
  > Tu najpierw policzono $4 * 3$. Mnożenie i dzielenie są równorzędne.
- [ ] $6$
```

- Linie przed pierwszą odpowiedzią to treść (może mieć rysunek `<svg>`).
- `- [x]` (albo `- [X]`) to odpowiedź dobra, `- [ ]` zła. Dokładnie jedna dobra, co najmniej dwie razem, bez powtórzonych tekstów.
- Linia wcięta co najmniej dwiema spacjami i zaczynająca się od `>` pod odpowiedzią to wyjaśnienie, pokazywane, gdy uczennica wybierze tę odpowiedź. Kilka takich linii skleja się w jedną.
- Aplikacja tasuje odpowiedzi.

### `{pf}`: prawda albo fałsz

```
## Znaki [1 pkt] {pf #k02}
Oceń, czy zdanie jest prawdziwe, czy fałszywe.
- [P] $(-3) * (-4) = 12$
- [F] $(-2) * 5 = 10$
```

Punkt jest tylko za ocenienie wszystkich zdań dobrze.

### `{luka}`: pola do wpisania

```
## Dzielenie z resztą [1 pkt] {luka #k11}
$47 : 6 =$ ___[7] reszty ___[5]
```

- `___[odpowiedź]` (trzy podkreślenia) to pole. Kilka dopuszczalnych odpowiedzi rozdziela `|`: `___[0,5|1/2]`. Pierwsza jest pokazywana jako poprawna.
- Porównanie ignoruje spacje i wielkość liter, kropka równa się przecinkowi, każdy rodzaj myślnika to minus. Liczby dziesiętne porównywane są jako liczby (`2,50` = `2,5`, `-0` = `0`). Ułamki zwykłe porównywane są dosłownie (`22/24` ≠ `11/12`), więc jeśli nieskrócony wynik też jest dobry, dopisz go po `|`.
- Klawiatura: gdy wszystkie odpowiedzi w zadaniu są nieujemnymi liczbami, telefon pokaże klawiaturę numeryczną. Gdy choć jedna ma minus, `/` albo litery, pełną.
- Luka może stać w akapicie, w tabeli, w liście i obok wzoru. Nie wstawiaj luki do wnętrza `$...$`, generator PDF może tego nie obsłużyć. Zamknij wzór przed luką: `$S = ($___[5], ___[1]$)$`.
- Treść luki może zawierać rysunek `<svg>`.

### `{kolejnosc}`: ułóż kroki

```
## NWW krok po kroku [1 pkt] {kolejnosc #k10}
Ułóż kroki obliczania $NWW(12, 18)$.
1. $12 = 2^2 * 3$
2. $18 = 2 * 3^2$
3. $NWW(12, 18) = 36$
```

Kroki to lista numerowana w dobrej kolejności. Linie przed listą to treść. Co najmniej dwa kroki.

### `{pary}`: dopasuj

```
## Cechy podzielności [1 pkt] {pary #k05}
Dopasuj cechę podzielności.
| przez | cecha |
|---|---|
| 2 | ostatnia cyfra parzysta |
| 3 | suma cyfr dzieli się przez 3 |
```

Pierwszy wiersz tabeli to nagłówki kolumn, wiersz `|---|` jest pomijany. Każdy kolejny wiersz to para. Co najmniej dwie pary, prawa kolumna bez powtórzeń.

### Zadanie otwarte `[odp: n]`

```
## Suma kolejnych liczb [2 pkt]
Uzasadnij, że suma trzech kolejnych liczb naturalnych dzieli się przez 3.
[odp: 4]

### Rozwiązanie
...
```

Nie ma `{typ}`. Linia `[odp: n]` mówi generatorowi PDF, ile linii zostawić na odpowiedź. Aplikacja tę linię pomija i pokazuje zadanie w „Na kartce” z rozwijanym rozwiązaniem. Nie jest oceniane, więc identyfikator nie jest wymagany.

## Fiszki

```
# Fiszki
- {#f01} Kolejność działań :: nawiasy, potęgi i pierwiastki, mnożenie i dzielenie, dodawanie i odejmowanie
- {#f02} $a * (b + c)$ :: $a * b + a * c$
```

Jedna fiszka w jednej linii: `- {#id} przód :: tył`. Obie strony mogą mieć wzory. Puste linie są pomijane, każda inna linia daje ostrzeżenie.

## Identyfikatory

- Identyfikatory zadań i fiszek są unikalne w obrębie tematu (wspólna pula dla zadań i fiszek). Bez spacji, `}` i dwukropka.
- Konwencja prefiksów: litera tematu i numer. Zadania `k01`, `k02` (liczby), `g01` (figury). Fiszki `f01` (liczby), `gf01` (figury). Nowy temat dostaje nową literę.
- Postęp leży w przeglądarce pod kluczem `nauka:<id tematu>:<id elementu>`, np. `nauka:mat-e8-figury:g07`. **Zmiana identyfikatora to utrata postępu w tym elemencie.** Poprawiając treść, zostaw identyfikator. Zadanie zmienione tak, że stary postęp nie ma sensu, dostaje nowy identyfikator, a stary zostaje nieużywany.
- Numery nie muszą iść po kolei w pliku. Nowe zadanie dostaje kolejny wolny numer, nawet jeśli stoi w środku pliku.

## Treść: bloki i wzory

Tak samo w kompendium, treści zadań, rozwiązaniach i zadaniach otwartych.

| zapis | wynik |
|---|---|
| kolejne niepuste linie | jeden akapit (linie sklejone spacją) |
| pusta linia | koniec akapitu |
| `**tekst**` | pogrubienie |
| `*tekst*` | kursywa (gwiazdka z odstępem, np. `2 * 3`, zostaje gwiazdką) |
| ` - ` (myślnik ze spacjami) | półpauza „–” |
| `- element` | lista punktowana |
| `1. element` | lista numerowana |
| `> tekst` | ramka z uwagą |
| `\| a \| b \|` i `\|---\|---\|` | tabela, pierwszy wiersz to nagłówek |
| `$...$` | wzór w tekście |
| `$$ ... $$` w jednej linii | wzór wyśrodkowany w osobnej linii |
| `<svg ...>` ... `</svg>` od początku linii | rysunek |

Nagłówków `###` i niższych nie ma w treści (poza `### Rozwiązanie`). Linków i obrazków Markdown nie ma.

### Wzory

Wewnątrz `$...$`:

| zapis | wynik |
|---|---|
| `*` | kropka mnożenia `·` |
| `-` | minus `−` |
| `x^2`, `x^{n+1}` | potęga |
| `x_1`, `x_{12}` | indeks dolny |
| `\frac{a}{b}` | ułamek piętrowy |
| `\sqrt{x}` | pierwiastek z kreską nad całym argumentem |
| `\pi` | π (można też pisać π wprost) |
| pojedyncza litera łacińska | kursywa (zmienna) |
| wyraz z kilku liter, np. `NWD` | prosto |
| dwie i więcej spacji | szeroki odstęp, np. między dwoma wzorami w jednej linii |

Inne polecenia z `\` zostaną wypisane dosłownie. Znaku `$` nie da się wpisać w tekście, bo zawsze otwiera wzór. Greckie litery, `≤`, `≈`, `°`, `²` pisz wprost.

### Rysunki `<svg>`

```
<svg viewBox="0 0 240 170" style="width:100%;max-width:240px" xmlns="http://www.w3.org/2000/svg">
<g stroke="currentColor" fill="none" stroke-width="2">
<polygon points="20,140 220,140 150,30"/>
</g>
<g fill="currentColor" font-size="16" text-anchor="middle">
<text x="110" y="160">a</text>
</g>
</svg>
```

- Blok zaczyna linia, która zaczyna się od `<svg`, a kończy linia z `</svg>`. Pustych linii w środku lepiej nie robić.
- Kolor rysuj przez `currentColor`, wtedy rysunek zmieni kolor w trybie ciemnym.
- Dozwolone elementy: `svg`, `g`, `line`, `polyline`, `polygon`, `path`, `rect`, `circle`, `ellipse`, `text`, `tspan`, `title`, `desc`, `defs`, `marker`, `linearGradient`, `radialGradient`, `stop`, `pattern`, `clipPath`, `mask`, `use`, `symbol`.
- Usuwane bez ostrzeżenia: inne elementy (`script`, `foreignObject`, `image`, `a`, `style`, animacje), atrybuty `on…`, wartości z `javascript:`, `data:`, `url(` innym niż `url(#…)`, a `href` inne niż `#kotwica`. Rysunek nie może niczego pobierać z sieci.
- Inny HTML w tekście (np. `<b>`) wyświetli się dosłownie i daje ostrzeżenie.
- W fiszkach rysunków nie ma (fiszka to jedna linia).

## Katalog `tematy/index.json`

```json
{
  "format": 1,
  "tematy": [
    {"id": "mat-e8-liczby", "tytul": "Liczby i działania", "przedmiot": "Matematyka",
     "klasa": 8, "wersja": "2026-11-03", "plik": "mat-e8-liczby.md"}
  ]
}
```

Generuje go `python3 narzedzia/katalog.py` z frontmatterów. Kolejność w katalogu to kolejność na liście tematów. Po dodaniu albo zmianie tematu uruchom skrypt i `python3 testy/run.py`, który sprawdza zgodność katalogu z plikami.

## Plik postępu (eksport)

Nie jest częścią formatu tematu, ale opisuję go tutaj, bo przenosi dane między wersjami.

```json
{
  "format": "nauka-postep",
  "wersja": 2,
  "eksport": "2026-11-03T20:00:00.000Z",
  "licznik": {"uruchomienia": 12, "pierwsze": "2026-10-30T10:00:00.000Z"},
  "ustawienia": {"klasa": "8", "ostatni": "mat-e8-figury"},
  "postep": {"mat-e8-figury:g07": {"n": 3, "ok": 2, "box": 1, "last": 1, "t": 1762200000000}},
  "tematyZPliku": {"mat-e8-nowy": "---\nid: mat-e8-nowy\n..."}
}
```

`n` to liczba podejść, `ok` liczba dobrych, `box` pudełko powtórek 0–5, `last` wynik ostatniego podejścia (1 albo 0), `t` czas ostatniego podejścia w milisekundach. Import przyjmuje też stary eksport wersji jednoplikowej `{"eksport": ..., "stan": {"items": {"temat/id": ...}, "launches": n, "first": ...}}`, w którym fiszki mają klucze `temat/f:id`.
