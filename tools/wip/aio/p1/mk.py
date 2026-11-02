"""mk.py OUT [edit[=arg]...]: from n8c.c, apply named edits (see the ED table)."""
import re, sys
HERE = __file__.replace('mk.py', '')
t = open(HERE + 'n8c.c', newline='').read()
i = t.index('_Bool optIniBool(')
j = t.index('int optIniInt(')
OB = t[i:j]
B = '\t'
N = '\n'
CP = '__builtin_constant_p'
ED = {}


def ed(f):
    ED[f.__name__] = f
    return f


def copyopt(name, edit):
    return edit(OB.replace('_Bool optIniBool(', 'static _Bool %s(' % name))


@ed
def noecdg(t):
    "noecdremap: own copy, bad expected, one dead exit (P 115, G 10)"
    c = copyopt('optN', lambda b: b.replace('if (!bad) {', 'if (__builtin_expect(!bad, 0)) {').replace(
        B + 'if (xb.bootFlags & set) {',
        B + 'if (__builtin_expect(%s(xb.bootFlags + 2), 0)) return 0;' % CP + N + B + 'if (xb.bootFlags & set) {'))
    k = t.index('int optIniInt(')
    t = t[:k] + c + t[k:]
    return t.replace('OPT("noecdremap", 0x80000000, 0);', 'if (!(xb.bootFlags & 0x80000000)) optN("noecdremap", 0x80000000, 0, 0);')


F41 = ('if (%s(xb.xellButton + 1)) { if (%s(xb.xellButton + 2)) goto z; if (%s(xb.xellButton + 3)) goto z; }' % (CP, CP, CP))


@ed
def xb1(t, feed=None):
    "xellbutton: parseButton copy with dead feeds into the !s path"
    feed = feed or F41
    c = '''static int parseButtonX(const char *s)
{
	int b = 0;

	if (!s) {
z:
		return 0;
	}
	if (__builtin_expect(!strnicmp(s, "power", 5), 1)) {
		b = 0x11;
		DXF
bx: ;
	} else {
		__asm__ goto ("" :::: dxc);
		FEED
		if (!strnicmp(s, "remopower", 9))
			b = 0x20;
		else if (!strnicmp(s, "remox", 5))
			b = 0x22;
		else if (__builtin_expect(!strnicmp(s, "winbutton", 9), 1))
			b = 0x24;
		else
			b = parseButtonPart(s);
	}
	return b;
dxc: __attribute__((cold));
	goto dx;
dx:
	__asm__ volatile ("" :: "i"(3));
	b = 0x11;
	if (__builtin_constant_p(xb.xellButton + 6))
		goto bx;
	__builtin_unreachable();
}

'''.replace('FEED', feed).replace('DXF', 'if (__builtin_expect(__builtin_constant_p(xb.xellButton + 5), 1)) goto dx;')
    k = t.index('int parseButton(')
    t = t[:k] + c + t[k:]
    return t.replace('parseButton(getIniValue("xellbutton"))', 'parseButtonX(getIniValue("xellbutton"))')


@ed
def old2(t, head=None):
    "olddvd: copy with a dead feed into S (branch edge of the label after olddvd) and I at 38"
    head = head or ('if (__builtin_expect(%s(xb.bootFlags + 7), 0)) goto r; if (%s(xb.bootFlags + 8) && %s(xb.bootFlags + 9)) goto r;' % (CP, CP, CP))
    a = OB.index(B + 'if (xb.bootFlags & set) {')
    b = OB.index(B + 'if (perboxExists(name)) {')
    c = OB[:a] + B + head + N + B + 'if ((xb.bootFlags & set) || (xb.bootFlagsOff & set))' + N + B + B + 'return 0;' + N + OB[b:]
    c = c.replace('_Bool optIniBool(', 'static _Bool optO(')
    k = t.index('int optIniInt(')
    t = t[:k] + c + t[k:]
    return t.replace('OPT("olddvd", 0, 4);', 'if (!(xb.bootFlags & 0)) optO("olddvd", 0, 4, 0);')


@ed
def gl(t, spec):
    "gl=name:copy,...: the option uses a copy of optIniBool with bad expected (G lower)"
    for it in spec.split(','):
        nm_, c_ = it.split(':')
        c = copyopt(c_, lambda b: b.replace('if (!bad) {', 'if (__builtin_expect(!bad, 0)) {'))
        k = t.index('int optIniInt(')
        t = t[:k] + c + t[k:]
        m = re.search(r'OPT\("%s", (\w+), (\w+)\);' % nm_, t)
        t = t.replace(m.group(0), 'if (!(xb.bootFlags & (%s))) %s("%s", %s, %s, 0);' % (m.group(1), c_, nm_, m.group(1), m.group(2)))
    return t


@ed
def dzm(t, feed=None):
    "dummy in the macid chars warning trace, keyed from the block after sprintf (its flow only reaches the return)"
    feed = feed or ('if (__builtin_expect(%s(xb.blSuffix[1] + 1), 0)) { if (%s(xb.blSuffix[1] + 2)) { if (__builtin_expect(%s(xb.blSuffix[1] + 4), 1)) goto dz1; } }' % (CP, CP, CP))
    a = B * 4 + 'log_printf(0, "***** WARNING: invalid characters in macid \'");'
    assert a in t
    t = t.replace(a, B * 4 + '__builtin_memset(s, 0, __builtin_constant_p(xb.macid[1] + 9));' + N + B * 4 + '__asm__ goto ("" :::: dzc1);' + N + a)
    b = B * 3 + 'sprintf(xb.blSuffix, "_%s", s);'
    assert b in t
    t = t.replace(b, B * 2 + 'if (s) {' + N + b + N + B * 3 + feed + N + 'b1: ;' + N + B * 2 + '}').replace(B * 2 + 'if (s)' + N + B * 2 + 'if (s) {', B * 2 + 'if (s) {')
    k = t.index('void applyIniOptions(void)')
    e = t.index(N + '}' + N, k)
    return t[:e] + N + B + 'if (0) { dzc1: __attribute__((cold)); goto dz1; dz1: __asm__ volatile ("" :: "i"(1)); if (__builtin_constant_p(xb.blSuffix[1] + 3)) goto b1; __builtin_unreachable(); }' + t[e:]


@ed
def xb2(t, feed=None):
    "xellbutton2: parseButton copy with a dummy at the end of the cold chain; flow returns from dz"
    feed = feed or ('if (%s(xb.xellAltButton + 1) && %s(xb.xellAltButton + 2)) goto dz; back:' % (CP, CP))
    i = t.index('int parseButton(')
    j = t.index(N + '}' + N, i) + 3
    c = t[i:j].replace('int parseButton(', 'static int parseButtonY(')
    c = c.replace('b = parseButtonPart(s);', '{ b = parseButtonPart(s); __asm__ goto ("" :::: dz); }')
    c = c.replace(B + 'return b;', B + 'return b;' + N + 'dz:' + N + B + '__asm__ volatile ("" :: "i"(2));' + N + B + 'if (%s(xb.xellAltButton + 3)) goto back;' % CP + N + B + '__builtin_unreachable();')
    c = c.replace('if (!strnicmp(s, "power", 5))', 'if (__builtin_expect(!strnicmp(s, "power", 5), 1))').replace('b = 0x11;', '{ b = 0x11; ' + feed + ' ; }')
    t = t[:j] + N + c + t[j:]
    return t.replace('parseButton(getIniValue("xellbutton2"))', 'parseButtonY(getIniValue("xellbutton2"))')


@ed
def dzd(t, feed=None):
    "dummy at the end of the dualboot chain, keyed from the block after sprintf"
    feed = feed or ('if (__builtin_expect(%s(xb.blSuffix[1] + 5), 0)) { if (%s(xb.blSuffix[1] + 6)) { if (%s(xb.blSuffix[1] + 7)) { if (__builtin_expect(%s(xb.blSuffix[1] + 8), 1)) goto dz2; } } }' % (CP, CP, CP, CP))
    a = B * 4 + 'xb.dualButton = 0;'
    assert a in t
    t = t.replace(a, B * 4 + '__asm__ goto ("" :::: dzc2);' + N + a)
    assert 'b1: ;' in t
    t = t.replace('b1: ;', 'b1: ;' + N + B * 3 + feed + N + 'b2: ;')
    k = t.index('void applyIniOptions(void)')
    e = t.index(N + '}' + N, k)
    return t[:e] + N + B + 'if (0) { dzc2: __attribute__((cold)); goto dz2; dz2: __asm__ volatile ("" :: "i"(4)); if (__builtin_constant_p(xb.blSuffix[1] + 9)) goto b2; __builtin_unreachable(); }' + t[e:]


out = sys.argv[1]
for e in sys.argv[2:]:
    n, _, a = e.partition('=')
    t = ED[n](t, a) if a else ED[n](t)
open(out, 'w', newline='\n').write(t)
