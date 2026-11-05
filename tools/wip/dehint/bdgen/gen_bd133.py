"""loadBl written in loadBlFiles' loop, as loadConsoleBlFiles' switch is, with r in place of *pr.  One hint set at a time."""
import itertools, re


def inline(base, fail='block'):
    a = base.index('/* load the input file e (xb.files[i]) by its type */')
    b = base.index('int loadBlFiles(void)\n{')
    c = base.index('int loadConsoleBlFiles(void)\n{')
    body = base[a:b]
    sw = body[body.index('\ttype = e->type;'):body.index('\treturn;\n')]
    sw = sw.replace('*pr', 'r')
    sw = sw.replace('goto fail;', 'goto fail;')
    sw = ''.join('\t\t' + l + '\n' if l else '\n' for l in sw.split('\n')[:-1])
    # labels keep their own indentation
    f = 'int loadBlFiles(void)\n{\n\tstruct fileent *e;\n\tuint32_t i;\n\tuint32_t r;\n\n\tfor (i = 1; i < (uint32_t)xb.nFiles; i++) {\n\t\te = &xb.files[i];\n\t\tr = 0;\n\t\tif (strnicmp(e->name, "none", 4) || e->crc) {\n\t\t\tint type;\n\n'
    f += ''.join('\t' + l + '\n' if l else '\n' for l in sw.split('\n')[:-1])
    if fail == 'block':
        f += '\t\t\tif (0) {\nfail:\n\t\t\t\t__asm__ __volatile__("");\n\t\t\t\tr = -1;\n\t\t\t}\n'
    f += '\t\t}\n\t\tif (r) {\n\t\t\tlog_printf(0, "\\n\\n**** could not read %s (%i) ****\\n\\n", e->name, r);\n\t\t\treturn -1;\n\t\t}\n\t}\n\treturn 0;\n}\n\n'
    return base[:a] + f + base[c:]


def dropfail(t):
    return t.replace('goto fail;', 'r = -1;\nbreak;', 3)


def CASES(base):
    t = inline(base)
    out = [('inline all hints', t)]
    return out + [
        ('noexpr', t.replace('__builtin_expect(r != 0, 0)', 'r != 0')),
        ('nolab', t.replace('t5le: __attribute__((hot));\n', '\n')),
        ('nolabexpr', t.replace('t5le: __attribute__((hot));\n', '\n').replace('__builtin_expect(r != 0, 0)', 'r != 0')),
        ('nobad', t.replace('badsize: __attribute__((hot));\n', '\n')),
        ('no10', t.replace('__builtin_expect(type == 10, 0)', 'type == 10')),
        ('nopin', t.replace('__asm__("" : "+a"(d));\n', '\n')),
    ]
