"""build's tricks as named source edits.  Importable; also a CLI:

python tools/wip/dehint/bdtricks.py singles            every trick removed alone
python tools/wip/dehint/bdtricks.py pairs [names..]    every pair (of names, default all)
python tools/wip/dehint/bdtricks.py greedy [names..]   greedy: take every removal that stays IDENTICAL
python tools/wip/dehint/bdtricks.py show a,b,c [-o out.c] [-v fn]  score that combination
Base text: src/build.c, or BDBASE=<file>.  Names whose text isn't in the base are skipped.
BDFLAGS="" compiles plain -O3 (default: build.sh's param)."""
import itertools, os, sys
from concurrent.futures import ThreadPoolExecutor
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bdlib

EXP_CRC = '__builtin_expect(crc != c, 0)'


def crc(case):
    """the crc expect of checkBl's `case N:` arm"""
    def f(text):
        i = text.find('\tcase %d:\n' % case, text.find('int checkBl('))
        if i < 0:
            return None
        j = text.find('c = crc32(bl, blsize);\n', i)
        k = text.find('if (', j)
        if not text.startswith('if (' + EXP_CRC + ')', k):
            return None
        return text[:k] + 'if (crc != c)' + text[k + 4 + len(EXP_CRC) + 1:]
    return f


T = {
    # --- loadFileCrc
    'exp_verbose': [('if (__builtin_expect(verbose, 1)) {', 'if (verbose) {')],
    'pin_e': [('''			__asm__("" : : "S"(e));
''', '')],
    # --- loadInputFile
    'noclone': [('''__attribute__((noclone))
int loadInputFile''', 'int loadInputFile')],
    # --- patchSmcConfig
    'nei_smc': [('''__attribute__((optimize("no-early-inlining")))
uint32_t patchSmcConfig''', 'uint32_t patchSmcConfig')],
    'cb1': [('''			cb_hint(&dead);
			smc[0x11] = xb.cpuFan | 0x80;''', '''			smc[0x11] = xb.cpuFan | 0x80;''')],
    'cb2': [('''			cb_hint(&dead);
			smc[0x11] = 0x7f;''', '''			smc[0x11] = 0x7f;''')],
    'cb3': [('''			cb_hint(&dead);
			smc[0x12] = xb.gpuFan | 0x80;''', '''			smc[0x12] = xb.gpuFan | 0x80;''')],
    'cb4': [('''			cb_hint(&dead);
			smc[0x12] = 0x7f;''', '''			smc[0x12] = 0x7f;''')],
    # --- extractSmcConfig
    'noinline': [('__attribute__((noinline)) int extractSmcConfig', 'int extractSmcConfig')],
    'addr_size': [('''	(void)&size;
''', '')],
    'exp_200': [('__builtin_expect(i + 0x200 <= size, 1)', 'i + 0x200 <= size')],
    'pin_i': [('''		__asm__("" : : "S"(i + 0x200), "D"(buf));
''', '')],
    'exp_210': [('__builtin_expect(i + 0x210 <= size, 1)', 'i + 0x210 <= size')],
    'exp_400': [('__builtin_expect(size - i >= 0x400, 1)', 'size - i >= 0x400')],
    'pin_src': [('''			__asm__("" : "+r"(src) : "r"(buf));
''', '')],
    'lab_nf1': [('''notfound: __attribute__((hot));
''', '''notfound:
''')],
    'lab_nf2': [('''notfound2: __attribute__((hot));
''', '')],
    # --- checkBl
    'nei_chk': [('''__attribute__((optimize("no-early-inlining")))
int checkBl''', 'int checkBl')],
    'pin_type': [('''	__asm__("" : : "D"(type));
''', '')],
    'lit_chk': [('''	__asm__("" :: "i"("\\n\\n***** ERROR: BL crc check failed! calculated: %08x expected: %08x\\n"));
''', '')],
    'lab_size': [('''toobig: __attribute__((hot));
''', '''toobig:
''')],
    'cb5': [('''	cb_hint(&dead);
	m = bl[0];''', '''	m = bl[0];''')],
    'pin_m': [('''	__asm__("" :: "a"(m));
''', '')],
    'crc5': [crc(5)], 'crc7': [crc(7)], 'crc8': [crc(8)], 'crc9': [crc(9)], 'crc10': [crc(10)],
    'crc12': [crc(12)], 'crc13': [crc(13)],
    # --- loadBl60, loadBl
    'pin_p60': [('''		uint8_t *p = e->data;

		__asm__("" : "+r"(p));
''', '''		uint8_t *p = e->data;

''')],
    'aa_60': [('''		e->size = 0x60;
		memcpy(__builtin_assume_aligned(p, 4), defBl60, 0x60);''', '''		e->size = 0x60;
		memcpy(p, defBl60, 0x60);''')],
    'exp_t10': [('__builtin_expect(type == 10, 0)', 'type == 10')],
    'lab_t5le': [('''		t5le: __attribute__((hot));
''', '')],
    'exp_pr': [('if (__builtin_expect(*pr != 0, 0))', 'if (*pr != 0)')],
    'lab_badsize': [('''		badsize: __attribute__((hot));
''', '')],
    'exp_27': [('__builtin_expect(type == 27, 1) && loadBaseFile', 'type == 27 && loadBaseFile')],
    'pin_d': [('''			__asm__("" : "+a"(d));
''', '')],
    'vol_fail': [('''	__asm__ __volatile__("");
''', '')],
    # --- loadConsoleBl
    'exp_t9': [('if (__builtin_expect(type == 9, 0)) {', 'if (type == 9) {')],
    'pin_p': [('''					__asm__("" : "+r"(p));
''', '')],
    'aa_p': [('''					e->size = 0x60;
					memcpy(__builtin_assume_aligned(p, 4), defBl60, 0x60);''', '''					e->size = 0x60;
					memcpy(p, defBl60, 0x60);''')],
    'exp_t2': [('''				if (__builtin_expect(type != 2, 0))
					break;
''', '')],
    'lab_none': [('''none: __attribute__((cold));
''', '''none:
''')],
    # --- the rest
    'nei_blmod': [('''__attribute__((optimize("no-early-inlining")))
void patchBlsBlmod''', 'void patchBlsBlmod')],
    'exp_t24': [('type == 25 && __builtin_expect(type != 24, 1) && e->offset', 'type == 25 && e->offset')],
    'exp_upd': [('__builtin_expect(type == 23 || type == 15, 0) || type == 16', 'type == 23 || type == 15 || type == 16')],
    'pin_size': [('''		__asm__("" : "+b"(size));
''', '')],
    'exp_devgl': [('__builtin_expect(xb.type == BUILD_DEVGL || xb.type == BUILD_DEVGL16, 0)', 'xb.type == BUILD_DEVGL || xb.type == BUILD_DEVGL16')],
}


def base():
    return bdlib.read_src(os.environ.get('BDBASE') or bdlib.SRC)


def flags():
    v = os.environ.get('BDFLAGS')
    return bdlib.P98 if v is None else v.split()


def apply(text, names):
    """apply the named edits, leaving out those whose text is gone; (text, applied)"""
    got = []
    for n in names:
        for e in T[n]:
            if callable(e):
                t2 = e(text)
                if t2 is None:
                    break
                text = t2
            else:
                if e[0] not in text:
                    break
                text = text.replace(e[0], e[1])
        else:
            got.append(n)
    return text, got


def active(text):
    return [n for n in T if apply(text, [n])[1]]


def score(names, b=None):
    t, _ = apply(b if b is not None else base(), names)
    return bdlib.score_text(t, flags())


def pool():
    return ThreadPoolExecutor(max(2, (os.cpu_count() or 4) - 1))


def main():
    a = sys.argv[1:]
    cmd = a.pop(0)
    b = base()
    if cmd == 'singles':
        names = a or active(b)
        with pool() as p:
            rs = list(p.map(lambda n: (n, score([n], b)), names))
        rs.sort(key=lambda x: (x[1].get('total', 10**9), x[1].get('identical') is not True))
        for n, r in rs:
            print('%-12s %s' % (n, bdlib.fmt(r)))
    elif cmd == 'pairs':
        names = a or active(b)
        with pool() as p:
            rs = list(p.map(lambda c: (c, score(list(c), b)), itertools.combinations(names, 2)))
        rs.sort(key=lambda x: x[1].get('total', 10**9))
        for c, r in rs:
            print('%-24s %s' % ('+'.join(c), bdlib.fmt(r)))
    elif cmd == 'greedy':
        names = a or active(b)
        cur = []
        progress = True
        while progress:
            progress = False
            todo = [n for n in names if n not in cur]
            with pool() as p:
                rs = list(p.map(lambda n: (n, score(cur + [n], b)), todo))
            for n, r in rs:
                if r.get('identical') and not progress:
                    pass
            free = [n for n, r in rs if r.get('identical')]
            for n in free:
                r = score(cur + [n], b)
                if r.get('identical'):
                    cur.append(n)
                    progress = True
                    print('took', n, flush=True)
        print('free:', ','.join(cur))
    elif cmd == 'show':
        names = a.pop(0).split(',')
        o = None
        if '-o' in a:
            i = a.index('-o')
            o = a[i + 1]
            del a[i:i + 2]
        t, got = apply(b, names)
        print('applied', got, 'skipped', [n for n in names if n not in got])
        if o:
            open(o, 'w', newline='\n').write(t)
        print(bdlib.fmt(bdlib.score_text(t, flags())))
    else:
        print(__doc__)


if __name__ == '__main__':
    main()
