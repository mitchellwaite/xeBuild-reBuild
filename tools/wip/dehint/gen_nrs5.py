"""netRecv alone: the size <= 0 path skips the got == size test (nested or goto), so `store` no longer gets its share."""
import importlib.util, itertools, os
spec = importlib.util.spec_from_file_location('g3', os.path.join(os.path.dirname(os.path.abspath(__file__)), 'gen_nrs3.py'))
g = importlib.util.module_from_spec(spec)
spec.loader.exec_module(g)
F = g.F
STORE = 'if (got == size) {\n*len = size;\nreturn buf;\n}\n'
NE = 'if (got != size)\ngoto fail;\n*len = size;\nreturn buf;\n'
FAIL = g.LOG + '\n' + F + '\nreturn NULL;'


def shapes(sel):
    body = g.SEL[sel] + '\n' + g.RECV + '\n'
    yield 'nest_do', 'got = 0;\nif (size > 0) {\ndo {\n' + body + 'got += r;\n} while (got < size);\n' + STORE + '}\n' + FAIL
    yield 'nest_while', 'got = 0;\nif (size > 0) {\nwhile (got < size) {\n' + body + 'got += r;\n}\n' + STORE + '}\n' + FAIL
    yield 'goto_do', 'got = 0;\nif (size <= 0)\ngoto fail;\ndo {\n' + body + 'got += r;\n} while (got < size);\n' + STORE + 'fail:\n' + FAIL
    yield 'goto_do2', 'got = 0;\nif (size <= 0)\ngoto fail;\ndo {\n' + body + 'got += r;\n} while (got < size);\n' + NE + 'fail:\n' + FAIL
    yield 'goto_while', 'got = 0;\nif (size <= 0)\ngoto fail;\nwhile (got < size) {\n' + body + 'got += r;\n}\n' + STORE + 'fail:\n' + FAIL
    yield 'goto_for', 'got = 0;\nif (size > 0) {\nfor (;;) {\n' + body + 'got += r;\nif (got >= size)\nbreak;\n}\n' + STORE + '}\n' + FAIL


def variants():
    for sel, dc in itertools.product(g.SEL, g.DECL):
        for tag, code in shapes(sel):
            yield '|'.join((tag, sel, dc)), g.HEAD.replace('DECLS', g.DECL[dc]).replace('HSEL', g.HSEL['pl']).replace('HRECV', g.HRECV['pl']) + code + '\n}\n'
