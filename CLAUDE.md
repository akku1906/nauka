# Nauka — aplikacja do nauki (PWA)

Jedna aplikacja webowa instalowana na Androidzie jako ikona (PWA), dla dwóch uczennic: klasy 8 i klasy 4. Silnik powstaje raz, a wiedza to pliki tematów w Markdown. Nie ma serwera, kont ani AI na żywo. Postęp zostaje wyłącznie w telefonie, a aplikacja niczego nie wysyła.

## Twarde zasady

- Repozytorium jest PUBLICZNE. Nie wpisuj imion dzieci, nazwy szkoły, nazwisk ani żadnych danych osobowych, ani w kodzie, ani w treściach, commitach czy PR. Uczennice to „kl. 8” i „kl. 4”.
- Interfejs i treści są po polsku. W tekstach dla ludzi używaj cudzysłowów „ ”.
- Autor commitów: `Artur <127636071+akku1906@users.noreply.github.com>`. Ustaw to w `git config` na początku sesji.
- Jest jedno źródło treści: pliki `tematy/*.md` w składni generatora (frontmatter, potem `# Kompendium`, `# Zadania`, `# Fiszki`). Format jest kontraktem z osobnym generatorem PDF. Zmieniaj go tylko wstecznie zgodnie i opisuj w `docs/FORMAT.md`.
- Aplikacja w działaniu nie pobiera niczego spoza repozytorium: bez CDN, bez fontów Google, bez analityki. Wszystko leży w repo i trafia do pamięci service workera.
- Używaj wyłącznie ścieżek względnych, bo strona działa pod podkatalogiem `/nauka/` na `akku1906.github.io`.
- Klucze zapisu w przeglądarce mają prefiks `nauka:` i zawierają identyfikator tematu, np. `nauka:mat-e8-figury:g07`. Domena `akku1906.github.io` jest wspólna dla wszystkich przyszłych stron z tego konta.
- Nie łam istniejącego zapisu postępu bez migracji.
- Przed każdym commitem zmieniającym silnik uruchom testy: `python3 testy/run.py`.
- W repozytorium musi być plik `.nojekyll` (bez niego GitHub Pages przepuszcza pliki `.md` z frontmatterem przez Jekylla i tematy zwracają 404).

## Czego nie robić

- Nie dodawaj frameworków ani kroku budowania przez npm. Zostajemy przy zwykłym HTML, JS i CSS.
- Nie usuwaj eksportu i importu postępu ani paska stanu z numerem uruchomienia. To narzędzia diagnostyczne.
- Nie dodawaj trybu dla kl. 4 z grywalizacją ani tutora AI. To osobne etapy.
