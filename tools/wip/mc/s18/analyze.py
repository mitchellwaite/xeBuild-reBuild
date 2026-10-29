"""analyze.py SLOTDIR : real bbro dump of a slot -> round-4 order and keys in sp numbering.
Prints: order (sp), inversions vs mcsim2.WANT, and per block 'sp:P/f' (P = priority, f = freq)."""
import os, re, sys
ROOT = r'C:\Users\Win11VM\Documents\GitHub\xebuildBugFix'
sys.path.insert(0, ROOT + r'\tools\wip'); sys.path.insert(0, ROOT + r'\tools\wip\mc')
import mcvar, mcsim2

SPC = dict(zip(mcvar.WANT[:19], mcsim2.WANT[12:31]))
SPC.update({'strnicmp:-c': 73, 'strnicmp:-i': 81, 'strnicmp:-p': 86, 'strnicmp:-v': 91, 'usage:1': 93})
CALL = {'netDumpNand': 107, 'clientWrite': 108, 'clientKeys': 109, 'clientReadBlocks': 119, 'clientWriteBlocks': 120,
        'clientBinPatch': 128, 'myatoh32': 121}


def cfg(cg):
    blk = {}
    for m in re.finditer(r';; basic block (\d+), loop depth \d+\n;;  pred:([^\n]*(?:\n;;\s{10,}[^\n]*)*)\n(.*?);;  succ:([^\n]*(?:\n;;\s{10,}[^\n]*)*)', cg, re.S):
        b = int(m.group(1))
        num = lambda s: [int(x) for x in re.findall(r'(?:^|\s)(\d+)', s.replace(';;', ' '))]
        blk[b] = {'pred': num(m.group(2)), 'succ': num(m.group(4)),
                  'calls': re.findall(r'symbol_ref:SI \("(\w+)"\)[^\n]*<function_decl', m.group(3))}
    return blk


def spmap(sd):
    bbro = mcvar.section(open(os.path.join(sd, 'm.c.274r.bbro')).read(), 'mode_client')
    cg = mcvar.section(open(os.path.join(sd, 'm.c.267r.compgotos')).read(), 'mode_client')
    asm = open(os.path.join(sd, 'fdo.s')).read()
    sg = mcvar.sigs(cg, asm)
    sp = {}
    for b, s in sg.items():
        if s in SPC: sp[b] = SPC[s]
        if s == 'log:invalid mode specifi': sp[b] = 132
        if s == 'strnicmp:-ke': sp[b] = 'k48'
    blk = cfg(cg)
    inv = {v: k for k, v in sp.items()}
    for b, d in blk.items():
        for c in d['calls']:
            if c in CALL and b not in sp: sp[b] = CALL[c]
    for b, d in blk.items():
        s = set(d['succ'])
        if inv.get(112) in s and len(s) == 2: sp[b] = 110
        if inv.get(115) in s and len(s) == 2: sp[b] = 113
        if inv.get(117) in s and len(s) == 2 and not d['calls']: sp[b] = 116
        if inv.get(130) in s and len(s) == 2 and not d['calls']: sp[b] = 129
    inv2 = {v: k for k, v in sp.items()}
    if 'k48' in inv2:
        for x in blk[inv2['k48']]['succ']:
            if x != inv2.get(49): sp[x] = 'k94'
    for b, d in blk.items():
        if b in sp: continue
        if 'clientInfo' in d['calls']: sp[b] = 131
        elif 'clientPatches' in d['calls']: sp[b] = 118
        elif 'sendCompatData' in d['calls']: sp[b] = 114
    disp = max((b for b in blk if not blk[b]['calls']), key=lambda b: len(blk[b]['succ']))
    sp[disp] = 'disp'
    for b, d in blk.items():
        if b != disp and not d['calls'] and len(d['succ']) >= 3 and b not in sp: sp[b] = 'x1'
    for b, d in blk.items():
        if 'netGetInfo' in d['calls'] and inv.get(103) in d['succ']: sp[b] = 'rok'
    return bbro, sp


def freqs(bbro):
    t = bbro[bbro.index('Trace 1 ('):]
    t = t[:t.index('\n\n')] if '\n\n' in t else t
    return {int(a): int(b) for a, b in re.findall(r'(\d+) \[(\d+)\]', t)}


def keys(bbro):
    """per bb: list of (round, key) assignments; and round-4 pop order"""
    t = bbro[bbro.index('STC - round 1'):bbro.index('Trace 1 (')]
    last, rnd, order = {}, 0, []
    for l in t.split('\n'):
        m = re.match(r'STC - round (\d+)', l)
        if m: rnd = int(m.group(1)); continue
        m = re.match(r'\s*Possible start (?:point )?(?:of )?(?:this|next) round: (\d+) \(key: (-?\d+)\)', l)
        if m: last[int(m.group(1))] = int(m.group(2)); continue
        m = re.match(r'Changing key for bb (\d+) from (-?\d+) to (-?\d+)', l)
        if m: last[int(m.group(1))] = int(m.group(3)); continue
        m = re.match(r'Getting bb (\d+)', l)
        if m and rnd == 4: order.append((int(m.group(1)), last.get(int(m.group(1)))))
    return order


def dec(k):
    if k is None: return None, None
    k = -k
    return ((k - 1000000) // 100, (k - 1000000) % 100) if k >= 1000000 else (0, k)


def analyze(sd):
    bbro, sp = spmap(sd)
    o = keys(bbro)
    seen, out = set(), []
    for b, k in o:
        if b in seen: continue
        seen.add(b)
        if b in sp: out.append((sp[b], dec(k)))
    order = [s for s, _ in out]
    p = mcsim2.pos
    oo = [s for s in order if s in p]
    inv = sum(1 for a in range(len(oo)) for c in range(a + 1, len(oo)) if p[oo[a]] > p[oo[c]])
    fq = freqs(bbro)
    named = {v: fq.get(k) for k, v in sp.items() if isinstance(v, str)}
    t3 = bbro[bbro.index('Trace 1 ('):]
    named['r3'] = ' '.join('%s[%s]' % (sp.get(int(a), a), c) for a, c in re.findall(r'Trace \d+ \(round 3\):\s+(\d+) \[(\d+)\]', t3))
    named['b46'], named['b5'] = fq.get(46), fq.get(5)
    named['fq'] = {v: fq.get(k) for k, v in sp.items() if not isinstance(v, str)}
    return order, inv, dict(out), named


if __name__ == '__main__':
    order, inv, k, named = analyze(sys.argv[1])
    print(named)
    print('inv', inv)
    print('order', ' '.join(map(str, order)))
    print('keys', ' '.join('%s:%s/%s' % (s, k[s][0], k[s][1]) for s in order))
