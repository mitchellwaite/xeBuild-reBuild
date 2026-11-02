"""pick.py TAB.jsonl BASETAG STATE.json 'b:+d,...' OUTSTATE.json: choose neutral single-effect table entries
realizing the target f deltas, predict with hsim, realize (real compile) and report."""
import sys, os, json
os.environ['DUP'] = '1'; os.environ['LU'] = '1'
R0 = r'C:\Users\Win11VM\Documents\GitHub\xebuildBugFix'
sys.path.insert(0, R0 + r'\tools\wip\mc\s18'); sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import hsim, pot, gs, ev
R, keys = hsim.load(os.path.join(R0, 'build', 'v', 'mc35', 'slot_' + sys.argv[2])); f0, P0 = hsim.measured(keys)
L = [json.loads(l) for l in open(sys.argv[1])]
tgt = {int(a.split(':')[0]): int(a.split(':')[1]) for a in sys.argv[4].split(',')}
st = json.load(open(sys.argv[3])); f = dict(f0); used = set(); miss = []
for b, d in tgt.items():
    c = [x for x in L if x['nev'] == 0 and list(x['df']) == [str(b)] and None not in x['df'][str(b)]
         and x['df'][str(b)][1] - x['df'][str(b)][0] == d]
    c = [x for x in c if json.dumps(gs_slot := (x['add'][0][0][0] if x['add'][0] else x['add'][1][0][:2] + [x['add'][1][0][3]])) not in used]
    if not c: miss.append(b); continue
    x = min(c, key=lambda x: x['fncmp'])
    used.add(json.dumps(x['add'][0][0][0] if x['add'][0] else x['add'][1][0][:2] + [x['add'][1][0][3]]))
    st['v'] += x['add'][0]; st['a'] += x['add'][1]; f[b] += d
    print('use', b, d, x['add'], x['fncmp'])
print('missing', miss, 'pred', pot.tinv(hsim.sim(R, f, P0)))
# arm injections sharing (arm, n): renumber n so each is distinct
seen = {}
for a in st['a']:
    k = a[1]; seen[k] = seen.get(k, 0) + 1; a[3] = 10 * seen[k] if a[1] != 'top' else a[3]
ns = {}
for a in st['a']:
    if a[1] == 'top': ns[a[3]] = ns.get(a[3], 0) + 1; a[3] = a[3] + 100 * (ns[a[3]] - 1)
json.dump(st, open(sys.argv[5], 'w'))
r = ev.ev(gs.build(st), 'pk', True); print('REAL', r['score'], r['fncmp'], ' '.join(map(str, r['o'][12:])))
