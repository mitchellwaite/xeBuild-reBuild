"""loadBl from build/bd/a5/lb4.c: forms of the CF/CG fallback, which decide whether the CG path's checkBl shares CF's."""
import itertools

BASE = 'build/bd/a5/lb4.c'
OLD = '''if (*pr) {
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
if (*pr)
break;
'''
CHK = '*pr = checkBl(e->data, e->size, type, e->crc);\nif (!*pr) {\nif (type == 5'
F = {
    'g1': ('if (*pr) {\nif (type == 9) {\nif (!suGetCF(&e->data, &e->size))\nbreak;\n} else if (type == 10) {\nif (!suGetCG(&e->data, &e->size))\nbreak;\ngoto chk;\n} else\nbreak;\n}\n', 1),
    'g2': ('if (*pr) {\nif (type == 9) {\nif (!suGetCF(&e->data, &e->size))\nbreak;\n} else if (type == 10) {\nif (!suGetCG(&e->data, &e->size))\nbreak;\n} else\nbreak;\n}\n', 0),
    'g3': ('if (*pr) {\nif (type == 9) {\nif (!suGetCF(&e->data, &e->size))\nbreak;\n} else if (type == 10) {\nif (!suGetCG(&e->data, &e->size))\nbreak;\n*pr = 0;\ngoto chk;\n} else\nbreak;\n*pr = 0;\n}\n', 1),
    'g4': ('if (*pr) {\nif (type == 9) {\nif (!suGetCF(&e->data, &e->size))\nbreak;\n} else if (type == 10) {\nif (!suGetCG(&e->data, &e->size))\nbreak;\n} else\nbreak;\n*pr = 0;\n}\n', 0),
    'g5': ('if (*pr && type != 9 && type != 10)\nbreak;\nif (*pr && type == 9 && !suGetCF(&e->data, &e->size))\nbreak;\nif (*pr && type == 10 && !suGetCG(&e->data, &e->size))\nbreak;\n', 0),
    'g6': ('if (*pr) {\nif (type != 9 && type != 10)\nbreak;\nif (type == 9) {\nif (!suGetCF(&e->data, &e->size))\nbreak;\n} else {\nif (!suGetCG(&e->data, &e->size))\nbreak;\n}\n}\n', 0),
    'g7': ('if (*pr) {\nif (type == 10) {\nif (!suGetCG(&e->data, &e->size))\nbreak;\n} else if (type == 9) {\nif (!suGetCF(&e->data, &e->size))\nbreak;\n} else\nbreak;\n}\n', 0),
    'g8': ('if (*pr) {\nif (type == 9) {\nif (!suGetCF(&e->data, &e->size))\nbreak;\n} else if (type != 10 || !suGetCG(&e->data, &e->size))\nbreak;\n}\n', 0),
    'g9': ('if (*pr) {\nif (type == 9) {\nif (!suGetCF(&e->data, &e->size))\nbreak;\n} else {\nif (type != 10)\nbreak;\nif (!suGetCG(&e->data, &e->size))\nbreak;\n}\n}\n', 0),
}


def CASES(base):
    out = []
    for f, t10 in itertools.product(F, (0, 1)):
        s, lab = F[f]
        if t10:
            s = s.replace('else if (type == 10) {', 'else if (__builtin_expect(type == 10, 0)) {')
        t = base.replace(OLD, s)
        if lab:
            t = t.replace(CHK, 'chk:\n' + CHK, 1)
        out.append(('%s t10=%d' % (f, t10), t))
    return out
