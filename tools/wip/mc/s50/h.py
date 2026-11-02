"""h.py: evaluate H5c2 + edits: ev score/fncmp + round-3 feature score vs s18 match.
as module: run(text, tag) -> dict(score, fncmp, r3, r3s, hist)"""
import sys, os, io, contextlib
R = r'C:\Users\Win11VM\Documents\GitHub\xebuildBugFix'
sys.path.insert(0, os.path.join(R, r'tools\wip\mc\s42')); sys.path.insert(0, os.path.join(R, r'tools\wip\mc\s18')); sys.path.insert(0, os.path.join(R, r'tools\wip'))
import ev, hsim
BASE = open(os.path.join(R, r'tools\wip\mc\s47\H5c2.c')).read()
def hist(tag):
    Rr, keys = hsim.load(os.path.join(R, 'build', 'v', 'mc42', 'slot_' + tag))
    out = []
    for ri, r in enumerate(Rr, 1):
        for b, es in r['g'].items():
            out.append((ri, b, [('%s%s' % (x[0][0], x[1]) if x[0] != 'ins' else 'i%s:%s' % (x[2], x[1][0])) for x in es]))
    return out
def r3feat(h):
    r3 = [(b, e) for ri, b, e in h if ri == 3]
    flat = [x for b, e in r3 for x in e]
    s = 0
    if 'v94' in flat: s += 3
    for k in (112, 115, 103, 132):
        if 'c%d' % k not in flat: s += 1
    for k in (115, 112, 131, 118):
        if 'p%d' % k not in flat: s += 1
    pu = [x for x in flat if x[0] == 'p']
    try:
        if pu.index('p53') < pu.index('p42'): s += 1
        if pu.index('p53') < pu.index('p35'): s += 1
    except ValueError: s += 2
    return s, ' | '.join('g%s:%s' % (b, ' '.join(e)) for b, e in r3 if any(x[0] != 'p' for x in e))
def run(text, tag, fncmp=False):
    with contextlib.redirect_stdout(io.StringIO()):
        r = ev.ev(text, tag, fncmp=fncmp)
    if r is None: return None
    try: h = hist(tag); s, d = r3feat(h)
    except Exception as e: s, d = 99, repr(e)
    return {'score': r['score'], 'fncmp': r.get('fncmp'), 'r3s': s, 'r3': d, 'o': r['o'], 'fq': r['fq']}
if __name__ == '__main__':
    t = open(sys.argv[1]).read() if len(sys.argv) > 1 else BASE
    print(run(t, sys.argv[2] if len(sys.argv) > 2 else 'h0', fncmp=True))
