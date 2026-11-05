"""options' tricks as named source edits.  Importable; also a CLI:

python tools/wip/dehint/optricks.py singles [names..]        every trick removed alone
python tools/wip/dehint/optricks.py pairs [names..]          every pair (of names, default all)
python tools/wip/dehint/optricks.py greedy [names..]         take every removal that stays IDENTICAL
python tools/wip/dehint/optricks.py show a,b,c [-o out.c] [-v [fn]]   score that combination
Base text: src/options.c, or OPBASE=<file>.  Names whose text isn't in the base are skipped.
The pseudo-edit `param` compiles without build.sh's --param (plain -O3).
parseOption's tricks (po_*) and applyIniOptions' (the rest) barely interact: `greedy po`
or `greedy aio` restricts to one group."""
import itertools, os, sys
from concurrent.futures import ThreadPoolExecutor
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import optlib


def F(hdr, old, new):
    """replace old by new inside the function whose definition starts with hdr"""
    def f(text):
        i = text.find(hdr)
        if i < 0:
            return None
        j = text.find('\n}\n', i)
        body = text[i:j]
        if old not in body:
            return None
        return text[:i] + body.replace(old, new, 1) + text[j:]
    return f


ARM_ON = '''	if (xb.bootFlags & set) {
		if (__builtin_constant_p(xb.bootFlags + 1))
			goto r;
		return 0;
	}
'''
ARM_ON_P = '''	if (xb.bootFlags & set)
		return 0;
'''
ARM_OFF = '''	if (xb.bootFlagsOff & set) {
		if (__builtin_constant_p(xb.bootFlagsOff + 1))
			goto r;
		return 0;
	}
'''
ARM_OFF_P = '''	if (xb.bootFlagsOff & set)
		return 0;
'''
EXP_BAD = 'if (__builtin_expect(!bad, 0)) {'

HDR = {'ib': '_Bool optIniBool(', 'N': 'static _Bool optN(', 'E': 'static _Bool optE(',
       'C': 'static _Bool optC(', 'S': 'static _Bool optS(', 'U': 'static _Bool optU('}

T = {}
for k, h in HDR.items():
    T[k + '_cp1'] = [F(h, ARM_ON, ARM_ON_P)]
    T[k + '_cp2'] = [F(h, ARM_OFF, ARM_OFF_P)]
    if k != 'ib':
        T[k + '_exp'] = [F(h, EXP_BAD, 'if (!bad) {')]

T.update({
    'N_entry': [('	if (__builtin_expect(__builtin_constant_p(xb.bootFlags + 2), 0)) return 0;\n', '')],
    'O_e1': [('	if (__builtin_expect(__builtin_constant_p(xb.bootFlags + 7), 0)) goto r; ', '	')],
    'O_e2': [('if (__builtin_constant_p(xb.bootFlags + 8) && __builtin_constant_p(xb.bootFlags + 9)) goto r;', '')],
    # the copies replaced by optIniBool calls (the copy is then unused)
    'm_N': [('if (!(xb.bootFlags & 0x80000000)) optN("noecdremap", 0x80000000, 0, 0);', 'OPT("noecdremap", 0x80000000, 0);')],
    'm_U': [('if (!(xb.bootFlags & (0x10000000))) optU("nandmu", 0x10000000, 0, 0);', 'OPT("nandmu", 0x10000000, 0);')],
    'm_S': [('if (!(xb.bootFlags & (0x4000000))) optS("nosecurity", 0x4000000, 0, 0);', 'OPT("nosecurity", 0x4000000, 0);')],
    'm_C': [('if (!(xb.bootFlags & (1))) optC("cygnos", 1, 0, 0);', 'OPT("cygnos", 1, 0);')],
    'm_E': [('if (!(xb.bootFlags & (0x400000))) optE("smcnoeject", 0x400000, 0, 0);', 'OPT("smcnoeject", 0x400000, 0);')],
    'm_O': [('if (!(xb.bootFlags & 0)) optO("olddvd", 0, 4, 0);', 'OPT("olddvd", 0, 4);')],
    # parseButton
    'm_bx': [('xb.xellButton = parseButtonX(getIniValue("xellbutton"));', 'xb.xellButton = parseButton(getIniValue("xellbutton"));')],
    'bx_exp': [F('static int parseButtonX(', 'if (__builtin_expect(!strnicmp(s, "power", 5), 1)) {', 'if (!strnicmp(s, "power", 5)) {')],
    'pb_exp': [('else if (__builtin_expect(!strnicmp(s, "winbutton", 9), 1))', 'else if (!strnicmp(s, "winbutton", 9))')],
    # optIniIntI
    'ii_attr': [('static inline __attribute__((always_inline)) int optIniIntI', 'static inline int optIniIntI')],
    'm_ii': [('xb.cfLdv = optIniIntI(', 'xb.cfLdv = optIniInt('), ('= optIniIntI(', '= optIniInt(')],
    # macid
    'lit_mac': [('''			/* the original's .rdata has these before the length error (its
			   tests were likely the other way round) */
			__asm__("" :: "i"("***** WARNING: invalid characters in macid '"), "i"("' provided in ini file! Discarding!\\n"));
''', '')],
    'mac_ms': [('				__builtin_memset(s, 0, __builtin_constant_p(xb.macid[1] + 9));\n', '')],
    'mac_goto': [('				__asm__ goto ("" :::: dzc1);\n', '')],
    'mac_bar': [('''				/* keeps if-conversion from hoisting i = 0 above the test */
				__asm__("");
''', '')],
    'dual_goto': [('				__asm__ goto ("" :::: dzc2);\n', '')],
    'rev1': [('''			if (__builtin_expect(__builtin_constant_p(xb.blSuffix[1] + 1), 0)) { if (__builtin_constant_p(xb.blSuffix[1] + 2)) { if (__builtin_expect(__builtin_constant_p(xb.blSuffix[1] + 4), 1)) goto dz1; } }
b1: ;
''', '')],
    'rev2': [('''			if (__builtin_expect(__builtin_constant_p(xb.blSuffix[1] + 15), 0)) { if (__builtin_constant_p(xb.blSuffix[1] + 16)) { if (__builtin_constant_p(xb.blSuffix[1] + 17)) { if (__builtin_constant_p(xb.blSuffix[1] + 18)) { if (__builtin_expect(__builtin_constant_p(xb.blSuffix[1] + 19), 1)) goto dz2; } } } }
b2: ;
''', '')],
    'dz1blk': [('	if (0) { dzc1: ; goto dz1; dz1: __asm__ volatile ("" :: "i"(1));  __builtin_unreachable(); }\n', '')],
    'dz2blk': [('	if (0) { dzc2: ; goto dz2; dz2: __asm__ volatile ("" :: "i"(4));  __builtin_unreachable(); }\n', '')],
    # parseOption
    'po1': [('''			if (xb.cpuTemp == -1) {
				po_hint(&dead);
				goto bad;
			}
''', '''			if (xb.cpuTemp == -1)
				goto bad;
''')],
    'po2': [('''			if (xb.gpuFan == -1) {
				po_hint(&dead);
				goto bad;
			}
''', '''			if (xb.gpuFan == -1)
				goto bad;
''')],
    'po_nei': [('__attribute__((optimize("no-early-inlining")))\nuint32_t parseOption', 'uint32_t parseOption')],
    'po_exp1': [('if (__builtin_expect(setBoolOption(opt, val) == 1, 0)) {', 'if (setBoolOption(opt, val) == 1) {')],
    'po_exp2': [('if (__builtin_expect(vlen, 0)) {', 'if (vlen) {')],
    'po_int': [('''uint32_t parseOption(char *opt);
/* parseCmdOptions matches only when it sees an int return */
int parseOptionInt(char *opt) __asm__("_parseOption");
''', 'int parseOption(char *opt);\n'), ('uint32_t parseOption(char *opt)\n{', 'int parseOption(char *opt)\n{'),
               ('if (!parseOptionInt(opt))', 'if (!parseOption(opt))')],
    'po_int2': [('''uint32_t parseOption(char *opt);
/* parseCmdOptions matches only when it sees an int return */
int parseOptionInt(char *opt) __asm__("_parseOption");
''', 'uint32_t parseOption(char *opt);\n'), ('if (!parseOptionInt(opt))', 'if (!parseOption(opt))')],
    'param': [],
})

# parseButtonPart folded back into parseButton (needs m_bx: parseButtonX calls it)
PART_DEF_START = '/* parseButton after its first four names'
PART_DEF_END = 'int baseFileExists('
PART_BODY = '''	else if (!strnicmp(s, "wirelessx", 9))
		b = 0x55;
	else if (!strnicmp(s, "wiredx", 6)) {
		if (!strnicmp(s, "wiredxb1", 8))
			b = 0x59;
		else if (!strnicmp(s, "wiredxb2", 8))
			b = 0x58;
		else if (!strnicmp(s, "wiredxb3", 8))
			b = 0x5a;
		else if (!strnicmp(s, "wiredxf1", 8))
			b = 0x56;
		else if (!strnicmp(s, "wiredxf2", 8))
			b = 0x57;
		else
			b = 0x5a;
	} else if (!strnicmp(s, "eject", 5))
		b = 0x12;
	else if (!strnicmp(s, "kiosk", 5))
		b = 0x41;
'''


def part(text):
    i = text.find(PART_DEF_START)
    j = text.find(PART_DEF_END)
    if i < 0 or j < 0:
        return None
    text = text[:i] + text[j:]
    old = '''	else
		b = parseButtonPart(s);
	return b;
}
'''
    k = text.find('int parseButton(const char *s)')
    m = text.find(old, k)
    if k < 0 or m < 0:
        return None
    return text[:m] + PART_BODY + '	return b;\n}\n' + text[m + len(old):]


T['part'] = [part]

GROUPS = {
    'po': [n for n in T if n.startswith('po')],
}
GROUPS['aio'] = [n for n in T if n not in GROUPS['po'] and n != 'param']


def base():
    return optlib.read_src(os.environ.get('OPBASE') or optlib.SRC)


def apply(text, names):
    got = []
    for n in names:
        t = text
        ok = True
        for e in T[n]:
            if callable(e):
                t2 = e(t)
                if t2 is None:
                    ok = False
                    break
                t = t2
            else:
                if e[0] not in t:
                    ok = False
                    break
                t = t.replace(e[0], e[1])
        if ok:
            text = t
            got.append(n)
    return text, got


def active(text):
    return [n for n in T if apply(text, [n])[1]]


def flags_for(names):
    return [] if 'param' in names else optlib.P83


def score(names, b=None):
    t, _ = apply(b if b is not None else base(), names)
    return optlib.score_text(t, flags_for(names))


def pool():
    return ThreadPoolExecutor(max(2, (os.cpu_count() or 4) - 1))


def expand(a):
    out = []
    for x in a:
        out += GROUPS.get(x, [x])
    return out


def main():
    a = sys.argv[1:]
    cmd = a.pop(0)
    b = base()
    if cmd == 'singles':
        names = expand(a) or active(b)
        with pool() as p:
            rs = list(p.map(lambda n: (n, score([n], b)), names))
        rs.sort(key=lambda x: (x[1].get('total', 10**9), x[1].get('identical') is not True))
        for n, r in rs:
            print('%-12s %s' % (n, optlib.fmt(r)), flush=True)
    elif cmd == 'pairs':
        names = expand(a) or active(b)
        with pool() as p:
            rs = list(p.map(lambda c: (c, score(list(c), b)), itertools.combinations(names, 2)))
        rs.sort(key=lambda x: x[1].get('total', 10**9))
        for c, r in rs:
            print('%-24s %s' % ('+'.join(c), optlib.fmt(r)))
    elif cmd == 'greedy':
        names = expand(a) or active(b)
        cur = []
        progress = True
        while progress:
            progress = False
            todo = [n for n in names if n not in cur]
            with pool() as p:
                rs = list(p.map(lambda n: (n, score(cur + [n], b)), todo))
            for n in [n for n, r in rs if r.get('identical')]:
                if score(cur + [n], b).get('identical'):
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
        if '-v' in a:
            i = a.index('-v')
            optlib.vdiff(t, flags_for(names), a[i + 1] if i + 1 < len(a) else None)
        else:
            print(optlib.fmt(optlib.score_text(t, flags_for(names))))
    else:
        print(__doc__)


if __name__ == '__main__':
    main()
