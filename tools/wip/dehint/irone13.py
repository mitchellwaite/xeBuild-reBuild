"""python tools/wip/dehint/irone13.py <gen.py> <label+label> <out.c>: write one variant of a generator (attempt 13)."""
import importlib.util, itertools, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import irlib
s = importlib.util.spec_from_file_location('gen', sys.argv[1])
m = importlib.util.module_from_spec(s)
s.loader.exec_module(m)
text = open(os.path.join(irlib.R, getattr(m, 'BASE', 'src/image_read.c')), newline='').read().replace('\r\n', '\n')
want = sys.argv[2]
for c in itertools.product(*m.AXES):
    if '+'.join(x[0] for x in c if x[0]) == want:
        t = text
        for lab, ed in c:
            for a, b in ed:
                assert a in t, a[:60]
                t = t.replace(a, b)
        open(sys.argv[3], 'w', newline='\n').write(t)
        print(irlib.fmt(irlib.score_text(t, []))[:200])
        break
