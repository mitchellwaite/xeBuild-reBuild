"""loadBl from gen_bd138's best (build/bd/a5/lb2.c), every subset of the old hints back in: which are still needed, and for what."""
import itertools

BASE = 'build/bd/a5/lb2.c'


def t10(t):
    return t.replace('} else if (type == 10) {\nif (!suGetCG', '} else if (__builtin_expect(type == 10, 0)) {\nif (!suGetCG')


def bad(t):
    return t.replace('log_printf(1, "\\n\\n***** ERROR: patch size', 'badsize: __attribute__((hot));\nlog_printf(1, "\\n\\n***** ERROR: patch size', 1)


def pind(t):
    return t.replace('uint8_t *d = xb.files[xb.nFlashFiles].data;\n\n\t\t\t\n', 'uint8_t *d = xb.files[xb.nFlashFiles].data;\n\n__asm__("" : "+a"(d));\n', 1)


def cp(t):
    t = t.replace('*pr = checkBl(e->data, e->size, type, e->crc);\nif (!*pr) {', 'chk:\n*pr = checkBl(e->data, e->size, type, e->crc);\nif (!*pr) {', 1)
    return t.replace('log_printf(1, "####### unhandled bl load %d %s\\n", type, e->name);\n', 'log_printf(1, "####### unhandled bl load %d %s\\n", type, e->name);\nif ((char *)__builtin_constant_p(i) == (char *)1 && (char *)__builtin_constant_p(type) == (char *)1) {\ntype = (type & 1) + 18;\ngoto chk;\n}\n', 1)


def fail(t):
    t = t.replace('e->size);\n*pr = -1;\nbreak;\n', 'e->size);\ngoto fail;\n', 1)
    t = t.replace('if (!e->offset)\n*pr = -1;\n', 'if (!e->offset)\ngoto fail;\n', 1)
    i = t.index('int loadBlFiles(void)\n{')
    k = t.rindex('\treturn;\n}\n', 0, i)
    return t[:k] + '\treturn;\nfail:\n\t__asm__ __volatile__("");\n\t*pr = -1;\n}\n' + t[k + 11:]


def t5(t):
    return t.replace('if (xb.type <= BUILD_DEVGL16)\nbreak;\nif (type == 14)', 'if (xb.type <= BUILD_DEVGL16) {\nt5le: __attribute__((hot));\nbreak;\n}\nif (type == 14)', 1)


H = {'t10': t10, 'bad': bad, 'pind': pind, 'cp': cp, 'fail': fail, 't5': t5}


def CASES(base):
    out = []
    names = list(H)
    for n in range(len(names) + 1):
        for s in itertools.combinations(names, n):
            t = base
            for x in s:
                t = H[x](t)
            out.append((','.join(s) or 'none', t))
    return out
