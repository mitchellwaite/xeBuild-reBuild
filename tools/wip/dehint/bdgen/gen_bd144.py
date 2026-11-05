"""lb6: subsets of the old hints on top of it (pin and shared fail are in lb6 already; they can come off)."""
import itertools, re

BASE = 'build/bd/a5/lb6.c'


def t10(t):
    return t.replace('} else if (type == 10) {\nif (!suGetCG', '} else if (__builtin_expect(type == 10, 0)) {\nif (!suGetCG')


def bad(t):
    return t.replace('log_printf(1, "\\n\\n***** ERROR: patch size', 'badsize: __attribute__((hot));\nlog_printf(1, "\\n\\n***** ERROR: patch size', 1)


def cp(t):
    return t.replace('log_printf(1, "####### unhandled bl load %d %s\\n", type, e->name);\n', 'log_printf(1, "####### unhandled bl load %d %s\\n", type, e->name);\nif ((char *)__builtin_constant_p(i) == (char *)1 && (char *)__builtin_constant_p(type) == (char *)1) {\ntype = (type & 1) + 18;\ngoto chk;\n}\n', 1)


def t5(t):
    return t.replace('if (xb.type <= BUILD_DEVGL16)\nbreak;\nif (type == 14)', 'if (xb.type <= BUILD_DEVGL16) {\nt5le: __attribute__((hot));\nbreak;\n}\nif (type == 14)', 1)


def pr(t):
    return t.replace('if (xb.type <= BUILD_DEVGL16)\nbreak;\nif (type == 14)', 'if (xb.type <= BUILD_DEVGL16) {\nif (__builtin_expect(*pr != 0, 0))\ngoto fail;\nbreak;\n}\nif (type == 14)', 1)


def pr5(t):
    return t.replace('if (xb.type <= BUILD_DEVGL16)\nbreak;\nif (type == 14)', 'if (xb.type <= BUILD_DEVGL16) {\nt5le: __attribute__((hot));\nif (__builtin_expect(*pr != 0, 0))\ngoto fail;\nbreak;\n}\nif (type == 14)', 1)


def nopin(t):
    return t.replace('__asm__("" : "+a"(d));\n', '\n')


H = {'t10': t10, 'bad': bad, 'cp': cp, 'nopin': nopin}
TAIL = {'le': None, 't5': t5, 'pr': pr, 'pr5': pr5}


def CASES(base):
    out = []
    names = list(H)
    for n in range(len(names) + 1):
        for s in itertools.combinations(names, n):
            for k, f in TAIL.items():
                t = base
                for x in s:
                    t = H[x](t)
                if f:
                    t = f(t)
                out.append((','.join(s + (k,)), t))
    return out
