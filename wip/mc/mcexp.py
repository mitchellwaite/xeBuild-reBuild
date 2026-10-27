"""Expect toggles: wrap the k-th `if (` condition of the draft (from clientEraseBlock on) in E(...) and score.
python mcexp.py [k ...] | all"""
import os, re, sys
S = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, S)
import mcvar
DRAFT = os.environ.get('BASE') or r'C:\Users\Win11VM\Documents\GitHub\xebuildBugFix\wip\app\mode_client.c'
base = open(DRAFT).read()
start = base.index('void clientEraseBlock(')
conds = []
pos = start
while True:
    i = base.find('if (', pos)
    if i < 0: break
    # find the matching paren
    depth, j = 0, i + 3
    while True:
        if base[j] == '(': depth += 1
        elif base[j] == ')':
            depth -= 1
            if depth == 0: break
        j += 1
    cond = base[i + 4:j]
    if not cond.startswith('E('):
        conds.append((i + 4, j, cond))
    pos = j
def variant(ks):
    t = base
    for k in sorted(ks, reverse=True):
        a, b, c = conds[k]
        t = t[:a] + 'E(' + c + ')' + t[b:]
    return t
if __name__ == '__main__':
    flags = ['-O3', '--param', 'builtin-expect-probability=50']
    os.makedirs(os.path.join(S, 'gen'), exist_ok=True)
    if sys.argv[1:] == ['list']:
        for k, (a, b, c) in enumerate(conds): print(k, c[:70])
        sys.exit()
    ks = range(len(conds)) if sys.argv[1:] == ['all'] else [[int(x) for x in a.split(',')] for a in sys.argv[1:]]
    for k in ks:
        kk = k if isinstance(k, list) else [k]
        p = os.path.join(S, 'gen', 'exp_%s.c' % '_'.join(map(str, kk)))
        open(p, 'w', newline='\n').write(variant(kk))
        res, err = mcvar.run(p, flags, fncmp=bool(os.environ.get('FNCMP')))
        if res is None: print(kk, 'ERR', err[:100]); continue
        print('%-10s inv=%2d pre=%2d%s %s' % (kk, res['inv'], res['pre'], ' fncmp=%d' % res['fncmp'] if 'fncmp' in res else '', ' '.join(res['order'][:12])), flush=True)
