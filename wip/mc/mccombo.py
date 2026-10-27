import os, sys, itertools
S = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, S)
import mcgen, mcvar
names = sys.argv[1].split(',')
flags = ['-O3', '--param', 'builtin-expect-probability=50']
for r in range(0, len(names) + 1):
    for c in itertools.combinations(names, r):
        try:
            t = mcgen.make(list(c))
        except AssertionError as e:
            print(c, 'SKIP'); continue
        p = os.path.join(S, 'gen', 'cb_' + ('_'.join(c) or 'none') + '.c')
        open(p, 'w', newline='\n').write(t)
        res, err = mcvar.run(p, flags, fncmp=True)
        if res is None: print(c, 'ERR'); continue
        print('%-45s inv=%2d pre=%2d fncmp=%3d %s' % ('+'.join(c) or 'none', res['inv'], res['pre'], res['fncmp'], ' '.join(res['order'][:6])), flush=True)
