"""python tools/wip/dehint/rfone.py <generator.py> <tag> <out.c>: write one sweep variant to out.c."""
import importlib.util, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
gen, want, out = sys.argv[1:4]
spec = importlib.util.spec_from_file_location('g', gen)
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
base = open(os.path.join(ROOT, 'src', 'fileutil.c')).read()
a, b = base.index('/*\n * readFileIn:'), base.index('unsigned int calcConfigSum')
for v in m.variants():
    if v[0] == want:
        head = base[:a]
        for old, new in (v[3] if len(v) > 3 else []):
            head = head.replace(old, new)
        open(out, 'w', newline='\n').write(head + v[1].strip('\n') + '\n\n' + base[b:])
        break
else:
    sys.exit('no such tag: ' + want)
