"""image_write's tricks as named source edits.  Importable; also a CLI:

python tools/wip/dehint/iwtricks.py singles          every trick removed alone
python tools/wip/dehint/iwtricks.py pairs [names..]  every pair (of names, default all)
python tools/wip/dehint/iwtricks.py greedy           greedy descent from the full source
python tools/wip/dehint/iwtricks.py show a,b,c [-o out.c] : score that combination, optional output
Base text: src/image_write.c, or IWBASE=<file>.

`param` removes the --param (it only acts on __builtin_expect)."""
import itertools, os, sys
from concurrent.futures import ThreadPoolExecutor
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import iwlib

T = {
    'exp_file': [('if (__builtin_expect(lim >= off + len, 1)) {', 'if (lim >= off + len) {')],
    'exp_mob': [('if (__builtin_expect(imgFits(off, len), 1)) {', 'if (imgFits(off, len)) {')],
    'lab_lnp2': [('''		else {
			/* imgAddFile's clone: keeps DOM2's threading from zeroing the npages guard edge */
			lnp2: __attribute__((hot));
		}
''', '')],
    'lab_c1': [('''			c1: __attribute__((cold));
''', '')],
    'dead_c1': [('''		/* dead; cold, so the threading that removes it doesn't leave the
		   error edge at 75% (the error block is then laid out after the
		   big-block path) */
		if ((len & 0x3fff) > 0x3fff) {
			c1: __attribute__((cold));
			name++;
		}
''', '')],
    'dead_lenpp': [('''	if ((len & 0x3fff) > 0x3fff)
		len++;
''', '')],
    'opt': [('__attribute__((optimize("no-tree-scev-cprop"))) void writeFsTable', 'void writeFsTable')],
    'xmalloc': [('void *xmalloc(size_t) __asm__("_malloc") __attribute__((malloc));\n', ''),
                ('xmalloc(xb.rawSize)', 'malloc(xb.rawSize)')],
    'pin_bb': [('''			bb = xb.bigBlock;
			__asm__("" :: "b"(bb));
			if (bb)
''', '''			if (xb.bigBlock)
''')],
    'pin_t': [('''			__asm__("" :: "g"(t));
''', '')],
    'pin_end': [('''	__asm__("" :: "g"(end));
''', '')],
    'pin_hdr': [('''			__asm__("" :: "a"(xb.hdr));
''', '')],
    'dead_add1': [('''	if (x > first + 0x4000)
		blocks += 2;
	memcpy(xb.hdr + off, src, len);''', '''	memcpy(xb.hdr + off, src, len);''')],
    'dead_add2': [('''		if (x > first + 0x4000)
			__asm__("");
''', '')],
    'dead_add3': [('''		if (x + 0x4000 < first)
			blocks++;
''', '')],
    'dead_add4': [('''		if ((len & 0x3fff) > 0x3fff)
			__asm__("");
''', '')],
    'dead_add5': [('''			if (x > first + 0x4000)
				blocks++;
''', '')],
    'dead_add6': [('''		if (x + 0x4000 < first)
			start++;
''', '')],
}
# edits that overlap: dead_c1 includes lab_c1
CONFLICT = {('lab_c1', 'dead_c1')}


def base():
    p = os.environ.get('IWBASE', iwlib.SRC)
    return open(p, newline='').read().replace('\r\n', '\n')


def apply(text, names):
    for n in names:
        if n == 'param':
            continue
        for a, b in T[n]:
            if a not in text:
                continue  # already gone from this base
            text = text.replace(a, b)
    return text


def flags_for(names):
    return [] if 'param' in names else ['--param', 'builtin-expect-probability=50']


def run(names, text=None):
    names = list(names)
    # apply bigger edits first so overlaps resolve
    order = sorted(names, key=lambda n: 0 if n == 'dead_c1' else 1)
    t = apply(text if text is not None else base(), order)
    return iwlib.score_text(t, flags_for(names))


ALL = [n for n in T if all(a in base() for a, b in T[n])] + ['param']


def many(combos, text=None, workers=4):
    with ThreadPoolExecutor(workers) as ex:
        return list(ex.map(lambda c: (c, run(c, text)), combos))


if __name__ == '__main__':
    cmd = sys.argv[1]
    if cmd == 'singles':
        for c, r in many([(n,) for n in ALL]):
            print(','.join(c), iwlib.fmt(r), flush=True)
    elif cmd == 'pairs':
        names = sys.argv[2:] or ALL
        res = many(list(itertools.combinations(names, 2)))
        res.sort(key=lambda x: x[1].get('total', 1e9))
        for c, r in res:
            print(','.join(c), iwlib.fmt(r))
    elif cmd == 'show':
        names = sys.argv[2].split(',') if sys.argv[2] != '-' else []
        r = run(names)
        print(iwlib.fmt(r))
        if '-o' in sys.argv:
            order = sorted(names, key=lambda n: 0 if n == 'dead_c1' else 1)
            open(sys.argv[sys.argv.index('-o') + 1], 'w', newline='\n').write(apply(base(), order))
    elif cmd == 'greedy':
        cur = []
        best = run(cur)
        print('start', iwlib.fmt(best), flush=True)
        while True:
            res = many([cur + [n] for n in ALL if n not in cur])
            res.sort(key=lambda x: x[1].get('total', 1e9))
            c, r = res[0]
            print(','.join(c), iwlib.fmt(r), flush=True)
            for c2, r2 in res[1:4]:
                print('   ', c2[-1], r2.get('total'), flush=True)
            if len(c) >= len(ALL):
                break
            cur = list(c)
