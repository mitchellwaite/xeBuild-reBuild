"""Attempt 14: macid's two warnings with ONE copy of their common tail in the source (the
reference crossjumps the two tails into one: `mov $LC129,4(%esp)` falls into L670 and the
chars warning jumps there), i.e. a PHI of the message pointer whose edge copies are the
two `movl $LCx, 4(%esp)`.  Crossed with the dz removals.

python tools/wip/dehint/op14mac.py [variants..]   (RMS=none,ag1,dz1,dzall)"""
import os, sys
from concurrent.futures import ThreadPoolExecutor
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import optlib
import op13

RM = dict(op13.RM)
RM['none'] = []
MS = op13.MS
AG1 = op13.AG1
CH = '"***** WARNING: invalid characters in macid \'"'
LN = '"***** WARNING: invalid length macid \'"'
TAIL = '"\' provided in ini file! Discarding!\\n"'
LOOP = '''					for (i = 0; i < 6; i++) {
						xb.macid[i] = myatox8(s);
						s += 2;
					}
'''
OLD = '''			if (strlen(s) == 12) {
				if (validateString(s)) {
''' + LOOP + '''				} else {
''' + MS + AG1 + '''					log_printf(0, ''' + CH + ''');
					showHexPairs(0, s);
					log_printf(0, ''' + TAIL + ''', s);
				}
			} else {
				log_printf(0, ''' + LN + ''');
				showHexPairs(0, s);
				log_printf(0, ''' + TAIL + ''', s);
			}
'''


def tail(ind, arg=', s'):
    return (ind + 'log_printf(0, msg);\n' + ind + 'showHexPairs(0, s);\n' +
            ind + 'log_printf(0, ' + TAIL + arg + ');\n')


V = {}
# a: msg = NULL flag, nested tests as now, tail under if (msg)
V['flag'] = '''			msg = NULL;
			if (strlen(s) == 12) {
				if (validateString(s)) {
''' + LOOP + '''				} else {
''' + MS + AG1 + '''					msg = ''' + CH + ''';
				}
			} else
				msg = ''' + LN + ''';
			if (msg) {
''' + tail('\t\t\t\t') + '''			}
'''
# b: goto past the tail after the loop
V['goto'] = '''			if (strlen(s) == 12) {
				if (validateString(s)) {
''' + LOOP + '''					goto macok;
				}
''' + MS.replace('\t\t\t\t\t', '\t\t\t\t\t') + AG1 + '''				msg = ''' + CH + ''';
			} else
				msg = ''' + LN + ''';
''' + tail('\t\t\t') + '''		macok:;
'''
# c: length test first as the bad arm, else-if chars, else loop
V['elif'] = '''			msg = NULL;
			if (strlen(s) != 12)
				msg = ''' + LN + ''';
			else if (!validateString(s)) {
''' + MS + AG1 + '''				msg = ''' + CH + ''';
			} else {
''' + LOOP.replace('\t\t\t\t\t', '\t\t\t\t') + '''			}
			if (msg) {
''' + tail('\t\t\t\t') + '''			}
'''
# d: the tail first under if (msg), loop in the else
V['elif2'] = '''			msg = NULL;
			if (strlen(s) == 12) {
				if (!validateString(s)) {
''' + MS + AG1 + '''					msg = ''' + CH + ''';
				}
			} else
				msg = ''' + LN + ''';
			if (msg) {
''' + tail('\t\t\t\t') + '''			} else {
''' + LOOP.replace('\t\t\t\t\t', '\t\t\t\t') + '''			}
'''
# e: message defaults to the length one
V['dflt'] = '''			msg = ''' + LN + ''';
			if (strlen(s) == 12) {
				if (validateString(s)) {
''' + LOOP + '''					msg = NULL;
				} else {
''' + MS + AG1 + '''					msg = ''' + CH + ''';
				}
			}
			if (msg) {
''' + tail('\t\t\t\t') + '''			}
'''
# f: ok flag; tail when not ok, msg chosen by length
V['okf'] = '''			ok = 0;
			if (strlen(s) == 12) {
				if (validateString(s)) {
''' + LOOP + '''					ok = 1;
				} else {
''' + MS + AG1 + '''					msg = ''' + CH + ''';
				}
			} else
				msg = ''' + LN + ''';
			if (!ok) {
''' + tail('\t\t\t\t') + '''			}
'''
# g: ternary message
V['tern'] = '''			if (strlen(s) == 12 && validateString(s)) {
''' + LOOP.replace('\t\t\t\t\t', '\t\t\t\t') + '''			} else {
''' + MS.replace('\t\t\t\t\t', '\t\t\t\t') + AG1.replace('\t\t\t\t\t', '\t\t\t\t') + '''				log_printf(0, strlen(s) == 12 ? ''' + CH + ''' : ''' + LN + ''');
				showHexPairs(0, s);
				log_printf(0, ''' + TAIL + ''', s);
			}
'''


def build(v, rm):
    t = optlib.read_src(os.environ.get('OPBASE', optlib.SRC))
    assert OLD in t
    t = t.replace(OLD, V[v], 1)
    decl = '\tchar *s;\n\tint i;\n\n\tOPT("nomobile"'
    assert decl in t
    t = t.replace(decl, '\tchar *s;\n\tconst char *msg;\n\tint i, ok;\n\n\tOPT("nomobile"', 1)
    for old, new in RM[rm]:
        if old not in t:
            return None
        t = t.replace(old, new, 1)
    return t


def run(c):
    t = build(*c)
    if t is None:
        return c, {'compile': 'edit missing'}
    return c, optlib.score_text(t, optlib.P83)


def main():
    a = sys.argv[1:]
    if a and a[0] == 'show':
        v, _, rm = a[1].partition('+')
        t = build(v, rm or 'none')
        if os.environ.get('OUT'):
            open(os.environ['OUT'], 'w', newline='\n').write(t)
        optlib.vdiff(t, optlib.P83)
        return
    vs = a or list(V)
    rms = os.environ.get('RMS', 'none,ag1,dz1,dzall').split(',')
    with ThreadPoolExecutor(8) as ex:
        res = list(ex.map(run, [(v, r) for v in vs for r in rms]))
    for (v, r), s in res:
        print('%-8s %-6s %s' % (v, r, optlib.fmt(s)))


if __name__ == '__main__':
    main()
