"""netRecv alone: store inside the loop / break forms, nested while, guard spellings."""
import importlib.util, itertools, os
spec = importlib.util.spec_from_file_location('g3', os.path.join(os.path.dirname(os.path.abspath(__file__)), 'gen_nrs3.py'))
g = importlib.util.module_from_spec(spec)
spec.loader.exec_module(g)
F = g.F
FAIL = g.LOG + '\n' + F + '\nreturn NULL;'
OK = '*len = size;\nreturn buf;'
STORE = 'if (got == size) {\n' + OK + '\n}\n'


def shapes(sel):
    body = g.SEL[sel] + '\n' + g.RECV + '\n'
    yield 'in_eq', 'got = 0;\nwhile (got < size) {\n' + body + 'got += r;\n' + STORE + '}\n' + FAIL
    yield 'in_ge', 'got = 0;\nwhile (got < size) {\n' + body + 'got += r;\nif (got >= size) {\n' + STORE + 'break;\n}\n}\n' + FAIL
    yield 'in_for', 'for (got = 0; got < size; ) {\n' + body + 'got += r;\n' + STORE + '}\n' + FAIL
    yield 'in_do', 'got = 0;\nif (size > 0) do {\n' + body + 'got += r;\n' + STORE + '} while (got < size);\n' + FAIL
    yield 'in_do2', 'got = 0;\nif (size > 0) {\nfor (;;) {\n' + body + 'got += r;\nif (got >= size)\nbreak;\n}\n' + STORE + '}\n' + FAIL
    yield 'nest_while', 'got = 0;\nif (size > 0) {\nwhile (got < size) {\n' + body + 'got += r;\n}\n' + STORE + '}\n' + FAIL
    yield 'while_else', 'got = 0;\nwhile (got < size) {\n' + body + 'got += r;\n}\n' + 'if (got == size && size > 0) {\n' + OK + '\n}\n' + FAIL
    yield 'while_gt', 'got = 0;\nwhile (got < size) {\n' + body + 'got += r;\n}\n' + 'if (size > 0 && got == size) {\n' + OK + '\n}\n' + FAIL
    yield 'do_and', 'got = 0;\nif (size > 0) do {\n' + body + 'got += r;\n} while (got < size);\n' + 'if (size > 0 && got == size) {\n' + OK + '\n}\n' + FAIL
    yield 'do_and2', 'got = 0;\nif (size > 0) do {\n' + body + 'got += r;\n} while (got < size);\n' + 'if (got == size && size > 0) {\n' + OK + '\n}\n' + FAIL
    yield 'wh_ge', 'got = 0;\nwhile (got < size) {\n' + body + 'got += r;\n}\n' + 'if (got > 0 && got == size) {\n' + OK + '\n}\n' + FAIL
    yield 'wh_got', 'got = 0;\nwhile (got < size) {\n' + body + 'got += r;\n}\n' + 'if (got && got == size) {\n' + OK + '\n}\n' + FAIL


def variants():
    for sel, dc in itertools.product(['pl', 'side'], ['sgr']):
        for tag, code in shapes(sel):
            yield '|'.join((tag, sel, dc)), g.HEAD.replace('DECLS', g.DECL[dc]).replace('HSEL', g.HSEL['pl']).replace('HRECV', g.HRECV['pl']) + code + '\n}\n'
