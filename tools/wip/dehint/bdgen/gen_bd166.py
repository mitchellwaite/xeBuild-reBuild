"""More update fallbacks, looking for a non-constant way into the shared checkBl that lasts until dom2 (the job constant_p does)."""
import importlib.util, itertools, os
d = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location('g165', os.path.join(d, 'gen_bd165.py'))
g5 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(g5)
g = g5.g

SE = g5.SE
CHK = '*pr = checkBl(e->data, e->size, type, e->crc);\n'
FORMS = {
    # CF clears *pr and falls in, CG goes straight to its check
    'c3': '''if (*pr) {
if (type == 9) {
if (suGetCF(&e->data, &e->size))
*pr = 0;
} else if (type == 10) {
if (!suGetCG(&e->data, &e->size))
break;
goto chk;
}
}
if (*pr)
break;
''' + SE + 'chk:\n' + CHK,
    'c4': '''if (*pr) {
if (type == 9) {
if (!suGetCF(&e->data, &e->size))
break;
} else if (type == 10) {
if (suGetCG(&e->data, &e->size))
*pr = 0;
}
}
if (*pr)
break;
''' + SE + CHK,
    'c5': '''if (*pr) {
if (type == 9) {
if (!suGetCF(&e->data, &e->size))
break;
*pr = 0;
} else if (type == 10) {
if (!suGetCG(&e->data, &e->size))
break;
*pr = 0;
}
}
if (*pr)
break;
''' + SE + CHK,
    'c6': '''if (*pr) {
if (type != 9 && type != 10)
break;
if (type == 9) {
if (!suGetCF(&e->data, &e->size))
break;
} else {
if (!suGetCG(&e->data, &e->size))
break;
}
}
''' + SE + CHK,
    'c7': '''if (*pr) {
if (type == 9) {
if (!suGetCF(&e->data, &e->size))
break;
} else if (type == 10) {
if (!suGetCG(&e->data, &e->size))
break;
} else
break;
}
''' + SE + CHK,
    'c8': '''if (*pr) {
if (type == 9 ? !suGetCF(&e->data, &e->size) : type == 10 ? !suGetCG(&e->data, &e->size) : 1)
break;
}
''' + SE + CHK,
    'c9': '''if (*pr) {
if (type == 9) {
if (!suGetCF(&e->data, &e->size))
break;
} else if (type == 10) {
if (!suGetCG(&e->data, &e->size))
break;
} else
break;
*pr = 0;
}
''' + SE + CHK,
}


def arm(form, body, sg, tail):
    s = 'if (type == 5 || type == 17 || type == 11) {\n' + g.sig(sg) + '}\n'
    b = g5.BODY[body].replace('SIG\n', s).replace('TAIL\n', g5.TAILS[tail])
    return '*pr = loadInputFile(e->name, e, 1, 0, NULL, 0, 0, 1);\n' + FORMS[form] + b + 'break;\n'


def CASES(base):
    out = []
    for form, body, sg, tail, bad in itertools.product(FORMS, g5.BODY, ('dead', 'a'), ('failx', 'fail', 'and', 'brk'), (0, 1)):
        def mk(b, form=form, body=body, sg=sg, tail=tail, bad=bad):
            t = g.with_arm(b, arm(form, body, sg, tail))
            t = g.nocp(t)
            return g.nobad(t) if bad else t
        out.append(('%s %s %s %s bad%d' % (form, body, sg, tail, bad), mk))
    return out


FOCUS = ['_loadBlFiles']
