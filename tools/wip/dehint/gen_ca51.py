"""Attempt 4: gen_ca50's arms swap because the manifest block (5) is under bbro's round 3 threshold (10), so it pops in round 4
and extends into its failure arm. Spellings of the dead test that change its prediction: <= 0 (opcode positive), != 1, types."""
import itertools, os
from importlib import util

here = os.path.dirname(os.path.abspath(__file__))


def load(n):
    s = util.spec_from_file_location(n, os.path.join(here, n + '.py'))
    m = util.module_from_spec(s)
    s.loader.exec_module(m)
    return m


g, g45 = load('gen_ca30'), load('gen_ca45')
ITEMS, S, T, ENDS = g45.ITEMS, g45.S, g45.T, g45.ENDS
ITEMS = {k: ITEMS[k] for k in ('cast', 'k')}
ENDS = {'brk0': ENDS['brk0']}
OK = {'!': ('!ok', 'ok'), 'le': ('ok <= 0', 'ok > 0'), 'lt1': ('ok < 1', 'ok >= 1'), 'ne1': ('ok != 1', 'ok == 1'), 'eq0': ('ok == 0', 'ok != 0')}
TYPES = {'int': 'int', 'long': 'long', 'u32': 'uint32_t'}
HEADS = {
    'td': 'if (i >= n) {\n' + T + 'if (@D@)\ngoto out;\n@S@}\n' + T,
    'dt': 'if (i >= n) {\nif (@D@)\ngoto out;\n' + T + '@S@}\n' + T,
    'or': 'if (i >= n) {\nif (!ret || @D@)\ngoto out;\n@S@}\n' + T,
    'ro': 'if (i >= n) {\nif (@D@ || !ret)\ngoto out;\n@S@}\n' + T,
    'and': 'if (i >= n) {\nif (ret && @P@) {\n@S@}\ngoto out;\n}\n' + T,
    'dna': 'if (i >= n) {\nif (@P@ && ret) {\n@S@}\ngoto out;\n}\n' + T,
    'nest': 'if (i >= n) {\nif (ret) {\nif (@D@)\ngoto out;\n@S@}\ngoto out;\n}\n' + T,
    'nest2': 'if (i >= n) {\nif (@P@) {\nif (!ret)\ngoto out;\n@S@}\ngoto out;\n}\n' + T,
    'else': 'if (i >= n) {\nif (!ret)\ngoto out;\nif (@D@)\ngoto out;\nelse {\n@S@}\n}\n' + T,
}
BOT = {
    'okN': 'ok = ret != 0;\nn = manifest.count;\ni += ok;\nif (!ret)\n%(f)s\n',
    'okNr': 'ok = ret != 0;\nn = manifest.count;\ni += ret != 0;\nif (!ret)\n%(f)s\n',
}


def variants():
    for it, ty, o, h, b, en in itertools.product(ITEMS, TYPES, OK, HEADS, BOT, ENDS):
        if ty == 'u32' and o in ('le', 'lt1'):
            pass
        v, decl, d = ITEMS[it]
        head = HEADS[h].replace('@S@', S).replace('@D@', OK[o][0]).replace('@P@', OK[o][1])
        body = decl + g.LOG % v + '\n' + g.SEND % v + '\n' + BOT[b] % {'f': g.FAIL % v}
        loop = 'i = 0;\nn = manifest.count;\nok = 1;\nfor (;;) {\n' + head + body + '}\n'
        src = g.PREP + g.FRAME.replace('@DECL@', '\tint sent, n;\n\t' + TYPES[ty] + ' ok;\n' + d).replace('@LOOP@', loop).replace('@TAIL@', ENDS[en]).replace('@OUT@', 'out:')
        yield '|'.join((it, ty, o, h, b, en)), src
