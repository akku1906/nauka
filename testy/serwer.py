"""Lokalny serwer, który odtwarza GitHub Pages: pliki repozytorium pod /nauka/.

Nagłówki jak na Pages: Cache-Control max-age=600, ETag/Last-Modified (304),
typy MIME dla .webmanifest i .md. Serwer można zatrzymać i uruchomić ponownie
na tym samym porcie, co w testach udaje utratę i powrót sieci.
"""
import functools
import http.server
import socketserver
import threading

PREFIKS = '/nauka/'


class Obsluga(http.server.SimpleHTTPRequestHandler):
    extensions_map = dict(http.server.SimpleHTTPRequestHandler.extensions_map, **{
        '.webmanifest': 'application/manifest+json',
        '.md': 'text/markdown; charset=utf-8',
        '.json': 'application/json; charset=utf-8',
        '.js': 'text/javascript; charset=utf-8',
        '.html': 'text/html; charset=utf-8',
        '.png': 'image/png',
    })

    def translate_path(self, path):
        sciezka = path.split('?', 1)[0].split('#', 1)[0]
        if not sciezka.startswith(PREFIKS):
            return '/nie/istnieje'
        return super().translate_path('/' + sciezka[len(PREFIKS):])

    def send_head(self):
        if self.path.split('?', 1)[0] == PREFIKS.rstrip('/'):
            self.send_response(301)
            self.send_header('Location', PREFIKS)
            self.end_headers()
            return None
        return super().send_head()

    def end_headers(self):
        self.send_header('Cache-Control', 'max-age=600')
        super().end_headers()

    def log_message(self, *a):
        pass


class Serwer(socketserver.ThreadingMixIn, http.server.HTTPServer):
    daemon_threads = True
    allow_reuse_address = True

    def handle_error(self, request, client_address):
        pass  # przeglądarka zrywa połączenia przy przeładowaniu; to nie jest błąd testu


class SerwerTestowy:
    def __init__(self, katalog, port=0):
        self.katalog = str(katalog)
        self.port = port
        self.srv = None

    def start(self):
        obsl = functools.partial(Obsluga, directory=self.katalog)
        self.srv = Serwer(('127.0.0.1', self.port), obsl)
        self.port = self.srv.server_address[1]
        threading.Thread(target=self.srv.serve_forever, daemon=True).start()
        return self

    def stop(self):
        if self.srv:
            self.srv.shutdown()
            self.srv.server_close()
            self.srv = None

    @property
    def url(self):
        return f'http://127.0.0.1:{self.port}{PREFIKS}'


if __name__ == '__main__':
    import pathlib
    import sys
    import time
    s = SerwerTestowy(pathlib.Path(__file__).resolve().parent.parent, int(sys.argv[1]) if len(sys.argv) > 1 else 8000).start()
    print('Serwuję', s.url)
    try:
        while True:
            time.sleep(3600)
    except KeyboardInterrupt:
        s.stop()
