import sys, re, itertools, m, ev, json
sys.path.insert(0, r'..\s18'); import hsim
src0 = open(sys.argv[1]).read()
L0 = src0.index('for (i = 0; i < argc; i++) {', src0.index('int mode_client('))
TS = []
for mm in re.finditer(r'if \((E\()?(!strnicmp\(argv\[i\], "[^"]+", \d+\))\)?\)', src0[L0:L0 + 6000]):
    TS.append((L0 + mm.start(), mm.group(0), mm.group(2), bool(mm.group(1))))
print([t[2] for t in TS])
def tog(src, idx):
    for i in sorted(idx, reverse=True):
        p, full, inner, has = TS[i]
        new = 'if (%s)' % inner if has else 'if (E(%s))' % inner
        src = src[:p] + new + src[p + len(full):]
    return src
out = open(sys.argv[2], 'a')
for n in [int(x) for x in sys.argv[3].split(',')]:
    for idx in itertools.combinations(range(len(TS)), n):
        r = m.meas(tog(src0, idx), 't48', fncmp=False)
        if 'err' in r: continue
        try:
            R, k = hsim.load(r'C:\Users\Win11VM\Documents\GitHub\xebuildBugFix\build\v\mc29\slot_t48')
            g = R[2]['g'].get(1048)
        except Exception as e: g = repr(e)
        s = ev.score_order(r['order'].split()[1:])[0]
        rec = [s, [TS[i][2] for i in idx], r['raw'][0][:70], str(g)[:300], r['order']]
        out.write(json.dumps(rec) + '\n'); out.flush()
        if 'chg' in str(g): print(rec, flush=True)
