"""netRecv alone: size <= 0 skips the got == size test AND the failure return isn't the function's last, so it counts as an early return."""
import importlib.util, itertools, os
spec = importlib.util.spec_from_file_location('g3', os.path.join(os.path.dirname(os.path.abspath(__file__)), 'gen_nrs3.py'))
g = importlib.util.module_from_spec(spec)
spec.loader.exec_module(g)
F = g.F
FAIL = g.LOG + '\n' + F + '\nreturn NULL;'
OK = '*len = size;\nreturn buf;'


def shapes(sel):
    body = g.SEL[sel] + '\n' + g.RECV + '\n'
    do = 'do {\n' + body + 'got += r;\n} while (got < size);\n'
    wh = 'while (got < size) {\n' + body + 'got += r;\n}\n'
    yield 'goto_ok', 'got = 0;\nif (size > 0) {\n' + do + 'if (got == size)\ngoto ok;\n}\n' + FAIL + '\nok:\n' + OK
    yield 'goto_fail_in', 'got = 0;\nif (size <= 0)\ngoto fail;\n' + do + 'if (got != size) {\nfail:\n' + FAIL + '\n}\n' + OK
    yield 'wh_goto_ok', 'got = 0;\nif (size > 0) {\n' + wh + 'if (got == size)\ngoto ok;\n}\n' + FAIL + '\nok:\n' + OK
    yield 'or', 'got = 0;\nif (size > 0)\n' + do + 'if (size <= 0 || got != size) {\n' + FAIL + '\n}\n' + OK
    yield 'or2', 'got = 0;\nif (size > 0)\n' + do + 'if (got != size || size <= 0) {\n' + FAIL + '\n}\n' + OK
    yield 'ne', 'got = 0;\nif (size > 0)\n' + do + 'if (got != size) {\n' + FAIL + '\n}\n' + OK
    yield 'wh_ne', 'got = 0;\n' + wh + 'if (got != size) {\n' + FAIL + '\n}\n' + OK


def variants():
    for sel, dc in itertools.product(['pl', 'side'], ['sgr', 'u']):
        for tag, code in shapes(sel):
            yield '|'.join((tag, sel, dc)), g.HEAD.replace('DECLS', g.DECL[dc]).replace('HSEL', g.HSEL['pl']).replace('HRECV', g.HRECV['pl']) + code + '\n}\n'
