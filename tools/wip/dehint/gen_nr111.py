"""Attempt 12: failure arm assigns and rejoins, then a separate exit test right after it, which threads away later.
So the arm has its own edge at profile_estimate and the loop exit keeps its 3%, so f2/f1 stays near .97 (gen_nr110's else forms have .73)."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gen_nr110 import HEAD, FOOT, FREE, LOGS, NLOGR, PRINT, TAILCORE, SEL, RECV

# name: decl, select arm's assignment, recv arm's assignment, exit test, post-loop test (for break)
MARKS = {
    'ok': ('int ok = 1;', 'ok = 0;', 'ok = 0;', '!ok', '!ok'),
    'fail': ('int failed = 0;', 'failed = 1;', 'failed = 1;', 'failed', 'failed'),
    'r': ('', 'r = SOCKET_ERROR;', '', 'r == SOCKET_ERROR', 'r == SOCKET_ERROR'),
    'got+ok': ('int ok = 1;', 'ok = 0; got = size;', 'ok = 0; got = size;', 'got >= size', '!ok'),
    'got+buf': ('', 'buf = NULL; got = size;', 'buf = NULL; got = size;', 'got >= size', '!buf'),
    'size+buf': ('', 'buf = NULL; size = got;', 'buf = NULL; size = got;', 'got >= size', '!buf'),
    'got==+buf': ('', 'buf = NULL; got = size;', 'buf = NULL; got = size;', 'got == size', '!buf'),
    'size==+buf': ('', 'buf = NULL; size = got;', 'buf = NULL; size = got;', 'got == size', '!buf'),
    'ok-size': ('int ok = 1;', 'ok = 0; size = got;', 'ok = 0; size = got;', 'got == size', '!ok'),
}
EXITS = ('break', 'return', 'cont')  # cont: continue back to the head test, not an exit


def build(mark, which, ex, bottom=''):
    decl, ms, mr, test, post = MARKS[mark]
    def arm(w, a):
        if w in which:
            return a + '\n'
        return 'return NULL;\n'
    def t(w):
        if w not in which:
            return ''
        return 'if (' + test + ')\n' + {'break': 'break;', 'return': 'return NULL;', 'cont': 'continue;'}[ex] + '\n'
    inner = (SEL + LOGS + FREE + arm('s', ms) + '}\n' + t('s') + RECV + NLOGR + FREE + arm('r', mr) + '}\n' + t('r') + 'got += r;\n' + PRINT + bottom)
    lp = 'got = 0;\nwhile (got < size) {\n' + inner + '}\n'
    h = HEAD.replace('uint8_t *buf;', 'uint8_t *buf;\n' + decl) if decl else HEAD
    p = '' if ex == 'return' else 'if (' + post + ')\n return NULL;\n'
    return h + 'buf = calloc(size, 1);\nif (verbose)\n printf("waiting for 0x%x bytes\\n", size);\n' + lp + p + TAILCORE + '}\n' + FOOT


def variants():
    for mn in MARKS:
        for which in ('s', 'r', 'sr'):
            for ex in EXITS:
                yield '|'.join((mn, which, ex)), build(mn, which, ex)
                yield '|'.join((mn, which, ex, 'bot')), build(mn, which, ex, 'if (got >= size)\n break;\n')
