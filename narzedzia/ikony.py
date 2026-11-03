"""Generuje ikony aplikacji do katalogu ikony/.

Kartka w kratkę z czerwonym marginesem, żółtym zakreśleniem i zielonym ptaszkiem
na granatowym tle. Bez tekstu. Wersja „maskable” mieści rysunek w bezpiecznym
kole (40% promienia), bo Android przycina ikonę do własnego kształtu.

Uruchom: python3 narzedzia/ikony.py   (wymaga Pillow)
"""
import pathlib
from PIL import Image, ImageDraw

KORZEN = pathlib.Path(__file__).resolve().parent.parent
INK = (30, 43, 69)
PAPER = (250, 251, 247)
GRID = (214, 223, 232)
MARGIN = (235, 176, 174)
MARKER = (255, 231, 106)
GREEN = (47, 122, 75)
SKALA = 4  # rysujemy w większej rozdzielczości i zmniejszamy, żeby krawędzie były gładkie


def rysuj(rozmiar, maskable):
    s = rozmiar * SKALA
    im = Image.new('RGBA', (s, s), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    if maskable:
        d.rectangle([0, 0, s, s], fill=INK)
        kw, kh = 0.48, 0.58  # kartka mieści się w bezpiecznym kole o średnicy 80%
    else:
        d.rounded_rectangle([0, 0, s - 1, s - 1], radius=int(s * 0.22), fill=INK)
        kw, kh = 0.56, 0.68
    w, h = int(s * kw), int(s * kh)
    x0, y0 = (s - w) // 2, (s - h) // 2
    x1, y1 = x0 + w, y0 + h
    d.rounded_rectangle([x0, y0, x1, y1], radius=int(w * 0.07), fill=PAPER)
    krok = w / 7
    lw = max(1, int(s * 0.004))
    k = 1
    while y0 + k * krok < y1 - krok * 0.3:
        y = int(y0 + k * krok)
        d.line([x0 + lw, y, x1 - lw, y], fill=GRID, width=lw)
        k += 1
    k = 1
    while x0 + k * krok < x1 - krok * 0.3:
        x = int(x0 + k * krok)
        d.line([x, y0 + lw, x, y1 - lw], fill=GRID, width=lw)
        k += 1
    mx = int(x0 + krok * 1.05)
    d.line([mx, y0, mx, y1], fill=MARGIN, width=max(2, int(s * 0.012)))
    # żółte zakreślenie pod ptaszkiem
    d.rounded_rectangle([int(x0 + w * 0.26), int(y0 + h * 0.52), int(x1 - w * 0.08), int(y0 + h * 0.68)],
                        radius=int(h * 0.03), fill=MARKER)
    # ptaszek
    gr = int(s * (0.055 if maskable else 0.07))
    pkt = [(x0 + w * 0.30, y0 + h * 0.52), (x0 + w * 0.47, y0 + h * 0.70), (x0 + w * 0.80, y0 + h * 0.28)]
    pkt = [(int(a), int(b)) for a, b in pkt]
    d.line(pkt, fill=GREEN, width=gr, joint='curve')
    for a, b in (pkt[0], pkt[-1]):
        d.ellipse([a - gr // 2, b - gr // 2, a + gr // 2, b + gr // 2], fill=GREEN)
    return im.resize((rozmiar, rozmiar), Image.LANCZOS)


def main():
    out = KORZEN / 'ikony'
    out.mkdir(exist_ok=True)
    for r in (192, 512):
        rysuj(r, False).save(out / f'ikona-{r}.png', optimize=True)
        rysuj(r, True).convert('RGB').save(out / f'ikona-maskable-{r}.png', optimize=True)
    print('ok', sorted(p.name for p in out.glob('*.png')))


if __name__ == '__main__':
    main()
