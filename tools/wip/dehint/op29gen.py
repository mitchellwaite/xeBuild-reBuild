"""Attempt 29: parseButtonX bodies with up to MAXCP (default 3) dead __builtin_constant_p tests
in four slots: E (function entry), B (between `!s` and the power test), D (power's success arm),
L (head of the else arm; CF=1 puts remopower's strnicmp call ahead of it).  Atoms: one test
`if (T) goto X;`, nested `if (T1) { if (T2) goto X; }`, split `if (T1) { if (T2) goto X; goto Y; }`;
T is cp, cp > 0, cp < 0 or cp == 1; targets z (return 0), el (else arm), j (b = 0x11).
Defines V = {name: body}; used by op29fast.py (model search) and op29run.py (real compile)."""
import itertools, os
TF = {'p': '%s', 'g': '%s > 0', 'l': '%s < 0', 'e': '%s == 1'}
SLOT_T = {'E': ('z', 'el', 'j'), 'B': ('z', 'el', 'j'), 'D': ('z', 'el'), 'L': ('z', 'j')}
CF = int(os.environ.get('CF', '1'))

def atoms1(k):
    return [('1%s%s' % (f, x), 1, 'if (%s) goto %s;' % (TF[f], x)) for f in TF for x in SLOT_T[k]]

def atoms2(k):
    A = []
    ts = SLOT_T[k]
    for f1 in TF:
        for f2 in TF:
            for x in ts:
                A.append(('2%s%s%s' % (f1, f2, x), 2, 'if (%s) { if (%s) goto %s; }' % (TF[f1], TF[f2], x)))
            for x, y in itertools.permutations(ts, 2):
                A.append(('s%s%s%s%s' % (f1, f2, x, y), 2, 'if (%s) { if (%s) goto %s; goto %s; }' % (TF[f1], TF[f2], x, y)))
    return A

def body(sl, cf):
    n = [0]
    def fill(k):
        out = []
        for a in sl.get(k, ()):
            t = a[2]
            while '%s' in t:
                n[0] += 1
                t = t.replace('%s', '__builtin_constant_p(xb.xellButton + %d)' % n[0], 1)
            out.append(t)
        return ' '.join(out)
    E, B, S, D, L = (fill(k) for k in 'EBSDL')
    if cf:
        head = 'int r;\nel:\n\t\tr = strnicmp(s, "remopower", 9);\n\t\t%s\n\t\tif (!r)' % L
    else:
        head = '\nel:\n\t\t%s\n\t\tif (!strnicmp(s, "remopower", 9))' % L
    return '''
	int b = 0;

	%s
	if (!s) {
		%s
z:
		return 0;
	}
	%s
	if (!strnicmp(s, "power", 5)) {
j:
		b = 0x11;
		%s
	} else {
		%s
			b = 0x20;
		else if (!strnicmp(s, "remox", 5))
			b = 0x22;
		else if (!strnicmp(s, "winbutton", 9))
			b = 0x24;
		else
			b = parseButtonPart(s, 0);
	}
	return b;
''' % (E, S, B, D, head)

ONE = [(k, a) for k in SLOT_T for a in atoms1(k)]
TWO = [(k, a) for k in SLOT_T for a in atoms2(k)]
V = {}
def add(items):
    sl = {}
    for k, a in items:
        sl.setdefault(k, []).append(a)
    name = 'c%d_' % CF + '_'.join(k + a[0] for k, a in items)
    V[name] = body(sl, CF)
MAXCP = int(os.environ.get('MAXCP', '3'))
for r in (1, 2, 3):
    if r > MAXCP:
        break
    for items in itertools.permutations(ONE, r):
        # canonical: slots in order E,B,S,D,L; order within the same slot free
        ks = ['EBSDL'.index(k) for k, a in items]
        if ks != sorted(ks):
            continue
        add(items)
for t in TWO:
    add([t])
    if MAXCP >= 3:
        for o in ONE:
            for items in ([t, o], [o, t]):
                ks = ['EBSDL'.index(k) for k, a in items]
                if ks != sorted(ks):
                    continue
                if ks[0] == ks[1] and items[0] is o:
                    add(items)
                elif ks[0] != ks[1] or items[0] is t:
                    add(items)

