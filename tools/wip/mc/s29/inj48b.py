import sys, json, m, ev, inj48
sys.path.insert(0, r'..\s18'); import hsim
s = open(sys.argv[1]).read() if __name__ == "__main__" else ""
SRC = {o: '} else if (%s(!strnicmp(argv[i], "%s", %d))%s {' for o in []}
OPTS = [('-noenter', 8, ''), ('-reboot', 7, ''), ('-bp', 3, 'E'), ('-rb', 3, ''), ('-wb', 3, 'E'), ('-eb', 3, 'E'), ('-s', 2, '')]
def site(o, n, e):
    if o == '-noenter': return 'if (!strnicmp(argv[i], "-noenter", 8)) {'
    return '} else if (%s) {' % ('E(!strnicmp(argv[i], "%s", %d))' % (o, n) if e else '!strnicmp(argv[i], "%s", %d)' % (o, n))
out = open('inj48b.jsonl', 'a')
for tg in sys.argv[2].split(','):
    base = inj48.mk(s, (), inj48.TG[tg])
    for o, n, e in OPTS:
        st = site(o, n, e)
        if tg and st not in base: st = st.replace('E(', '').replace(')) {', ') {') if 'E(' in st else st
        if st not in base: print('nosite', o, tg); continue
        for w in ['b', 'p', 'q', 'pq', 'pp', 'qq', 'ppp', 'pqq']:
            t = base.replace(st, st + ' if (%s) goto k48l;' % inj48.W[w]('i + 10'), 1)
            r = m.meas(t, 'i48', fncmp=True)
            if 'err' in r: print(tg, o, w, 'ERR', r['err'][-200:]); continue
            try:
                R, k = hsim.load(r'C:\Users\Win11VM\Documents\GitHub\xebuildBugFix\build\v\mc29\slot_i48'); g = R[2]['g'].get(1048)
            except Exception as ex: g = repr(ex)
            rec = [tg, o, w, ev.score_order(r['order'].split()[1:])[0], r['fncmp'], r['raw'][0][:75], str(g)[:200]]
            out.write(json.dumps(rec) + '\n'); out.flush()
            print(*rec, flush=True)
