"""More prepSysex spellings looking for P(mount ok) ~ 80%, on two guard-correct bodies."""
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
PREPS = {
    'g1': f'if (!{NF}) {{ {F} goto fail; }} if (!{NM}) {{ {M} goto fail; }} return {C}; fail: return 0;',
    'g2': f'if ({NF}) {{ if ({NM}) return {C}; {M} goto fail; }} else {F} fail: return 0;',
    'g3': f'if ({NF}) {{ if (!{NM}) {{ {M} goto fail; }} return {C}; }} {F} fail: return 0;',
    'g4': f'if ({NF}) {{ if ({NM}) goto mounted; {M} }} else {F} return 0; mounted: return {C};',
    'g5': f'if (!{NF}) {{ {F} return 0; }} if ({NM}) return {C}; {M} return 0;',
    'g6': f'int r = 0; if ({NF}) {{ r = {NM}; if (!r) {M} else r = {C}; }} else {F} return r;',
    'g7': f'int r = {NF}; if (!r) {F} else {{ r = {NM}; if (!r) {M} else r = {C}; }} return r;',
    'g8': f'int r = {NF}; if (r) {{ r = {NM}; if (r) return {C}; {M} return 0; }} {F} return 0;',
    'g9': f'int r = {NF}; if (!r) {{ {F} return r; }} r = {NM}; if (!r) {{ {M} return r; }} return {C};',
    'g10': f'if ({NF}) {{ uint32_t m = {NM}; if (!m) {M} if (m) return {C}; }} else {F} return 0;',
    'g11': f'if ({NF}) {{ uint32_t m = {NM}; if (m) return {C}; {M} return m; }} {F} return 0;',
    'g13': f'if ({NF}) {{ if ({NM}) return {C}; else {{ {M} return 0; }} }} else {{ {F} return 0; }}',
    'g14': f'if ({NF}) {{ if (!{NM}) {{ {M} return 0; }} else return {C}; }} else {{ {F} return 0; }}',
    'g15': f'do {{ if (!{NF}) {{ {F} break; }} if (!{NM}) {{ {M} break; }} return {C}; }} while (0); return 0;',
    'g16': f'if ({NF}) {{ if (!{NM}) {{ {M} return 0; }} }} else {{ {F} return 0; }} return {C};',
    'g17': f'if ({NF}) {{ if ({NM}) {{ }} else {{ {M} return 0; }} }} else {{ {F} return 0; }} return {C};',
    'g18': f'int r; if ({NF}) {{ if (!{NM}) {{ {M} return 0; }} r = {C}; }} else {{ {F} r = 0; }} return r;',
    'g19': f'int r = 0; if ({NF}) {{ if (!{NM}) {{ {M} return 0; }} r = {C}; }} else {F} return r;',
    'g20': f'int r = 0; if (!{NF}) {F} else {{ if (!{NM}) {{ {M} return 0; }} r = {C}; }} return r;',
    'g21': f'int r = 0; if ({NF}) {{ if ({NM}) r = 1; else {M} }} else {F} if (r) r = {C}; return r;',
    'g22': f'int r = 0; if ({NF}) {{ if ({NM}) r = 1; else {M} }} else {F} if (!r) return 0; return {C};',
    'g23': f'int r = 0; if ({NF}) {{ if (!{NM}) {{ {M} }} else r = 1; }} else {F} return r ? {C} : 0;',
    'g24': f'if ({NF}) {{ if ({NM}) r1: return {C}; {M} return 0; }} {F} return 0;',
    'g25': f'if ({NF}) {{ if ({NM} == 0) {{ {M} return 0; }} }} else {{ {F} return 0; }} if ({C}) return 1; return 0;',
    'g26': f'if ({NF}) {{ if ({NM}) {{ if ({C}) return 1; return 0; }} {M} return 0; }} {F} return 0;',
    'g27': f'if ({NF}) {{ if ({NM}) return {C} != 0; {M} }} else {F} return 0;',
    'g28': f'if ({NF}) {{ if (!{NM}) {{ {M} return 0; }} if (!{C}) return 0; return 1; }} {F} return 0;',
    'g29': f'if (!{NF}) {F} else if ({NM}) {{ if ({C}) return 1; }} else {M} return 0;',
}
BODIES = [('ifelse', 'and', 'gd1', 'ret_ge'), ('add', 'i_ret', 'wh', 'and_ge')]


def variants():
    for p, (bn, c, f, t) in itertools.product(PREPS, BODIES):
        body = 'uint32_t k = i;' + g5.send('k') + g5.INNER[bn]('k')
        loop = g5.FORMS[f] % {'c': g5.CONDS[c], 'b': body}
        tail = 'if (%s) {\n%s\n}' % (g7.T[t], g5.MF)
        prep = 'int prepSysex(void)\n{\n' + PREPS[p] + '\n}\n'
        yield '%s|%s|%s|%s|%s' % (p, bn, c, f, t), prep + g5.HEAD.replace('@LOOP@', loop).replace('@TAIL@', tail)
