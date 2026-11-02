"""ebt.py STATE.json TAG 'src:w:tgt:n;...' : build STATE + eb bcp items, measure, cm."""
import json, sys, os
os.environ['DUP'] = '1'; os.environ['LU'] = '1'
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gs, ev, ebl, cm
st = json.load(open(sys.argv[1])); it = [(a, b, c, int(d)) for a, b, c, d in (x.split(':') for x in sys.argv[3].split(';') if x)]
st.setdefault('e', []); st['e'] = st['e'] + [list(x) for x in it]
r = ev.ev(ebl.ebinj(gs.build(st), [tuple(x) for x in st['e']]), sys.argv[2], True)
print(r['score'], r['fncmp'], ' '.join(map(str, r['o'][12:])))
print('cm', cm.cm(os.path.join(r'C:\Users\Win11VM\Documents\GitHub\xebuildBugFix\build\v\mc35', 'v_%s.c' % sys.argv[2])))
if len(sys.argv) > 4: json.dump(st, open(sys.argv[4], 'w'))
