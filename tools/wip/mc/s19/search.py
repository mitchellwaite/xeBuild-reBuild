"""Greedy search for dead-edge frequency injections into mode_client (plain compile).
python build/v/mc19/search.py [steps] [start.json]
An injection (tgt, src, w): a label before the tgt-th call statement in mode_client and
`if (<w>) goto <label>;` at source location src, w a condition on __builtin_constant_p
(folded to 0 only in fab, after the loop passes; the frequency it adds stays).
Scores with tools/wip/mc/mcvar.py (inv, pre) and fncmp; prints each step's best."""
import json, os, re, sys
ROOT = r'C:\Users\Win11VM\Documents\GitHub\xebuildBugFix'
sys.path.insert(0, os.path.join(ROOT, 'tools', 'wip', 'mc'))
import mcvar
FLAGS = ['-O3', '-fno-toplevel-reorder', '-fno-ipa-profile', '-fno-reorder-functions',
         '--param', 'builtin-expect-probability=50', '-I' + os.path.join(ROOT, 'src')]
SRC = open(os.path.join(ROOT, 'src', 'mode_client.c'), newline='').read()
D = os.path.join(ROOT, 'build', 'v', 'mc19')
FN0 = SRC.index('int mode_client(int argc')
LOOP0 = SRC.index('\tfor (i = 0; i < argc; i++) {', FN0)
LOOP1 = SRC.index('\tif (NO_MODE_ARG(mode, arg))', FN0)
EB0 = SRC.index('void clientEraseBlock(')
EB1 = SRC.index('\n}\n', EB0)

# targets: call statements (start offsets) in mode_client's cold code and clientEraseBlock
CALLS = re.compile(r'\b(client_usage|log_printf|clientPatches|clientInfo|netDumpNand|clientWrite|clientKeys|'
                   r'sendAvatarData|sendCompatData|clientReadBlocks|clientWriteBlocks|clientEraseBlock|clientBinPatch)\s*\(')
TGT = []
for m in CALLS.finditer(SRC, FN0):
    TGT.append(('mc', m.start()))
for m in CALLS.finditer(SRC, SRC.index('{', EB0), EB1):
    TGT.append(('eb', m.start()))

def inloop(off):
    return LOOP0 < off < LOOP1

# sources: (name, insertion offset, variable for bcp, region)
SRCS = {
    'top': (SRC.index('\t\tif (!strnicmp(argv[i], "help", 2)', LOOP0), 'i', 'loop'),
    'after': (LOOP1, 'mode', 'post'),
    'rok': (SRC.index('\t\t\t\tJUMP(c12', FN0), 'mode', 'post'),
    'fail': (SRC.index('\tlog_printf(0, "\\n\\n***** ERROR: unable to connect', FN0), 'mode', 'post'),
    'ebtop': (SRC.index('\tif (block != -1) {', EB0), 'block', 'eb'),
}
B = lambda v: '__builtin_constant_p(%s)' % v
P = lambda v: '(char *)%s == (char *)1' % B(v)
Q = lambda v: '%s == 3' % B(v)
# (__builtin_expect is 50% in this object: builtin-expect-probability=50)
W = {'p': lambda v: P(v), 'q': lambda v: Q(v), 'b': lambda v: B(v),
     'pq': lambda v: '%s && %s' % (P(v), Q(v + ' + 1')), 'pp': lambda v: '%s && %s' % (P(v), P(v + ' + 1')),
     'qq': lambda v: '%s && %s' % (Q(v), Q(v + ' + 1')),
     'ppp': lambda v: '%s && %s && %s' % (P(v), P(v + ' + 1'), P(v + ' + 2')),
     'pqq': lambda v: '%s && %s && %s' % (P(v), Q(v + ' + 1'), Q(v + ' + 2'))}

def ok(t, s):
    kind, off = TGT[t]
    reg = SRCS[s][2]
    if kind == 'eb':
        return reg == 'eb'
    if reg == 'eb':
        return False
    if inloop(off):
        return reg == 'loop' and off > SRCS[s][0]
    # after the loop: no target upstream of its source (no new cycle)
    if s == 'after':
        return reg == 'post' and off > SRCS[s][0]
    return reg == 'post' and off > LOOP1 and TGT[t][1] != SRCS[s][0]

def make(inj):
    ins = []
    for n, (t, s, w) in enumerate(inj):
        lab = 'dz%d' % n
        off, var, _ = SRCS[s]
        ins.append((TGT[t][1], '%s: ' % lab))
        # a distinct argument per injection, or FRE merges the tests
        ins.append((off, 'if (%s) goto %s;\n' % (W[w]('%s + %d' % (var, 10 * (n + 1))), lab)))
    out = SRC
    for off, txt in sorted(ins, key=lambda x: -x[0]):
        out = out[:off] + txt + out[off:]
    return out

def score(inj, tag='cur'):
    p = os.path.join(D, 'v_%s.c' % tag)
    open(p, 'w', newline='\n').write(make(inj))
    res, err = mcvar.run(p, FLAGS, fncmp=True)
    if res is None:
        return None
    return res

def key(r):
    return r['fncmp'] + 2 * r['inv'] + 10 * len(r['missing'])

if __name__ == '__main__':
    steps = int(sys.argv[1]) if len(sys.argv) > 1 else 6
    cur = json.load(open(sys.argv[2])) if len(sys.argv) > 2 else []
    cur = [tuple(x) for x in cur]
    r = score(cur)
    best = key(r)
    print('start', cur, 'inv', r['inv'], 'pre', r['pre'], 'fncmp', r['fncmp'], flush=True)
    for st in range(steps):
        cand = None
        for t in range(len(TGT)):
            for s in SRCS:
                if not ok(t, s):
                    continue
                for w in W:
                    inj = cur + [(t, s, w)]
                    rr = score(inj)
                    if rr is None:
                        continue
                    k = key(rr)
                    if cand is None or k < cand[0]:
                        cand = (k, inj, rr)
        if cand is None or cand[0] >= best:
            print('no improvement', flush=True)
            break
        best, cur, r = cand
        line = SRC[TGT[cur[-1][0]][1]:SRC.index('\n', TGT[cur[-1][0]][1])].strip()
        print('step', st, cur[-1], line[:60], 'inv', r['inv'], 'pre', r['pre'], 'fncmp', r['fncmp'], flush=True)
        json.dump(cur, open(os.path.join(D, 'best.json'), 'w'))
        print('   ', ' '.join(r['order']), flush=True)
