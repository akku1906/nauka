import sys, pathlib
silnik = pathlib.Path('silnik.html').read_text(encoding='utf-8')
paczki = []
for p in sys.argv[1:-1]:
    src = pathlib.Path(p).read_text(encoding='utf-8').replace('</script', '<\\/script')
    paczki.append('<script type="text/markdown" class="paczka">\n' + src + '\n</script>')
out = silnik.replace('<!-- PACZKI -->', '\n'.join(paczki))
pathlib.Path(sys.argv[-1]).write_text(out, encoding='utf-8')
print('ok', sys.argv[-1], len(out))
