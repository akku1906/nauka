# Nauka

Aplikacja do nauki instalowana na Androidzie jako ikona (PWA): kompendium, zadania sprawdzane automatycznie, zadania na kartce i fiszki. Działa bez internetu, niczego nie wysyła, postęp zostaje w telefonie.

Adres: https://akku1906.github.io/nauka/

- `index.html`: cały silnik (HTML, CSS, JS), bez zależności i kroku budowania.
- `tematy/*.md`: treść. Składnia w [`docs/FORMAT.md`](docs/FORMAT.md). Katalog `tematy/index.json` generuje `python3 narzedzia/katalog.py`.
- `sw.js`, `manifest.webmanifest`, `ikony/`: PWA. Po zmianie powłoki uruchom `python3 narzedzia/wersja.py`.
- `narzedzia/zbuduj.py`: wersja jednoplikowa do otwarcia z pliku.
- `testy/run.py`: wszystkie testy (Python i Playwright).
- `docs/RAPORT.md`: raport z audytu i wdrożenia, z instrukcją dla rodzica.
