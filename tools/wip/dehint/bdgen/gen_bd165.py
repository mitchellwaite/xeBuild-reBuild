"""loadBl keeps *pr, the update fallback as loadConsoleBlFiles writes it (no goto chk).  No constant_p, no expect on type 10."""
import importlib.util, itertools, os
d = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location('g161', os.path.join(d, 'gen_bd161.py'))
g1 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(g1)
g = g1.g

SE = '''if (type == 9 && e->data[0] == 'S' && e->data[1] == 'E') {
e->type = type = 14;
xb.cfLdv = 0;
xb.seReplacesCf = 1;
}
'''
FALLS = {
    'con': '''if (*pr) {
if (type == 9) {
if (suGetCF(&e->data, &e->size))
*pr = 0;
} else if (type == 10) {
if (suGetCG(&e->data, &e->size))
*pr = 0;
}
}
''',
    'and': '''if (*pr && type == 9) {
if (suGetCF(&e->data, &e->size))
*pr = 0;
} else if (*pr && type == 10) {
if (suGetCG(&e->data, &e->size))
*pr = 0;
}
''',
    'seq': '''if (*pr && type == 9 && suGetCF(&e->data, &e->size))
*pr = 0;
if (*pr && type == 10 && suGetCG(&e->data, &e->size))
*pr = 0;
''',
    'nest2': '''if (*pr) {
if (type == 9 && suGetCF(&e->data, &e->size))
*pr = 0;
else if (type == 10 && suGetCG(&e->data, &e->size))
*pr = 0;
}
''',
}
SEFORM = {
    # the SE test before the error test, after it, or in the CF path
    'in': 'if (!*pr) {\n' + SE + '*pr = checkBl(e->data, e->size, type, e->crc);\nBODY}\n',
    'brk': 'if (*pr)\nbreak;\n' + SE + '*pr = checkBl(e->data, e->size, type, e->crc);\nBODY',
}
BODY = {
    'nest': 'if (!*pr) {\nSIG\nTAIL\n}\n',
    'brk': 'if (*pr)\nbreak;\nSIG\nTAIL\n',
}
TAILS = g1.TAILS
SIGN = ['dead', 'a', 'c']


def arm(fall, se, body, sg, tail):
    s = 'if (type == 5 || type == 17 || type == 11) {\n' + g.sig(sg) + '}\n'
    b = BODY[body].replace('SIG\n', s).replace('TAIL\n', TAILS[tail])
    return '*pr = loadInputFile(e->name, e, 1, 0, NULL, 0, 0, 1);\n' + FALLS[fall] + SEFORM[se].replace('BODY', b) + 'break;\n'


def CASES(base):
    out = []
    for fall, se, body, sg, tail, bad in itertools.product(FALLS, SEFORM, BODY, SIGN, ('failx', 'fail', 'and', 'nest', 'brk'), (0, 1)):
        def mk(b, fall=fall, se=se, body=body, sg=sg, tail=tail, bad=bad):
            t = g.with_arm(b, arm(fall, se, body, sg, tail))
            t = g.nocp(t)
            return g.nobad(t) if bad else t
        out.append(('%s %s %s %s %s bad%d' % (fall, se, body, sg, tail, bad), mk))
    return out


FOCUS = ['_loadBlFiles']
