"""Attempt 3: the 16 tricks of the landed src/image_write.c (aac860d6) as named edits.

python tools/wip/dehint/iw3.py singles             every trick removed alone
python tools/wip/dehint/iw3.py subsets a,b,c,...   every subset of those names (sorted by lines, top 40)
python tools/wip/dehint/iw3.py show a,b,c [-o out.c] [-v [fn]]

IW3BASE=<file> picks another base (edits that don't apply there are skipped silently, so check with `show`).
`param` drops the --param."""
import itertools, os, sys
from concurrent.futures import ThreadPoolExecutor
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import iwlib

M = '		if (x + 0x4000 < first || (len & 0x3fff) > 0x3fff)\n			blocks++;\n'
T = {
    'a1': [('	if (x > first + 0x4000)\n		blocks += 2;\n', '')],
    'a2': [('		if (x > first + 0x4000)\n			__asm__("");\n', '')],
    'c34': [(M, '')],
    'c3': [(M, '		if ((len & 0x3fff) > 0x3fff)\n			blocks++;\n')],
    'c4': [(M, '		if (x + 0x4000 < first)\n			blocks++;\n')],
    'a5': [('			if (x > first + 0x4000)\n				blocks++;\n', '')],
    'a6': [('		if (x + 0x4000 < first)\n			start++;\n', '')],
    'len': [('	if ((len & 0x3fff) > 0x3fff)\n		len++;\n', '')],
    'ab': [('		if ((len & 0x3fff) > 0x3fff)\n			abort();\n', '')],
    'opt': [('__attribute__((optimize("no-tree-scev-cprop"))) void writeFsTable', 'void writeFsTable')],
    'xmalloc': [('void *xmalloc(size_t) __asm__("_malloc") __attribute__((malloc));\n', ''),
                ('xmalloc(xb.rawSize)', 'malloc(xb.rawSize)')],
    'pin_t': [('			__asm__("" :: "g"(t));\n', '')],
    'pin_hdr': [('			__asm__("" :: "a"(xb.hdr));\n', '')],
    'exp_file': [('if (__builtin_expect(lim >= off + len, 1)) {', 'if (lim >= off + len) {')],
    'exp_mob': [('if (__builtin_expect(imgFits(off, len), 1)) {', 'if (imgFits(off, len)) {')],
    'lnp2': [('''		else {
			/* imgAddFile's clone: keeps DOM2's threading from zeroing the npages guard edge */
			lnp2: __attribute__((hot));
		}
''', '')],
    # lnp2's plain-C near miss (73% via PRED_TREE_OPCODE_POSITIVE), 12 lines alone
    'lnp2le': [('''		if (!partial)
			npages = 32;
		else {
			/* imgAddFile's clone: keeps DOM2's threading from zeroing the npages guard edge */
			lnp2: __attribute__((hot));
		}
''', '''		if (partial <= 0)
			npages = 32;
''')],
    'param': [],
}
ORDER = {'c34': 0, 'c3': 1, 'c4': 2, 'lnp2le': 0}


def base():
    p = os.environ.get('IW3BASE', iwlib.SRC)
    return open(p, newline='').read().replace('\r\n', '\n')


def apply(text, names):
    for n in sorted(names, key=lambda n: ORDER.get(n, 5)):
        for a, b in T[n]:
            text = text.replace(a, b)
    return text


def flags_for(names):
    return [] if 'param' in names else ['--param', 'builtin-expect-probability=50']


def run(names, text=None):
    return iwlib.score_text(apply(text if text is not None else base(), names), flags_for(names))


def many(combos, workers=4):
    text = base()
    with ThreadPoolExecutor(workers) as ex:
        return list(ex.map(lambda c: (c, run(c, text)), combos))


if __name__ == '__main__':
    cmd = sys.argv[1]
    if cmd == 'singles':
        res = many([(n,) for n in T])
        for c, r in res:
            print(','.join(c), iwlib.fmt(r)[:220], flush=True)
    elif cmd == 'subsets':
        names = sys.argv[2].split(',')
        combos = [c for k in range(1, len(names) + 1) for c in itertools.combinations(names, k)]
        print(len(combos), 'subsets', flush=True)
        res = many(combos)
        res.sort(key=lambda x: x[1].get('total', 1e9) if not x[1].get('identical') else -1)
        for c, r in res[:40]:
            print(','.join(c), iwlib.fmt(r)[:200])
        for c, r in res:
            if r.get('identical'):
                print('IDENTICAL', ','.join(c))
    elif cmd == 'show':
        names = sys.argv[2].split(',') if sys.argv[2] != '-' else []
        t = apply(base(), names)
        print(iwlib.fmt(iwlib.score_text(t, flags_for(names))))
        if '-o' in sys.argv:
            open(sys.argv[sys.argv.index('-o') + 1], 'w', newline='\n').write(t)
