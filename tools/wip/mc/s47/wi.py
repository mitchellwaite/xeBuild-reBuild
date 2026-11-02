"""wi.py: what-if on P's real bbro events: move the round-4 'ins' of 77/79 to every position (both orders);
report pop order of the key-0 tail. python wi.py BBRO_MC.txt"""
import sys
sys.path.insert(0, r'C:\Users\Win11VM\Documents\GitHub\xebuildBugFix\tools\wip')
import fibsim
ev = fibsim.parse(sys.argv[1])
base = [e for e in ev if not (e[0] == 'ins' and e[2] in (77, 79))]
r4 = next(i for i, e in enumerate(base) if e == ('round', 4))
T = [35, 42, 53, 77, 79]
seen = {}
def tail(o): return ' '.join(str(b) for b in o if b in T)
o, st = fibsim.run(ev, strict=False); print('orig', tail(o))
for i in range(r4 + 1, len(base)):
    for j in range(i, len(base)):
        for a, b in ((77, 79), (79, 77)):
            e2 = base[:i] + [('ins', 'this', a, 0)] + base[i:j] + [('ins', 'this', b, 0)] + base[j:]
            try: o, st = fibsim.run(e2, strict=False)
            except Exception as x: seen.setdefault("ERR "+repr(x)[:60], []).append((i,j)); continue
            t = tail(o); seen.setdefault(t, []).append((i, j, a, base[i-1], base[j-1]))
for t, l in seen.items(): print(t, len(l), l[:4])
