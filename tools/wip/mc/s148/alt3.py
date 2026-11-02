import sys
sys.argv = ['x', sys.argv[1], '0']; exec(open('alt.py').read())
insd = {e[2] for v in g.values() for e in v if e[0]=='ins'} | {e[2] for e in pre if e[0] in ('ins',)} | {e[1] for e in pre if e[0]=='push'}
def red(c):
    if c[0] != 'dum' or c[2] == 0: return True
    e = g[c[1]][c[2]-1]
    return not (e[0] == 'visit' and e[1] not in insd)
C = [c for c in CH if red(c) and score(run([c])) <= 9]
print('filtered', len(C)); sys.stdout.flush()
for cs in itertools.combinations(C, 3):
    if not ok(cs): continue
    s = score(run(list(cs)))
    if s <= 1: print(3, s, cs); sys.stdout.flush()
print('done3')
