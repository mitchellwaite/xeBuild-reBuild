"""loadBl's bootloader case in error-variable forms, as loadConsoleBlFiles' fell to (`if (!r) r = checkBl`), static with *pr or written in the loop with r.  Hints off in sets."""
import itertools, re, importlib.util, os
spec = importlib.util.spec_from_file_location('g133', os.path.join(os.path.dirname(os.path.abspath(__file__)), 'gen_bd133.py'))
g = importlib.util.module_from_spec(spec)
spec.loader.exec_module(g)

CHK_A = 'if (type == 9 && e->data[0] == \'S\' && e->data[1] == \'E\') {\n/* an SE where the CF goes */\ne->type = type = 14;\nxb.cfLdv = 0;\nxb.seReplacesCf = 1;\n}\n'
SIG = '''if (type == 5 || type == 17 || type == 11) {
if (xb.pub1bl) {
if (!cbVerifySig(e->data, xb.pub1bl)) {
log_printf(0, "\\n***** ERROR: loaded %s, but signature check failed!\\n", e->name);
R = -1;
} else if (type)
log_printf(1, "loaded %s, signature check passed!\\n", e->name);
} else
log_printf(1, "loaded %s, could not check signature rsa key not present!\\n", e->name);
}
'''
FLASH = 'if (type == 14 && xb.type > BUILD_DEVGL16)\nsetFlashBuild(getBeU16(xb.files[i].data + 2));\n'
FLASH2 = 'if (xb.type > BUILD_DEVGL16 && type == 14)\nsetFlashBuild(getBeU16(xb.files[i].data + 2));\n'
FB = '''if (R) {
if (type == 9) {
if (suGetCF(&e->data, &e->size))
R = 0;
} else if (type == 10) {
if (suGetCG(&e->data, &e->size))
R = 0;
}
}
'''
SE2 = FB
HEADS = {
    # the SE test and checkBl under one !r
    'a': FB + 'if (!R) {\n' + CHK_A + 'R = checkBl(e->data, e->size, type, e->crc);\n@T@}\nbreak;\n',
    # checkBl then a second !r
    'b': FB + 'if (!R) {\n' + CHK_A + 'R = checkBl(e->data, e->size, type, e->crc);\n}\nif (!R) {\n@T@}\nbreak;\n',
    # the SE test before the fallback's !r
    'c': 'if (R) {\nif (type == 9) {\nif (suGetCF(&e->data, &e->size))\nR = 0;\n} else if (type == 10) {\nif (suGetCG(&e->data, &e->size))\nR = 0;\n}\n}\nif (R)\nbreak;\n' + CHK_A + 'R = checkBl(e->data, e->size, type, e->crc);\nif (!R) {\n@T@}\nbreak;\n',
}
TAILS = {
    'plain': SIG + FLASH2,
    'plain2': SIG + FLASH,
    'r': SIG + 'if (!R && xb.type > BUILD_DEVGL16 && type == 14)\nsetFlashBuild(getBeU16(xb.files[i].data + 2));\n',
    'nest': SIG + 'if (xb.type > BUILD_DEVGL16) {\nif (type == 14)\nsetFlashBuild(getBeU16(xb.files[i].data + 2));\n}\n',
}


def ws(old):
    return r'[ \t]*' + r'\n[ \t]*'.join(re.escape(l) for l in old.split('\n'))


def edit(t, R, head, tail):
    i = t.index('type == 9) {\n', t.index('case 5: case 7:'))
    a = t.rindex('if (', 0, t.rindex('if (', 0, i))
    a = t.rindex('\n', 0, a) + 1
    b = t.index('case 6:', i)
    b = t.rindex('\n', 0, b) + 1
    s = re.sub(r'\bR\b', lambda m: R, HEADS[head].replace('@T@', TAILS[tail]))
    return t[:a] + s + t[b:]


def fix(t, R):
    t = re.sub(r'/\* never taken, but the edge.*?\*/\s*if \(\(char \*\)__builtin_constant_p\(i\).*?\}\n', '', t, flags=re.S)
    t = t.replace('__asm__("" : "+a"(d));\n', '\n')
    t = t.replace('badsize: __attribute__((hot));\n', '\n')
    t = re.sub(ws('e->size);\ngoto fail;'), 'e->size);\n%s = -1;\nbreak;' % R, t, count=1)
    t = re.sub(ws('if (!e->offset)\ngoto fail;'), 'if (!e->offset)\n%s = -1;' % R, t, count=1)
    return t


def CASES(base):
    out = []
    inl = g.inline(base, fail='none')
    for form, head, tail in itertools.product(('static', 'loop'), HEADS, TAILS):
        if form == 'static':
            t = edit(base, '*pr', head, tail)
            t = fix(t, '*pr')
            t = re.sub(r'\t/\* one -1 block.*?fail:\n\t__asm__ __volatile__\(""\);\n\t\*pr = -1;\n', '', t, flags=re.S)
        else:
            t = edit(inl, 'r', head, tail)
            t = fix(t, 'r')
        out.append(('%s %s %s' % (form, head, tail), t))
    return out
