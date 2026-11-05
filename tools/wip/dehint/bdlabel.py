"""python tools/wip/dehint/bdlabel.py gen.py "label" out.c: write one case of a bdrun generator without scoring the others, then print its score."""
import importlib.util, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bdlib, bdrun

gen, lab, out = sys.argv[1:4]
spec = importlib.util.spec_from_file_location('gen', gen)
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
base = bdlib.read_src(os.path.join(bdlib.R, getattr(m, 'BASE', 'src/build.c')))
if hasattr(m, 'PRE'):
    base = m.PRE(base)
for l, f in m.CASES(base):
    if l == lab:
        t = f(base) if callable(f) else f
        open(out, 'w', newline='\n').write(t)
        r = bdrun.score(t)
        print(lab, 'IDENTICAL' if r.get('identical') else r)
        break
else:
    print('no such label')
