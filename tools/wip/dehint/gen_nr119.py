"""Attempt 12: comparisons with 0 get no opcode prediction, so `!ok` is the null return's 10%; `ok != 1` adds PRED_OPCODE_NONEQUAL against it: P(stay) about .78, stale J about 445, store under 97.
Post test spelling x post form x loop-side test spelling x select arm's stop."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gen_nr110 import HEAD, FOOT, FREE, LOGS, NLOGR, PRINT, SEL, RECV
from gen_nr117 import CALLOC, NL, LOGT, STORE

POSTT = {'!=1': ('ok != 1', 'ok == 1'), '!': ('!ok', 'ok'), '<1': ('ok < 1', 'ok >= 1')}
LOOPT = {'!': '!ok', '!=1': 'ok != 1'}
SELA = {
    'size': ('size = got;', 'got >= size', 'return NULL;'),
    'ok-ret': ('ok = 0;', '!ok', 'return NULL;'),
    'ok-ret1': ('ok = 0;', 'ok != 1', 'return NULL;'),
    'size-ok': ('size = got;\nok = 0;', 'got >= size', 'break;'),
    'ok-brk': ('ok = 0;', '!ok', 'break;'),
    'ok-brk1': ('ok = 0;', 'ok != 1', 'break;'),
}
RECA = {'brk': 'break;', 'ret': 'return NULL;'}
FORMS = {
    'ret': lambda t, nt: 'if (' + t + ')\n return NULL;\n' + NL + 'if (got == size) {\n' + STORE + '}\n' + NL + LOGT + FREE + 'return NULL;\n',
    'if': lambda t, nt: 'if (' + nt + ') {\n' + NL + 'if (got == size) {\n' + STORE + '}\n' + NL + LOGT + FREE + '}\nreturn NULL;\n',
}


def build(sa, lt, pt, rec, form):
    a_s, t_s, x_s = SELA[sa]
    inner = SEL + LOGS + FREE + a_s + '\n}\nif (' + t_s + ')\n' + x_s + '\n' + RECV + NLOGR + FREE + 'ok = 0;\n}\nif (' + LOOPT[lt] + ')\n' + RECA[rec] + '\n' + 'got += r;\n' + PRINT
    h = HEAD.replace('uint8_t *buf;', 'uint8_t *buf;\nint ok = 1;\n')
    t, nt = POSTT[pt]
    return h + CALLOC + 'got = 0;\nwhile (got < size) {\n' + inner + '}\n' + FORMS[form](t, nt) + '}\n' + FOOT


def variants():
    for sa in SELA:
        for lt in LOOPT:
            for pt in POSTT:
                for rec in RECA:
                    for form in FORMS:
                        if rec == 'ret' and 'brk' not in sa and sa != 'size-ok':
                            continue
                        yield '|'.join((sa, lt, pt, rec, form)), build(sa, lt, pt, rec, form)
