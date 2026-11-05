"""Attempt 19: for a getImageSmc text, which passes still have a loop in the function, and what E looks like after PRE.
loops(text) -> list of pass tags whose dump has a back edge in getImageSmc."""
import os, re, sys, tempfile
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import irlib

PASSES = ('cunrolli', 'vrp1', 'dom2', 'pre', 'cunroll', 'dom3', 'vrp2', 'optimized')


def backedge(t):
    succ = {}
    cur = None
    for l in t.split('\n'):
        m = re.match(r'\s*<bb (\d+)>:', l)
        if m:
            nb = int(m.group(1))
            if cur is not None and cur not in term:
                succ.setdefault(cur, []).append(nb)
            cur = nb
            term.discard(cur)
            continue
        if l.strip().startswith('return') and cur is not None:
            term.add(cur)
        m = re.search(r'goto <bb (\d+)>', l)
        if m and cur is not None:
            succ.setdefault(cur, []).append(int(m.group(1)))
            if l.strip().startswith('goto') and not prev_is_cond(l):
                term.add(cur)
    state = {}
    found = [False]
    def dfs(n):
        state[n] = 1
        for s in succ.get(n, []):
            if state.get(s) == 1:
                found[0] = True
            elif s not in state:
                dfs(s)
        state[n] = 2
    if succ:
        dfs(min(succ))
    return found[0]


term = set()


def prev_is_cond(l):
    return l.startswith('    ')


def analyse(text, flags=()):
    d = tempfile.mkdtemp(dir=irlib.BUILD, prefix='c')
    ok, o, _ = irlib.compile_src(text, list(flags) + ['-fdump-tree-all'], workdir=d)
    if not ok:
        return {'error': o[:300]}
    res = {}
    for f in os.listdir(d):
        m = re.search(r'\.\d+t\.([a-z_0-9-]+)$', f)
        if not m:
            continue
        t = open(os.path.join(d, f), errors='replace').read()
        k = re.search(r';; Function getImageSmc.*?(?=\n;; Function |\Z)', t, re.S)
        if k:
            res[m.group(1)] = k.group(0)
    irlib.cleanup(d)
    term.clear()
    out = {p: backedge(res[p]) for p in PASSES if p in res}
    term.clear()
    out['_passes'] = [p for p in PASSES if p in res]
    return out, res


if __name__ == '__main__':
    from gen_ir240 import fn, ATT, Z, A, SZ, ARMS, END
    from ir17lib import put
    for a in A:
        for s in SZ:
            r = analyse(put(fn('a0', 'z', a, s, 'p', 'n')))
            print(a, s, {k: v for k, v in r[0].items() if k != '_passes' and v})
