"""loadBlFiles as loadConsoleBlFiles is written: the switch in the loop, r a local, r = -1 where it fails, no helper.  Attempt 6.

Built from src/build.c at attempt 5's commit: loadBl's text with *pr -> r."""
import importlib.util, itertools, os, re
d = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location('g161', os.path.join(d, 'gen_bd161.py'))
g1 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(g1)
g = g1.g

LOADS = {
    # the update fallback
    'brk': '''r = loadInputFile(e->name, e, 1, 0, NULL, 0, 0, 1);
if (r) {
if (type == 9) {
if (!suGetCF(&e->data, &e->size))
break;
} else if (type == 10) {
if (!suGetCG(&e->data, &e->size))
break;
goto chk;
} else
break;
}
SE
chk:
r = checkBl(e->data, e->size, type, e->crc);
BODY
''',
    # console's form, with the SE test ahead of checkBl
    'con': '''r = loadInputFile(e->name, e, 1, 0, NULL, 0, 0, 1);
if (r) {
if (type == 9) {
if (suGetCF(&e->data, &e->size))
r = 0;
} else if (type == 10) {
if (suGetCG(&e->data, &e->size))
r = 0;
}
}
if (!r) {
SE
r = checkBl(e->data, e->size, type, e->crc);
BODY
}
''',
}
SE = '''if (type == 9 && e->data[0] == 'S' && e->data[1] == 'E') {
e->type = type = 14;
xb.cfLdv = 0;
xb.seReplacesCf = 1;
}
'''
BODIES = {
    'nest': 'if (!r) {\nSIG\nTAIL\n}\n',
    'brk': 'if (r)\nbreak;\nSIG\nTAIL\n',
}
TAILS = {
    'and': 'if (xb.type > BUILD_DEVGL16 && type == 14)\nsetFlashBuild(getBeU16(xb.files[i].data + 2));\n',
    'nest': 'if (xb.type > BUILD_DEVGL16) {\nif (type == 14)\nsetFlashBuild(getBeU16(xb.files[i].data + 2));\n}\n',
    'brk': 'if (xb.type <= BUILD_DEVGL16)\nbreak;\nif (type == 14)\nsetFlashBuild(getBeU16(xb.files[i].data + 2));\n',
}
SIGN = ['a', 'b', 'c', 'd', 'dead']


def sigtext(s):
    t = g.sig(s).replace('*pr', 'r')
    return 'if (type == 5 || type == 17 || type == 11) {\n' + t + '}\n'


def arm(ld, body, sg, tail):
    b = BODIES[body].replace('SIG', sigtext(sg)).replace('TAIL', TAILS[tail])
    return LOADS[ld].replace('SE\n', SE).replace('BODY\n', b)


def loop(base, a, fails='flag'):
    """loadBlFiles with the switch written in the loop"""
    i = base.index('/* load the input file e (xb.files[i]) by its type */')
    j = base.index('int loadConsoleBlFiles(void)')
    fn = base[i:j]
    k = fn.index('switch (type) {')
    m = fn.index('\treturn;\n', k)
    sw = fn[k:m].replace('*pr', 'r')
    # the arm
    p = sw.index('r = loadInputFile(e->name, e, 1, 0, NULL, 0, 0, 1);')
    q = sw.index('\tcase 6:\n', p)
    sw = sw[:p] + a + 'break;\n' + sw[q:]
    # no constant_p, no labels, no shared fail
    x = sw.index('/* never taken, but the edge lasts until dom2')
    y = sw.index('break;\n', sw.index('goto chk;', x))
    sw = sw[:x] + sw[y:]
    sw = sw.replace('badsize: __attribute__((hot));\n', '')
    sw = re.sub(r'goto fail;', 'r = -1;', sw)
    sw = sw.replace('r = -1;\n\t\t}\n\t\tappendAddonPatches(e);', 'r = -1;\nbreak;\n\t\t}\n\t\tappendAddonPatches(e);')
    new = '''int loadBlFiles(void)
{
	struct fileent *e;
	uint32_t i;
	uint32_t r;

	for (i = 1; i < (uint32_t)xb.nFiles; i++) {
		e = &xb.files[i];
		r = 0;
		if (strnicmp(e->name, "none", 4) || e->crc) {
			int type = e->type;

			''' + sw + '''
		}
		if (r) {
			log_printf(0, "\\n\\n**** could not read %s (%i) ****\\n\\n", e->name, r);
			return -1;
		}
	}
	return 0;
}

'''
    # defaultBl60 stays
    return base[:i] + new + base[j:]


def CASES(base):
    out = []
    for ld, body, sg, tail in itertools.product(LOADS, BODIES, SIGN, TAILS):
        def mk(b, ld=ld, body=body, sg=sg, tail=tail):
            return loop(b, arm(ld, body, sg, tail))
        out.append(('%s %s %s %s' % (ld, body, sg, tail), mk))
    return out


FOCUS = ['_loadBlFiles']
