---
id: mat-e8-figury
tytul: Figury płaskie
przedmiot: Matematyka
tematyka: Egzamin ósmoklasisty 2027 — wzory, prawa, figury
klasa: 8
czas: 30 min
wersja: 2026-11-01
---

# Kompendium

## Kąty
Kąty **przyległe** mają wspólne ramię, a dwa pozostałe tworzą prostą. Razem dają 180°. Kąty **wierzchołkowe** leżą naprzeciw siebie przy przecięciu dwóch prostych i są równe.

<svg viewBox="0 0 320 180" style="width:100%;max-width:320px" xmlns="http://www.w3.org/2000/svg">
<g stroke="currentColor" fill="none" stroke-width="2">
<line x1="30" y1="90" x2="290" y2="90"/>
<line x1="40" y1="150" x2="280" y2="30"/>
</g>
<g fill="currentColor" font-size="16" text-anchor="middle">
<text x="215" y="82">α</text>
<text x="105" y="110">α</text>
<text x="145" y="70">β</text>
<text x="175" y="115">β</text>
</g>
</svg>

Tu $α + β = 180$°, a oba kąty α są równe, bo są wierzchołkowe.

Gdy prosta przecina dwie proste **równoległe**, kąty odpowiadające są równe i kąty naprzemianległe też są równe.

## Trójkąty
Suma kątów w każdym trójkącie wynosi 180°. Kąt zewnętrzny trójkąta jest równy sumie dwóch kątów wewnętrznych, które do niego nie przylegają.

**Nierówność trójkąta**: każdy bok jest krótszy od sumy dwóch pozostałych. Z odcinków 2, 3 i 5 trójkąta nie zbudujemy, bo $2 + 3 = 5$.

W trójkącie równoramiennym kąty przy podstawie są równe. W trójkącie równobocznym każdy kąt ma 60°.

Trójkąty są przystające, gdy zgadzają się trzy boki (bbb), dwa boki i kąt między nimi (bkb) albo bok i dwa kąty przy nim (kbk).

## Pole trójkąta
$$ P = \frac{a * h}{2} $$

<svg viewBox="0 0 240 170" style="width:100%;max-width:240px" xmlns="http://www.w3.org/2000/svg">
<g stroke="currentColor" fill="none" stroke-width="2">
<polygon points="20,140 220,140 150,30"/>
<line x1="150" y1="30" x2="150" y2="140" stroke-dasharray="5 4"/>
<path d="M150 128 h12 v12" stroke-width="1.5"/>
</g>
<g fill="currentColor" font-size="16" text-anchor="middle">
<text x="110" y="160">a</text>
<text x="160" y="90">h</text>
</g>
</svg>

Wysokość $h$ jest prostopadła do boku $a$, na który opada. Wysokość nie jest bokiem trójkąta, chyba że trójkąt jest prostokątny.

Trójkąt równoboczny o boku $a$: wysokość $h = \frac{a\sqrt{3}}{2}$, pole $P = \frac{a^2\sqrt{3}}{4}$.

## Twierdzenie Pitagorasa
W trójkącie prostokątnym kwadrat przeciwprostokątnej jest równy sumie kwadratów przyprostokątnych:

$$ a^2 + b^2 = c^2 $$

<svg viewBox="0 0 260 170" style="width:100%;max-width:260px" xmlns="http://www.w3.org/2000/svg">
<g stroke="currentColor" fill="none" stroke-width="2">
<polygon points="30,140 230,140 30,40"/>
<path d="M30 128 h12 v12" stroke-width="1.5"/>
</g>
<g fill="currentColor" font-size="16" text-anchor="middle">
<text x="130" y="160">a</text>
<text x="16" y="95">b</text>
<text x="140" y="80">c</text>
</g>
</svg>

Przeciwprostokątna $c$ leży naprzeciw kąta prostego i jest najdłuższym bokiem. Popularne trójki: 3, 4, 5; 6, 8, 10; 5, 12, 13.

Działa też w drugą stronę: jeśli $a^2 + b^2 = c^2$, to trójkąt jest prostokątny.

> Szukając przyprostokątnej, odejmujemy: $b^2 = c^2 - a^2$.

## Trójkąty szczególne
Przekątna kwadratu o boku $a$ ma długość $a\sqrt{2}$. Dzieli kwadrat na dwa trójkąty o kątach 45°, 45° i 90°.

W trójkącie o kątach 30°, 60° i 90° przyprostokątna leżąca naprzeciw kąta 30° jest dwa razy krótsza od przeciwprostokątnej. Jeśli przeciwprostokątna ma $2a$, to przyprostokątne mają $a$ i $a\sqrt{3}$.

## Czworokąty
| figura | pole |
|---|---|
| kwadrat | $a^2$ |
| prostokąt | $a * b$ |
| równoległobok | $a * h$ |
| romb | $\frac{e * f}{2}$ |
| trapez | $\frac{(a + b) * h}{2}$ |

<svg viewBox="0 0 300 170" style="width:100%;max-width:300px" xmlns="http://www.w3.org/2000/svg">
<g stroke="currentColor" fill="none" stroke-width="2">
<polygon points="20,140 280,140 200,50 80,50"/>
<line x1="80" y1="50" x2="80" y2="140" stroke-dasharray="5 4"/>
<path d="M80 128 h12 v12" stroke-width="1.5"/>
</g>
<g fill="currentColor" font-size="16" text-anchor="middle">
<text x="150" y="160">a</text>
<text x="140" y="42">b</text>
<text x="70" y="100">h</text>
</g>
</svg>

W trapezie $a$ i $b$ to podstawy, czyli boki równoległe. Przekątne rombu $e$ i $f$ przecinają się pod kątem prostym i dzielą się na połowy.

## Jednostki pola
Pole liczymy w jednostkach kwadratowych, więc przelicznik długości bierzemy do kwadratu. Skoro 1 m = 100 cm, to 1 m² = 100 * 100 cm² = 10 000 cm².

| jednostka | ile to |
|---|---|
| 1 cm² | 100 mm² |
| 1 m² | 10 000 cm² |
| 1 a (ar) | 100 m² |
| 1 ha (hektar) | 10 000 m² |
| 1 km² | 100 ha |

## Wielokąty
Suma kątów wewnętrznych $n$-kąta:

$$ (n - 2) * 180 $$

Czworokąt ma 360°, pięciokąt 540°, sześciokąt 720°. W wielokącie foremnym wszystkie kąty są równe, więc jeden kąt to suma podzielona przez $n$. Sześciokąt foremny składa się z sześciu trójkątów równobocznych, a każdy jego kąt ma 120°.

## Koło i okrąg
Okrąg to linia, a koło to cała figura razem z wnętrzem. Średnica jest dwa razy dłuższa od promienia: $d = 2r$.

$$ L = 2πr,   P = πr^2 $$

<svg viewBox="0 0 200 180" style="width:100%;max-width:200px" xmlns="http://www.w3.org/2000/svg">
<g stroke="currentColor" fill="none" stroke-width="2">
<circle cx="100" cy="90" r="70"/>
<line x1="100" y1="90" x2="170" y2="90"/>
</g>
<g fill="currentColor" font-size="16" text-anchor="middle">
<circle cx="100" cy="90" r="3"/>
<text x="135" y="82">r</text>
</g>
</svg>

Wycinek koła o kącie α to $\frac{α}{360}$ całego koła. Na przykład kąt 90° daje ćwierć koła.

> Przybliżenie $π ≈ 3,14$ stosujemy tylko wtedy, gdy zadanie o to prosi. Inaczej zostawiamy wynik z π, na przykład $25π$.

## Symetrie i układ współrzędnych
Liczba osi symetrii: kwadrat ma 4, prostokąt 2, trójkąt równoboczny 3, trójkąt równoramienny 1, koło nieskończenie wiele. Równoległobok nie ma żadnej osi, ale ma środek symetrii.

Środek odcinka o końcach $A = (x_1, y_1)$ i $B = (x_2, y_2)$:

$$ S = (\frac{x_1 + x_2}{2}, \frac{y_1 + y_2}{2}) $$

Przykład: dla $A = (2, 3)$ i $B = (8, -1)$ środek to $S = (5, 1)$.

# Zadania

## Kąty przyległe [1 pkt] {quiz #g01}
Jeden z kątów przyległych ma 65°. Ile ma drugi?
- [x] 115°
- [ ] 25°
  > To dopełnienie do 90°. Kąty przyległe dają razem 180°.
- [ ] 65°
  > Tyle samo miałby kąt wierzchołkowy, a nie przyległy.
- [ ] 295°
  > To dopełnienie do pełnego kąta 360°. Kąty przyległe tworzą półprostą, czyli 180°.

### Rozwiązanie
$180 - 65 = 115$.

## Rodzaje kątów [1 pkt] {pf #g02}
Oceń, czy zdanie jest prawdziwe, czy fałszywe.
- [P] Kąty wierzchołkowe są równe.
- [F] Kąty przyległe sumują się do 90°.
- [P] Gdy prosta przecina dwie proste równoległe, kąty odpowiadające są równe.
- [F] Kąty naprzemianległe przy prostych równoległych sumują się zawsze do 180°.

### Rozwiązanie
Kąty przyległe dają 180°, a nie 90°. Kąty naprzemianległe przy prostych równoległych są równe.

## Proste równoległe [1 pkt] {luka #g03}
Proste $a$ i $b$ są równoległe. Oblicz kąt β.

<svg viewBox="0 0 320 180" style="width:100%;max-width:320px" xmlns="http://www.w3.org/2000/svg">
<g stroke="currentColor" fill="none" stroke-width="2">
<line x1="20" y1="50" x2="290" y2="50"/>
<line x1="20" y1="130" x2="290" y2="130"/>
<line x1="146" y1="170" x2="205" y2="10"/>
<path d="M212 50 A22 22 0 0 0 197.5 29.3" stroke-width="1.5"/>
<path d="M143 130 A18 18 0 0 1 167.2 113.1" stroke-width="1.5"/>
</g>
<g fill="currentColor" font-size="16" text-anchor="middle">
<text x="226" y="38">70°</text>
<text x="136" y="114">β</text>
<text x="304" y="55">a</text>
<text x="304" y="135">b</text>
</g>
</svg>

β = ___[110]°

### Rozwiązanie
Kąt odpowiadający kątowi 70° przy prostej $b$ też ma 70°. Kąt β jest do niego przyległy, więc $β = 180 - 70 = 110$°.

## Kąt zewnętrzny [1 pkt] {quiz #g04}
Ile wynosi kąt zewnętrzny $x$? Rysunek jest poglądowy.

<svg viewBox="0 0 300 160" style="width:100%;max-width:300px" xmlns="http://www.w3.org/2000/svg">
<g stroke="currentColor" fill="none" stroke-width="2">
<polygon points="30,140 200,140 110,40"/>
<line x1="200" y1="140" x2="290" y2="140"/>
<path d="M220 140 A20 20 0 0 0 186.6 125.1" stroke-width="1.5"/>
</g>
<g fill="currentColor" font-size="16" text-anchor="middle">
<text x="62" y="132">40°</text>
<text x="110" y="66">75°</text>
<text x="222" y="122">x</text>
</g>
</svg>

- [x] 115°
- [ ] 65°
  > To kąt wewnętrzny przy tym wierzchołku. Kąt zewnętrzny jest do niego przyległy.
- [ ] 140°
  > Tu dodano 65° do 75°. Kąt zewnętrzny to suma dwóch kątów, które do niego nie przylegają: 40° i 75°.
- [ ] 180°
  > Tyle mają razem kąt zewnętrzny i wewnętrzny przy tym samym wierzchołku.

### Rozwiązanie
$x = 40 + 75 = 115$°. Inaczej: kąt wewnętrzny to $180 - 40 - 75 = 65$°, a $180 - 65 = 115$°.

## Nierówność trójkąta [1 pkt] {quiz #g05}
Z których odcinków da się zbudować trójkąt?
- [x] 4, 5, 8
- [ ] 2, 3, 5
  > $2 + 3 = 5$, więc krótsze odcinki położą się płasko na najdłuższym. Suma musi być większa, nie równa.
- [ ] 1, 2, 4
  > $1 + 2 = 3$, a to mniej niż 4. Krótsze odcinki się nie spotkają.
- [ ] 5, 5, 11
  > $5 + 5 = 10$, a to mniej niż 11.

### Rozwiązanie
$4 + 5 = 9$, a 9 jest większe od 8. Najdłuższy bok musi być krótszy od sumy dwóch pozostałych.

## Trójkąt równoramienny [1 pkt] {luka #g06}
W trójkącie równoramiennym kąt między ramionami ma 40°. Każdy kąt przy podstawie ma ___[70]°.

### Rozwiązanie
Kąty przy podstawie są równe: $(180 - 40) : 2 = 70$.

## Pole trójkąta [1 pkt] {quiz #g07}
Oblicz pole trójkąta z rysunku.

<svg viewBox="0 0 240 175" style="width:100%;max-width:240px" xmlns="http://www.w3.org/2000/svg">
<g stroke="currentColor" fill="none" stroke-width="2">
<polygon points="20,150 220,150 126,30"/>
<line x1="126" y1="30" x2="126" y2="150" stroke-dasharray="5 4"/>
<path d="M126 138 h12 v12" stroke-width="1.5"/>
</g>
<g fill="currentColor" font-size="16" text-anchor="middle">
<text x="120" y="170">10</text>
<text x="116" y="100">6</text>
<text x="60" y="85">8</text>
</g>
</svg>

- [x] $30$
- [ ] $60$
  > To $10 * 6$ bez dzielenia przez 2. Trójkąt to połowa prostokąta.
- [ ] $40$
  > Tu wzięto bok 8 zamiast wysokości. Wysokość to odcinek przerywany, prostopadły do podstawy.
- [ ] $24$
  > Tu pomnożono bok 8 przez wysokość 6. Wysokość 6 opada na bok 10, więc to z nim ją mnożymy.

### Rozwiązanie
$P = \frac{10 * 6}{2} = 30$. Bok 8 nie jest tu potrzebny.

## Pitagoras: przeciwprostokątna [1 pkt] {luka #g08}
Przyprostokątne trójkąta prostokątnego mają 6 i 8. Przeciwprostokątna ma ___[10].

### Rozwiązanie
$6^2 + 8^2 = 36 + 64 = 100$, a $\sqrt{100} = 10$.

## Pitagoras: przyprostokątna [1 pkt] {quiz #g09}
Przeciwprostokątna ma 13, a jedna przyprostokątna 5. Ile ma druga przyprostokątna?
- [x] $12$
- [ ] $8$
  > Tu odjęto same boki: $13 - 5$. Odejmujemy kwadraty boków.
- [ ] $\sqrt{194}$
  > Tu dodano kwadraty. Szukamy przyprostokątnej, więc odejmujemy: $13^2 - 5^2$.
- [ ] $144$
  > To jest kwadrat szukanego boku. Trzeba jeszcze wyciągnąć pierwiastek.

### Rozwiązanie
$b^2 = 13^2 - 5^2 = 169 - 25 = 144$, więc $b = 12$.

## Czy trójkąt jest prostokątny? [1 pkt] {pf #g10}
Oceń, czy trójkąt o podanych bokach jest prostokątny.
- [P] 6, 8, 10
- [F] 4, 5, 6
- [P] 7, 24, 25
- [F] 2, 3, 4

### Rozwiązanie
Sprawdzamy, czy suma kwadratów dwóch krótszych boków równa się kwadratowi najdłuższego. $49 + 576 = 625 = 25^2$, ale $16 + 25 = 41$, a $6^2 = 36$.

## Przekątna kwadratu [1 pkt] {quiz #g11}
Ile wynosi przekątna kwadratu o boku 5?
- [x] $5\sqrt{2}$
- [ ] $10$
  > Tu dodano dwa boki. Przekątna jest krótsza od drogi wzdłuż dwóch boków.
- [ ] $25$
  > To pole kwadratu, a nie przekątna.
- [ ] $5\sqrt{3}$
  > $\sqrt{3}$ pojawia się w trójkącie równobocznym. W kwadracie jest $\sqrt{2}$.

### Rozwiązanie
$d^2 = 5^2 + 5^2 = 50$, więc $d = \sqrt{50} = 5\sqrt{2}$.

## Trójkąt 30°, 60°, 90° [1 pkt] {luka #g12}
Oblicz długość $x$.

<svg viewBox="0 0 260 165" style="width:100%;max-width:260px" xmlns="http://www.w3.org/2000/svg">
<g stroke="currentColor" fill="none" stroke-width="2">
<polygon points="30,140 230,140 30,25"/>
<path d="M30 128 h12 v12" stroke-width="1.5"/>
</g>
<g fill="currentColor" font-size="16" text-anchor="middle">
<text x="190" y="132">30°</text>
<text x="140" y="72">12</text>
<text x="16" y="88">x</text>
</g>
</svg>

$x =$ ___[6]

### Rozwiązanie
Bok $x$ leży naprzeciw kąta 30°, więc jest dwa razy krótszy od przeciwprostokątnej: $12 : 2 = 6$. Druga przyprostokątna ma $6\sqrt{3}$.

## Wysokość trójkąta równobocznego [1 pkt] {quiz #g13}
Ile wynosi wysokość trójkąta równobocznego o boku 6?
- [x] $3\sqrt{3}$
- [ ] $6\sqrt{3}$
  > Wzór to $\frac{a\sqrt{3}}{2}$. Zabrakło dzielenia przez 2.
- [ ] $3$
  > To połowa boku, czyli odcinek, na który wysokość dzieli podstawę.
- [ ] $9\sqrt{3}$
  > To pole tego trójkąta, a nie wysokość.

### Rozwiązanie
$h = \frac{6\sqrt{3}}{2} = 3\sqrt{3}$.

## Wzory na pola [1 pkt] {pary #g14}
Dopasuj wzór na pole.
| figura | pole |
|---|---|
| kwadrat | $a^2$ |
| prostokąt | $a * b$ |
| równoległobok | $a * h$ |
| romb | $\frac{e * f}{2}$ |
| trapez | $\frac{(a + b) * h}{2}$ |
| trójkąt | $\frac{a * h}{2}$ |

### Rozwiązanie
Dzielenie przez 2 mają trójkąt, romb i trapez. Romb liczymy z przekątnych, a trapez z sumy podstaw.

## Pole trapezu [1 pkt] {luka #g15}
Oblicz pole trapezu. Rysunek jest poglądowy.

<svg viewBox="0 0 300 170" style="width:100%;max-width:300px" xmlns="http://www.w3.org/2000/svg">
<g stroke="currentColor" fill="none" stroke-width="2">
<polygon points="20,140 280,140 200,50 80,50"/>
<line x1="80" y1="50" x2="80" y2="140" stroke-dasharray="5 4"/>
<path d="M80 128 h12 v12" stroke-width="1.5"/>
</g>
<g fill="currentColor" font-size="16" text-anchor="middle">
<text x="150" y="160">10</text>
<text x="140" y="42">6</text>
<text x="70" y="100">4</text>
</g>
</svg>

$P =$ ___[32]

### Rozwiązanie
$P = \frac{(10 + 6) * 4}{2} = \frac{64}{2} = 32$.

## Romb [1 pkt] {luka #g16}
Przekątne rombu mają 6 i 8. Pole rombu to ___[24], a jego bok ma ___[5].

### Rozwiązanie
$P = \frac{6 * 8}{2} = 24$. Przekątne dzielą się na połowy pod kątem prostym, więc bok jest przeciwprostokątną trójkąta o przyprostokątnych 3 i 4: $\sqrt{9 + 16} = 5$.

## Jednostki pola [1 pkt] {quiz #g17}
Ile centymetrów kwadratowych ma 1 m²?
- [x] 10 000
- [ ] 100
  > Tyle centymetrów ma 1 metr, czyli długość. Przy polu przelicznik bierzemy do kwadratu.
- [ ] 1000
  > Tyle milimetrów ma 1 metr. Przy polu trzeba policzyć $100 * 100$.
- [ ] 1 000 000
  > Tyle milimetrów kwadratowych ma 1 m².

### Rozwiązanie
1 m = 100 cm, więc 1 m² = 100 cm * 100 cm = 10 000 cm².

## Trójkąt równoramienny krok po kroku [1 pkt] {kolejnosc #g18}
Ułóż kroki obliczania pola trójkąta równoramiennego o ramionach 10 i podstawie 12.
1. wysokość dzieli podstawę na połowy po 6
2. $h^2 + 6^2 = 10^2$
3. $h^2 = 64$
4. $h = 8$
5. $P = \frac{12 * 8}{2} = 48$

### Rozwiązanie
Wysokość opuszczona na podstawę tworzy trójkąt prostokątny z ramieniem jako przeciwprostokątną. Z twierdzenia Pitagorasa wychodzi wysokość, a potem pole.

## Kąty sześciokąta [1 pkt] {luka #g19}
Suma kątów sześciokąta to ___[720]°, a każdy kąt sześciokąta foremnego ma ___[120]°.

### Rozwiązanie
$(6 - 2) * 180 = 720$, a $720 : 6 = 120$.

## Wielokąty [1 pkt] {pf #g20}
Oceń, czy zdanie jest prawdziwe, czy fałszywe.
- [P] Suma kątów czworokąta wynosi 360°.
- [F] Suma kątów pięciokąta wynosi 450°.
- [P] Każdy kąt ośmiokąta foremnego ma 135°.
- [F] Sześciokąt foremny składa się z sześciu trójkątów prostokątnych.

### Rozwiązanie
Pięciokąt: $(5 - 2) * 180 = 540$. Ośmiokąt: $(8 - 2) * 180 : 8 = 135$. Sześciokąt foremny składa się z trójkątów równobocznych.

## Pole koła [1 pkt] {quiz #g21}
Ile wynosi pole koła o promieniu 5?
- [x] $25π$
- [ ] $10π$
  > To obwód okręgu, $2πr$. Pole to $πr^2$.
- [ ] $100π$
  > Tu do kwadratu podniesiono średnicę 10, a nie promień.
- [ ] $5π$
  > Promień trzeba podnieść do kwadratu.

### Rozwiązanie
$P = π * 5^2 = 25π$.

## Obwód okręgu [1 pkt] {luka #g22}
Okrąg ma średnicę 8. Jego obwód to ___[8]π.

### Rozwiązanie
Promień to 4, więc $L = 2π * 4 = 8π$. Krócej: obwód to średnica razy π.

## Wycinek koła [1 pkt] {luka #g23}
Koło ma promień 6. Pole wycinka o kącie 90° wynosi ___[9]π.

### Rozwiązanie
Całe koło ma pole $π * 6^2 = 36π$. Kąt 90° to $\frac{90}{360} = \frac{1}{4}$ koła, czyli $9π$.

## Osie symetrii [1 pkt] {pary #g24}
Dopasuj liczbę osi symetrii.
| figura | osie symetrii |
|---|---|
| kwadrat | 4 |
| trójkąt równoboczny | 3 |
| prostokąt, który nie jest kwadratem | 2 |
| trójkąt równoramienny, który nie jest równoboczny | 1 |
| równoległobok, który nie jest prostokątem ani rombem | 0 |
| koło | nieskończenie wiele |

### Rozwiązanie
Każda oś symetrii dzieli figurę na dwie połowy, które pokrywają się po złożeniu. Równoległobok nie ma takiej osi, ma tylko środek symetrii.

## Środek odcinka [1 pkt] {luka #g25}
$A = (2, 3)$, $B = (8, -1)$. Środek odcinka $AB$ to $S = ($___[5], ___[1]$)$.

### Rozwiązanie
$x = \frac{2 + 8}{2} = 5$, $y = \frac{3 + (-1)}{2} = 1$.

## Kąty wierzchołkowe [2 pkt]
Uzasadnij, że kąty wierzchołkowe są równe.
[odp: 4]

### Rozwiązanie
Niech α i γ będą kątami wierzchołkowymi, a β kątem przyległym do obu. Wtedy $α + β = 180$° i $γ + β = 180$°. Stąd $α = 180 - β = γ$.

# Fiszki
- {#gf01} Suma kątów trójkąta :: 180°
- {#gf02} Kąty przyległe :: sumują się do 180°
- {#gf03} Kąty wierzchołkowe :: są równe
- {#gf04} Kąt zewnętrzny trójkąta :: suma dwóch kątów wewnętrznych, które do niego nie przylegają
- {#gf05} Twierdzenie Pitagorasa :: $a^2 + b^2 = c^2$, gdzie $c$ to przeciwprostokątna
- {#gf06} Przekątna kwadratu o boku $a$ :: $a\sqrt{2}$
- {#gf07} Wysokość trójkąta równobocznego :: $\frac{a\sqrt{3}}{2}$
- {#gf08} Pole trójkąta równobocznego :: $\frac{a^2\sqrt{3}}{4}$
- {#gf09} Pole trapezu :: $\frac{(a + b) * h}{2}$
- {#gf10} Pole rombu :: $\frac{e * f}{2}$
- {#gf11} Suma kątów $n$-kąta :: $(n - 2) * 180$°
- {#gf12} Obwód okręgu :: $2πr$
- {#gf13} Pole koła :: $πr^2$
- {#gf14} 1 ha :: 10 000 m²
