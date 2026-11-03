"""prepSysex with createSysexDirs behind a flag test (no guarded call on the mount success edge), mount failure as an early return."""
import itertools
from importlib import util
import os

here = os.path.dirname(os.path.abspath(__file__))


def load(n):
    s = util.spec_from_file_location(n, os.path.join(here, n + '.py'))
    m = util.module_from_spec(s)
    s.loader.exec_module(m)
    return m


g5, g6, g7 = load('gen_ca5'), load('gen_ca6'), load('gen_ca7')
F = g6.FMT
M = g6.MNT
NF = 'netFormatSysex()'
NM = 'netMount(SYSEX, "\\\\SEP")'
C = 'createSysexDirs()'
TAIL = {
    'a': 'if (r) r = ' + C + '; return r;',
    'b': 'return r ? ' + C + ' : 0;',
    'c': 'if (!r) return 0; return ' + C + ';',
    'd': 'if (r) return ' + C + '; return 0;',
    'e': 'if (!r) return r; return ' + C + ';',
    'f': 'if (r) return ' + C + '; return r;',
}
HEADS = {
    'h1': f'int r = 0; if ({NF}) {{ if (!{NM}) {{ {M} return 0; }} r = 1; }} else {F} ',
    'h4': f'int r = 1; if ({NF}) {{ if (!{NM}) {{ {M} return 0; }} }} else {{ {F} r = 0; }} ',
    'h5': f'int r = {NF}; if (r) {{ if (!{NM}) {{ {M} return 0; }} }} else {F} ',
    'h6': f'int r = {NF}; if (!r) {F} else if (!{NM}) {{ {M} return 0; }} ',
    'h7': f'int r = {NF}; if (!r) {F} else {{ r = {NM}; if (!r) {{ {M} return 0; }} }} ',
    'h8': f'int r = {NF}; if (r) {{ r = {NM}; if (!r) {{ {M} return r; }} }} else {F} ',
    'h9': f'int r = {NF}; if (r) {{ r = {NM}; if (!r) {{ {M} return 0; }} }} else {F} ',
    'h10': f'uint32_t r = {NF}; if (!r) {F} else {{ r = {NM}; if (!r) {{ {M} return 0; }} }} ',
    'h11': f'int r = 0; if ({NF}) {{ if ({NM}) r = 1; else {{ {M} return 0; }} }} else {F} ',
    'h12': f'int r; if ({NF}) {{ if (!{NM}) {{ {M} return 0; }} r = 1; }} else {{ {F} r = 0; }} ',
    'h13': f'int r = 0; if ({NF}) {{ r = {NM}; if (!r) {{ {M} return 0; }} }} else {F} ',
    'h14': f'int r = 0; if (!{NF}) {F} else {{ r = {NM}; if (!r) {{ {M} return 0; }} }} ',
}
BODIES = [('ifelse', 'and', 'gd1', 'ret_ge'), ('add', 'i_ret', 'wh', 'and_ge')]


def variants():
    for h, t, (bn, c, f, tt) in itertools.product(HEADS, TAIL, BODIES):
        body = 'uint32_t k = i;' + g5.send('k') + g5.INNER[bn]('k')
        loop = g5.FORMS[f] % {'c': g5.CONDS[c], 'b': body}
        tail = 'if (%s) {\n%s\n}' % (g7.T[tt], g5.MF)
        prep = 'int prepSysex(void)\n{\n' + HEADS[h] + TAIL[t] + '\n}\n'
        yield '%s%s|%s|%s|%s|%s' % (h, t, bn, c, f, tt), prep + g5.HEAD.replace('@LOOP@', loop).replace('@TAIL@', tail)
