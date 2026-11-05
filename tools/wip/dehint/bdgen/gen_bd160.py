"""loadBl's case 5 arm with no constant_p: signature forms x tail forms x hints left (attempt 6).

The type-11 copy is an FSM thread: dom3 walks the tail's PHI arguments in edge order, and the first argument with type_N (the PHI in the
pub1bl block) decides, since the block then counts as visited.  So the no-key arm's edge has to come before the passed arm's in the tail."""
import itertools, os, re

SIGS = {
    # the signature test, *pr = -1 on failure
    'a': '''if (xb.pub1bl) {
	if (!cbVerifySig(e->data, xb.pub1bl)) {
		FAILED
	} else
		PASSED
} else
	NOKEY
''',
    'b': '''if (xb.pub1bl) {
	if (cbVerifySig(e->data, xb.pub1bl))
		PASSED
	else {
		FAILED
	}
} else
	NOKEY
''',
    'c': '''if (!xb.pub1bl)
	NOKEY
else if (!cbVerifySig(e->data, xb.pub1bl)) {
	FAILED
} else
	PASSED
''',
    'd': '''if (!xb.pub1bl)
	NOKEY
else if (cbVerifySig(e->data, xb.pub1bl))
	PASSED
else {
	FAILED
}
''',
    'e': '''if (!xb.pub1bl) {
	NOKEY
} else {
	if (!cbVerifySig(e->data, xb.pub1bl)) {
		FAILED
	} else {
		PASSED
	}
}
''',
    'f': '''if (xb.pub1bl) {
	if (cbVerifySig(e->data, xb.pub1bl)) {
		PASSED
	} else {
		FAILED
	}
} else {
	NOKEY
}
''',
    'dead': '''if (xb.pub1bl) {
	if (!cbVerifySig(e->data, xb.pub1bl)) {
		FAILED
	} else if (type)
		PASSED
} else
	NOKEY
''',
}
TXT = {
    'FAILED': 'log_printf(0, "\\n***** ERROR: loaded %s, but signature check failed!\\n", e->name);\n*pr = -1;',
    'PASSED': 'log_printf(1, "loaded %s, signature check passed!\\n", e->name);',
    'NOKEY': 'log_printf(1, "loaded %s, could not check signature rsa key not present!\\n", e->name);',
}
TAILS = {
    # after the signature test; nest: inside if (!*pr)
    'brk': 'if (xb.type <= BUILD_DEVGL16)\nbreak;\nif (type == 14)\nsetFlashBuild(getBeU16(xb.files[i].data + 2));\n',
    'and': 'if (xb.type > BUILD_DEVGL16 && type == 14)\nsetFlashBuild(getBeU16(xb.files[i].data + 2));\n',
    'nest': 'if (xb.type > BUILD_DEVGL16) {\nif (type == 14)\nsetFlashBuild(getBeU16(xb.files[i].data + 2));\n}\n',
}


def sig(name):
    s = SIGS[name]
    for k, v in TXT.items():
        s = s.replace(k, v)
    return s


def arm(sg, tail, nest, t10=False):
    """the text of the arm from its first load to the break before case 6"""
    t = '''*pr = loadInputFile(e->name, e, 1, 0, NULL, 0, 0, 1);
if (*pr) {
if (type == 9) {
if (!suGetCF(&e->data, &e->size))
break;
} else if (%s) {
if (!suGetCG(&e->data, &e->size))
break;
goto chk;
} else
break;
}
if (type == 9 && e->data[0] == 'S' && e->data[1] == 'E') {
e->type = type = 14;
xb.cfLdv = 0;
xb.seReplacesCf = 1;
}
chk:
*pr = checkBl(e->data, e->size, type, e->crc);
''' % ('__builtin_expect(type == 10, 0)' if t10 else 'type == 10')
    body = 'if (type == 5 || type == 17 || type == 11) {\n' + sig(sg) + '}\n' + TAILS[tail]
    if nest:
        t += 'if (!*pr) {\n' + body + '}\n'
    else:
        t += 'if (*pr)\nbreak;\n' + body
    return t + 'break;\n'


def with_arm(base, a):
    i = base.index('*pr = loadInputFile(e->name, e, 1, 0, NULL, 0, 0, 1);', base.index('static void loadBl('))
    j = base.index('\tcase 6:\n', i)
    return base[:i] + a + base[j:]


def nocp(t):
    i = t.index('/* never taken, but the edge lasts until dom2')
    j = t.index('break;\n', t.index('goto chk;', i))
    return t[:i] + t[j:]


def nobad(t):
    return t.replace('badsize: __attribute__((hot));\n', '')


def CASES(base):
    out = []
    for sg, tl, n in itertools.product(SIGS, TAILS, (0, 1)):
        for bad in (0, 1):
            def mk(b, sg=sg, tl=tl, n=n, bad=bad):
                t = with_arm(b, arm(sg, tl, n))
                t = nocp(t)
                return nobad(t) if bad else t
            out.append(('%s %s n%d bad%d' % (sg, tl, n, bad), mk))
    return out


FOCUS = ['_loadBlFiles']
