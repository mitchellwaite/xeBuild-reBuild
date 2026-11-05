"""loadBl with no hints at all: gen_bd137's best with more axes.  Fallback form, where the checkBl tests nest, `else if (type)` or plain, how the shared -1 is written, forms of the flash build test."""
import itertools, re, importlib.util, os
spec = importlib.util.spec_from_file_location('g133', os.path.join(os.path.dirname(os.path.abspath(__file__)), 'gen_bd133.py'))
g = importlib.util.module_from_spec(spec)
spec.loader.exec_module(g)

SE = 'if (type == 9 && e->data[0] == \'S\' && e->data[1] == \'E\') {\n/* an SE where the CF goes */\ne->type = type = 14;\nxb.cfLdv = 0;\nxb.seReplacesCf = 1;\n}\n'


def sig(el):
    return '''if (type == 5 || type == 17 || type == 11) {
if (xb.pub1bl) {
if (!cbVerifySig(e->data, xb.pub1bl)) {
log_printf(0, "\\n***** ERROR: loaded %s, but signature check failed!\\n", e->name);
R = -1;
} else''' + (' if (type)' if el else '') + '''
log_printf(1, "loaded %s, signature check passed!\\n", e->name);
} else
log_printf(1, "loaded %s, could not check signature rsa key not present!\\n", e->name);
}
'''


FLASH = {
    'gt': 'if (xb.type > BUILD_DEVGL16 && type == 14)\nsetFlashBuild(getBeU16(xb.files[i].data + 2));\n',
    'ty': 'if (type == 14 && xb.type > BUILD_DEVGL16)\nsetFlashBuild(getBeU16(xb.files[i].data + 2));\n',
    'ne': 'if (xb.type > BUILD_DEVGL16) {\nif (type == 14)\nsetFlashBuild(getBeU16(xb.files[i].data + 2));\n}\n',
    'le': 'if (xb.type <= BUILD_DEVGL16)\nbreak;\nif (type == 14)\nsetFlashBuild(getBeU16(xb.files[i].data + 2));\n',
}
FB = {
    'n': 'if (R) {\nif (type == 9) {\nif (suGetCF(&e->data, &e->size))\nR = 0;\n} else if (type == 10) {\nif (suGetCG(&e->data, &e->size))\nR = 0;\n}\n}\n',
    's': 'if (R) {\nif (type == 9 && suGetCF(&e->data, &e->size))\nR = 0;\nelse if (type == 10 && suGetCG(&e->data, &e->size))\nR = 0;\n}\n',
    'b': None,
}
BODY = {
    'c': '@FB@if (R)\nbreak;\n' + SE + 'R = checkBl(e->data, e->size, type, e->crc);\nif (!R) {\n@S@@F@}\nbreak;\n',
    'a': '@FB@if (!R) {\n' + SE + 'R = checkBl(e->data, e->size, type, e->crc);\nif (!R) {\n@S@@F@}\n}\nbreak;\n',
    'd': '@FB@if (R)\nbreak;\n' + SE + 'R = checkBl(e->data, e->size, type, e->crc);\nif (R)\nbreak;\n@S@@F@break;\n',
    'e': '@FB@if (!R) {\n' + SE + 'R = checkBl(e->data, e->size, type, e->crc);\nif (R)\nbreak;\n@S@@F@}\nbreak;\n',
}


def ws(old):
    return r'[ \t]*' + r'\n[ \t]*'.join(re.escape(l) for l in old.split('\n'))


def edit(t, R, body, fb, el, fl):
    i = t.index('type == 9) {\n', t.index('case 5: case 7:'))
    a = t.rindex('if (', 0, t.rindex('if (', 0, i))
    a = t.rindex('\n', 0, a) + 1
    b = t.index('case 6:', i)
    b = t.rindex('\n', 0, b) + 1
    f = FB[fb] or 'if (R) {\nif (type == 9) {\nif (!suGetCF(&e->data, &e->size))\nbreak;\n} else if (type == 10) {\nif (!suGetCG(&e->data, &e->size))\nbreak;\n} else\nbreak;\nR = 0;\n}\n'
    s = BODY[body].replace('@FB@', f).replace('@S@', sig(el)).replace('@F@', FLASH[fl])
    s = re.sub(r'\bR\b', lambda m: R, s)
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
    for form, body, fb, el, fl in itertools.product(('static', 'loop'), BODY, FB, (0, 1), FLASH):
        if form == 'static':
            t = edit(base, '*pr', body, fb, el, fl)
            t = fix(t, '*pr')
            t = re.sub(r'\t/\* one -1 block.*?fail:\n\t__asm__ __volatile__\(""\);\n\t\*pr = -1;\n', '', t, flags=re.S)
        else:
            t = edit(inl, 'r', body, fb, el, fl)
            t = fix(t, 'r')
        out.append(('%s %s %s el%d %s' % (form, body, fb, el, fl), t))
    return out
