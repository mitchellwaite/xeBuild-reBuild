"""loadBl in the loop, all hints off, and the shapes loadConsoleBlFiles uses for case 5's head, plus forms of the tail after the signature check."""
import itertools, re, importlib.util, os
spec = importlib.util.spec_from_file_location('g133', os.path.join(os.path.dirname(os.path.abspath(__file__)), 'gen_bd133.py'))
g = importlib.util.module_from_spec(spec)
spec.loader.exec_module(g)


def block(t, a, b):
    i = t.index(a)
    j = t.index(b, i)
    return i, j


def norm(t):
    """whitespace-insensitive edits are easier on a stripped text: remove indentation from the switch only by regex in sub()"""
    return t


def rsub(t, old, new):
    """old is matched with any leading whitespace on each line"""
    pat = r'[ \t]*' + r'\n[ \t]*'.join(re.escape(l) for l in old.split('\n'))
    t2, n = re.subn(pat, lambda m: new, t, count=1)
    if not n:
        raise ValueError('no match ' + old[:50])
    return t2


HEAD_CUR = '''if (r) {
if (type == 9) {
if (!suGetCF(&e->data, &e->size))
break;
} else if (__builtin_expect(type == 10, 0)) {
if (!suGetCG(&e->data, &e->size))
break;
goto chk;
} else
break;
}'''
HEADS = {
    'cur': '''if (r) {
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
''',
    'cons': '''if (r) {
if (type == 9) {
if (suGetCF(&e->data, &e->size))
r = 0;
} else if (type == 10) {
if (suGetCG(&e->data, &e->size))
r = 0;
}
if (r)
break;
}
''',
}
TAIL_OLD = '''if (xb.type <= BUILD_DEVGL16) {
t5le: __attribute__((hot));
if (__builtin_expect(r != 0, 0))
goto fail;
break;
}
if (type == 14)
setFlashBuild(getBeU16(xb.files[i].data + 2));
break;'''
TAILS = {
    'gt': 'if (xb.type > BUILD_DEVGL16 && type == 14)\nsetFlashBuild(getBeU16(xb.files[i].data + 2));\nbreak;',
    'nest': 'if (xb.type > BUILD_DEVGL16) {\nif (type == 14)\nsetFlashBuild(getBeU16(xb.files[i].data + 2));\n}\nbreak;',
    'r': 'if (xb.type <= BUILD_DEVGL16) {\nif (r)\nr = -1;\nbreak;\n}\nif (type == 14)\nsetFlashBuild(getBeU16(xb.files[i].data + 2));\nbreak;',
    'le': 'if (xb.type <= BUILD_DEVGL16)\nbreak;\nif (type == 14)\nsetFlashBuild(getBeU16(xb.files[i].data + 2));\nbreak;',
    'type': 'if (type == 14 && xb.type > BUILD_DEVGL16)\nsetFlashBuild(getBeU16(xb.files[i].data + 2));\nbreak;',
}


def PRE(b):
    t = g.inline(b, fail='none')
    t = rsub(t, HEAD_CUR, '@HEAD@')
    t = rsub(t, TAIL_OLD, '@TAIL@')
    # the constant_p entry
    t = re.sub(r'/\* never taken, but the edge.*?\*/\s*if \(\(char \*\)__builtin_constant_p\(i\).*?\}\n', '', t, flags=re.S)
    t = t.replace('__asm__("" : "+a"(d));\n', '\n')
    t = t.replace('badsize: __attribute__((hot));\n', '\n')
    # the patch size and the smc failure
    t = rsub(t, 'log_printf(1, "\\n\\n***** ERROR: patch size 0x%x is not a multiple of 4!\\n", e->size);\ngoto fail;', 'log_printf(1, "\\n\\n***** ERROR: patch size 0x%x is not a multiple of 4!\\n", e->size);\nr = -1;\nbreak;')
    t = rsub(t, 'if (!e->offset)\ngoto fail;', 'if (!e->offset)\nr = -1;')
    return t


def CASES(base):
    out = []
    for h, tl in itertools.product(HEADS, TAILS):
        t = base.replace('@HEAD@', HEADS[h]).replace('@TAIL@', TAILS[tl])
        if h == 'cons':
            t = t.replace('chk:\n', '')
        out.append(('%s %s' % (h, tl), t))
    return out
