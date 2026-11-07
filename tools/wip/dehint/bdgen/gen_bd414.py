"""Attempt 30: loadBl rebuilt with the signature check (and optionally the type-14 tail) after the switch, shared by every
arm at profile_estimate and threaded away by vrp1 for the arms whose type is known (attempt 24's lever, in a from-scratch
shape).  All seven loadBl hints off (etype axis only as a diagnostic).
Axes:
  RES   ptr (`*pr`) / retu (a local `uint32_t r` returned).
  POS   after: sig check and tail after the switch behind `if (r) return`; sig: only the sig check after the switch
        (tail stays in the arm, before it: the two never both act, since 5/11/17 aren't 14); arm: src's place.
  GUARD ret: `if (r) return r;` then the tests; and: `if (!r && (type == 5 || ..))` and the tail `if (!r && ..)`.
  FB    and9 / src.  FAIL c2 / end.  TAIL plain / and.  DEAD 0/1 (`else if (type)`, diagnostic).
Behaviour: the sig check runs only for 5/11/17 (all in the 5..21 arm) after checkBl returned 0; the tail only for 14
(the arm or SE) after a 0 result; every other arm's r passes through unchanged."""
import itertools, os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bdrun
from a30lib import off7, LB, LBF
import gen_bd411 as g

FB = {'src': g.FB_SRC, 'and9': g.FB_AND9}
SIGB = '''if (type == 5 || type == 17 || type == 11) {
	if (xb.pub1bl) {
		if (!cbVerifySig(e->data, xb.pub1bl)) {
			log_printf(0, "\\n***** ERROR: loaded %s, but signature check failed!\\n", e->name);
			R = -1;
		} else DEAD
			log_printf(1, "loaded %s, signature check passed!\\n", e->name);
	} else
		log_printf(1, "loaded %s, could not check signature rsa key not present!\\n", e->name);
}
'''
TAILB = {
    'plain': '''if (xb.type <= BUILD_DEVGL16)
	BRK;
if (type == 14)
	setFlashBuild(getBeU16(xb.files[i].data + 2));
''',
    'and': '''if (xb.type > BUILD_DEVGL16 && type == 14)
	setFlashBuild(getBeU16(xb.files[i].data + 2));
''',
}


def ind(t, n):
    return '\n'.join(('\t' * n + l if l else l) for l in t.split('\n'))


def mk(b, res, pos, guard, fb, fail, tail, dead):
    if pos == 'arm' and guard != 'ret':
        return None
    if pos == 'arm' and tail == 'plain' and False:
        return None
    i, j = bdrun.fnspan(b, LB)
    f = b[i:j]
    k0 = f.index('\tcase 6:\n')
    k1 = f.index('\tdefault:\n')
    rest = f[k0:k1]
    if fail == 'c2':
        rest = bdrun.sub(rest, g.C2A, g.C2B, 1)
    R = '*pr' if res == 'ptr' else 'r'
    sig = SIGB.replace('DEAD', 'if (type)' if dead else '').replace('else \n', 'else\n').replace('R = -1', '*pr = -1')
    tl = TAILB[tail]
    arm = '''	case 5: case 7: case 8: case 9: case 10: case 11: case 12: case 13:
	case 14: case 15: case 16: case 17: case 18: case 19: case 20: case 21:
		*pr = loadInputFile(e->name, e, 1, 0, NULL, 0, 0, 1);
		if (*pr) {
%s		}
		if (type == 9 && e->data[0] == 'S' && e->data[1] == 'E') {
			/* an SE where the CF goes */
			e->type = type = 14;
			xb.cfLdv = 0;
			xb.seReplacesCf = 1;
		}
	chk:
		*pr = checkBl(e->data, e->size, type, e->crc);
''' % FB[fb]
    after = ''
    if pos == 'arm':
        arm += '\t\tif (*pr)\n\t\t\tbreak;\n' + ind(sig, 2) + ind(tl.replace('BRK', 'break'), 2) + '\t\tbreak;\n'
    elif pos == 'sig':
        if tail == 'plain':
            arm += '''		if (*pr)
			break;
		if (xb.type > BUILD_DEVGL16 && type == 14)
			setFlashBuild(getBeU16(xb.files[i].data + 2));
		break;
'''
        else:
            arm += '''		if (!*pr && xb.type > BUILD_DEVGL16 && type == 14)
			setFlashBuild(getBeU16(xb.files[i].data + 2));
		break;
'''
        if guard == 'ret':
            after = '\tif (*pr)\n\t\treturn;\n' + ind(sig, 1)
        else:
            after = ind(sig.replace('if (type == 5 ||', 'if (!*pr && (type == 5 ||').replace('type == 11) {', 'type == 11)) {', 1), 1)
    else:
        arm += '\t\tbreak;\n'
        if guard == 'ret':
            after = '\tif (*pr)\n\t\treturn;\n' + ind(sig, 1) + ind(tl.replace('BRK', 'return'), 1)
        else:
            if tail == 'plain':
                return None
            after = ind(sig.replace('if (type == 5 ||', 'if (!*pr && (type == 5 ||').replace('type == 11) {', 'type == 11)) {', 1), 1)
            after += '\tif (!*pr && xb.type > BUILD_DEVGL16 && type == 14)\n\t\tsetFlashBuild(getBeU16(xb.files[i].data + 2));\n'
    sig_r = None
    body = '''static void loadBl(struct fileent *e, uint32_t i, uint32_t *pr)
{
	int type;

	type = e->type;
	switch (type) {
''' + arm + rest + '''	default:
		log_printf(1, "####### unhandled bl load %d %s\\n", type, e->name);
		break;
	}
''' + after.replace('R = -1', '*pr = -1') + '''	return;
'''
    if fail == 'end':
        body += 'fail:\n\t*pr = -1;\n'
    body += '}\n'
    if res == 'retu':
        k = body.index('{')
        body = body[:k] + body[k:].replace('*pr', 'r')
        body = bdrun.sub(body, 'static void loadBl(struct fileent *e, uint32_t i, uint32_t *pr)\n{\n\tint type;\n',
                         'static uint32_t loadBl(struct fileent *e, uint32_t i)\n{\n\tuint32_t r = 0;\n\tint type;\n', 1)
        body = body.replace('\t\treturn;\n', '\t\treturn r;\n').replace('\treturn;\n', '\treturn r;\n')
        body = body.replace('fail:\n\tr = -1;\n', 'fail:\n\treturn -1;\n')
    b = b[:i] + body + b[j:]
    if res == 'retu':
        b = bdrun.sub(b, g.LOOP_CALL, g.LOOP_CALL.replace('loadBl(e, i, &r);', 'r = loadBl(e, i);'), 1)
    return b


PRE = g.PRE


def CASES(base):
    return [(' '.join(map(str, k)), lambda b, k=k: mk(b, *k))
            for k in itertools.product(['ptr', 'retu'], ['after', 'sig', 'arm'], ['ret', 'and'], ['and9', 'src'],
                                       ['c2', 'end'], ['plain', 'and'], [0, 1])]


FOCUS = ['_loadBlFiles']
