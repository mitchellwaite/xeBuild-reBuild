"""gen.py: plain-compile variants of src/mode_client.c with asm-goto priority edges.
spec = {'J': set of active existing JUMP sites (0 RX126 efail, 1 X2 rok, 2 X1 switch, 3 RX117 p0->i0)
        or {idx: 'lab1,lab2'} to override the label list,
        'ins': [(anchor, text, where)]  where 'a' = after the anchor's line end... see below}
AT(l) labels are always emitted (unused labels don't change code)."""
import os, re
ROOT = r'C:\Users\Win11VM\Documents\GitHub\xebuildBugFix'
SRC = open(os.path.join(ROOT, 'src', 'mode_client.c'), newline='').read()
A = SRC.index('#ifdef BUILD_FDO'); B = SRC.index('#endif', A) + 6
HDR = ('#define NOPROF\n#define AT(l) l:\n#define JUMP(...)\n#define JMP(...) __asm__ goto ("" :::: __VA_ARGS__)\n'
       '#define NO_MODE_ARG(m, a) (!((m) && (a)))\n')
BODY = SRC[:A] + HDR + SRC[B:]
SITES = [m.start() for m in re.finditer(r'JUMP\(', BODY) if not BODY[m.start()-8:m.start()].endswith('define ')]
def make(spec):
    out = BODY
    J = spec.get('J', {})
    if not isinstance(J, dict): J = {j: None for j in J}
    ins = []
    for i, p in enumerate(SITES):
        if i in J:
            e = out.index(')', p)
            lab = J[i] if J[i] else out[p + 5:e]
            ins.append((p, e + 1, 'JMP(%s)' % lab))
    for anchor, text, where in spec.get('ins', []):
        n = 0
        if '#' in anchor and anchor.rsplit('#', 1)[1].isdigit():
            anchor, n = anchor.rsplit('#', 1); n = int(n)
        p = -1
        for _ in range(n + 1): p = out.index(anchor, p + 1)
        if where == 'b': ins.append((p, p, text))
        elif where == 'a': q = p + len(anchor); ins.append((q, q, text))
        elif where == 'eol': q = out.index('\n', p); ins.append((q, q, text))
    for s, e, t in sorted(ins, key=lambda x: -x[0]):
        out = out[:s] + t + out[e:]
    if spec.get('nma'):
        out = out.replace('#define NO_MODE_ARG(m, a) (!((m) && (a)))', '#define NO_MODE_ARG(m, a) (!(m) || ({ __asm__(""); 0; }) || !(a))')
    return out
