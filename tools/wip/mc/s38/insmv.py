"""insmv.py TAG [f-deltas]: what-if: relocate round-4 insertion of a tail block to another point (pre index / during pop of b)."""
import sys, os, copy
R0 = r'C:\Users\Win11VM\Documents\GitHub\xebuildBugFix'
sys.path.insert(0, R0 + r'\tools\wip\mc\s18'); sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import hsim, pot
R, k = hsim.load(os.path.join(R0, 'build', 'v', 'mc38', 'slot_' + sys.argv[1])); f, P = hsim.measured(k)
for a in sys.argv[2:]:
    if a:
        for x in a.split(','): b, d = x.split(':'); f[int(b)] += int(d)
print('base', pot.tinv(hsim.sim(R, f, P)))
r4 = R[3]
print('pre', [e[:3] for e in r4['pre'] if e[0] == 'ins'])
T = [127, 117, 130, 35, 42, 53, 77, 79, 33, 29, 67, 73, 81]
pops = list(r4['g'].keys())
res = []
for t in T:
    # find and remove
    R2 = copy.deepcopy(R); g = R2[3]
    ev = None
    for i, e in enumerate(g['pre']):
        if e[0] == 'ins' and e[2] == t: ev = e; del g['pre'][i]; src = 'pre'; break
    if ev is None:
        for b, es in g['g'].items():
            for i, e in enumerate(es):
                if e[0] == 'ins' and e[2] == t: ev = e; src = b; del es[i]; break
            if ev: break
    if ev is None: continue
    ev2 = ('ins', 'this', t, ev[3]) if len(ev) == 4 else ev
    for j in range(len(g['pre']) + 1):
        R3 = copy.deepcopy(R2); R3[3]['pre'].insert(j, ('ins', 'this', t, ev[3]))
        try: res.append((pot.tinv(hsim.sim(R3, f, P)), t, src, 'pre%d' % j))
        except Exception as x: pass
    for b in pops:
        for pos in ('head', 'tail'):
            R3 = copy.deepcopy(R2); es = R3[3]['g'][b]
            e2 = ('ins', 'this', t, ev[3])
            if pos == 'head': es.insert(0, e2)
            else: es.append(e2)
            try: res.append((pot.tinv(hsim.sim(R3, f, P)), t, src, '%s@%d' % (pos, b)))
            except Exception: pass
res.sort(key=lambda z: z[0])
for r in res[:30]: print(r)
def apply_mv(Rx, t, where):
    g = Rx[3]; ev = None
    for b, es in g['g'].items():
        for i, e in enumerate(es):
            if e[0] == 'ins' and e[2] == t: ev = e; del es[i]; break
        if ev: break
    if ev is None: return False
    pos, b = where.split('@'); b = int(b); e2 = ('ins', 'this', t, ev[3])
    if b not in g['g']: return False
    if pos == 'head': g['g'][b].insert(0, e2)
    else: g['g'][b].append(e2)
    return True
if os.environ.get('PAIR'):
    top = [r for r in res if r[0] <= 6 and r[3][:3] != 'pre']
    out = []
    for i in range(len(top)):
        for j in range(i + 1, len(top)):
            if top[i][1] == top[j][1]: continue
            Rx = copy.deepcopy(R)
            if not apply_mv(Rx, top[i][1], top[i][3]) or not apply_mv(Rx, top[j][1], top[j][3]): continue
            try: out.append((pot.tinv(hsim.sim(Rx, f, P)), top[i][1:], top[j][1:]))
            except Exception: pass
    out.sort(key=lambda z: z[0])
    for o in out[:20]: print(o)
