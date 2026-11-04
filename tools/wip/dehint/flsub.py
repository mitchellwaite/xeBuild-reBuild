"""flsub.py [flash sec seclen flen raw] ...: all subsets of parseIni's dead tests over shapes.
Each argument is a comma list for that axis; output build/filelist_ini/sub_<args>.txt."""
import itertools, sys
import fllib as L
import flpi as P

axes = sys.argv[1:] or ['nest', 'cur', 'goto', 'asm', 'asm,else']
ax = [a.split(',') for a in axes]
V = {}
names = P.ALLDEAD
for k in itertools.product(*ax):
    for r in range(len(names) + 1):
        for rm in itertools.combinations(names, r):
            V['_'.join(k) + '__' + '+'.join(rm)] = P.gen(*k, dead=rm)
print(len(V))
rs = L.sweep(V, prefix='sub', show=25)
with open(L.BD + '/sub_%s.txt' % '_'.join(a.replace(',', '') for a in axes), 'w', newline='\n') as f:
    for n, (sc, st, fd, sd) in rs:
        f.write('%s %s %s %s\n' % (sc, n, fd, sd))
