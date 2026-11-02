"""es.py: fine-grained event score vs s18 MATCH history. score = sum over rounds 1-4 of W[r] * edit distance
between flattened event token sequences (group headers included as tokens). run(text, tag) -> dict."""
import re, sys, os, io, contextlib, difflib
R = r'C:\Users\Win11VM\Documents\GitHub\xebuildBugFix'
sys.path.insert(0, os.path.join(R, r'tools\wip\mc\s50')); sys.path.insert(0, os.path.join(R, r'tools\wip\mc\s42'))
sys.path.insert(0, os.path.join(R, r'tools\wip\mc\s18')); sys.path.insert(0, os.path.join(R, r'tools\wip'))
import hsim, ev
W = {1: 8, 2: 4, 3: 2, 4: 1}
def toks(slot):
    Rr, keys = hsim.load(slot); out = {}
    for ri, r in enumerate(Rr, 1):
        t = ['pre'] + [('%s%s' % (x[0][0], x[1]) if x[0] != 'ins' else 'i%s:%s' % (x[2], x[1][0])) for x in r['pre']]
        for b, es in r['g'].items():
            t.append('G%s' % b); t += [('%s%s' % (x[0][0], x[1]) if x[0] != 'ins' else 'i%s:%s' % (x[2], x[1][0])) for x in es]
        out[ri] = t
    # canonicalize anonymous (>=1000) block ids by first appearance (offset-invariant)
    mp = {}
    def cn(m):
        n = int(m.group(2))
        if n < 1000: return m.group(0)
        return m.group(1) + 'X%d' % mp.setdefault(n, len(mp))
    return {r: [re.sub(r'^(\D+)(\d+)', cn, x) for x in t] for r, t in out.items()}
M = toks(os.path.join(R, 'build', 'mcmatch', 'slotm'))
def dist(a, b):
    sm = difflib.SequenceMatcher(None, a, b, autojunk=False)
    return sum(max(i2 - i1, j2 - j1) for op, i1, i2, j1, j2 in sm.get_opcodes() if op != 'equal')
def escore(slot):
    T = toks(slot); per = {r: dist(M.get(r, []), T.get(r, [])) for r in set(M) | set(T)}
    return sum(W.get(r, 1) * d for r, d in per.items()), per
def run(text, tag, fncmp=False):
    with contextlib.redirect_stdout(io.StringIO()):
        r = ev.ev(text, tag, fncmp=fncmp)
    if r is None: return None
    try: s, per = escore(os.path.join(R, 'build', 'v', 'mc42', 'slot_' + tag))
    except Exception as e: s, per = 9999, repr(e)
    return {'score': r['score'], 'fncmp': r.get('fncmp'), 'es': s, 'per': per}
if __name__ == '__main__':
    if sys.argv[1].endswith('.c'): print(run(open(sys.argv[1]).read(), sys.argv[2], True))
    else: print(escore(sys.argv[1]))
