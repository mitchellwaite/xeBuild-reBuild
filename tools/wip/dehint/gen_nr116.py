"""Attempt 12: gen_nr114's br/rb with a different test per arm. Left is the V latch cmp: the add's name comes from dce2's dead flag PHIs (vrp1 thread copies), so vary which flags and PHIs exist."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gen_nr110 import HEAD, FOOT, FREE, LOGS, NLOGR, PRINT, TAILCORE, SEL, RECV

CALLOC = 'buf = calloc(size, 1);\nif (verbose)\n printf("waiting for 0x%x bytes\\n", size);\n'
# arm kinds: (function-scope decl, body-scope decl, assignment, test)
KINDS = {
    'ok': ('int ok = 1;\n', '', 'ok = 0;', '!ok'),
    'okb': ('', 'int okb = 1;\n', 'okb = 0;', '!okb'),
    'failed': ('int failed = 0;\n', '', 'failed = 1;', 'failed'),
    'failb': ('', 'int failb = 0;\n', 'failb = 1;', 'failb'),
    'r': ('', '', 'r = SOCKET_ERROR;', 'r == SOCKET_ERROR'),
    'got': ('', '', 'got = size;', 'got >= size'),
    'size': ('', '', 'size = got;', 'got >= size'),
    'got=': ('', '', 'got = size;', 'got == size'),
    'none': ('', '', '', ''),
}
# what's tested after the loop: the break arm's flag
BREAK_OK = {'ok', 'failed', 'r'}


def build(ks, kr, xs, xr, extra=''):
    ds, bs, a_s, t_s = KINDS[ks]
    dr, br, a_r, t_r = KINDS[kr]
    decl = ds + (dr if dr != ds else '')
    body = bs + (br if br != bs else '')
    def ex(k, t, x):
        if k == 'none':
            return ''
        return 'if (' + t + ')\n' + ('break;' if x == 'b' else 'return NULL;') + '\n'
    def arm(k, a):
        return a + '\n' if k != 'none' else 'return NULL;\n'
    inner = body + SEL + LOGS + FREE + arm(ks, a_s) + extra + '}\n' + ex(ks, t_s, xs) + RECV + NLOGR + FREE + arm(kr, a_r) + '}\n' + ex(kr, t_r, xr) + 'got += r;\n' + PRINT
    h = HEAD.replace('uint8_t *buf;', 'uint8_t *buf;\n' + decl) if decl else HEAD
    tests = []
    if xs == 'b' and ks != 'none':
        tests.append(t_s)
    if xr == 'b' and kr != 'none' and t_r not in tests:
        tests.append(t_r)
    post = ('if (' + ' || '.join(tests) + ')\n return NULL;\n') if tests else ''
    return h + CALLOC + 'got = 0;\nwhile (got < size) {\n' + inner + '}\n' + post + TAILCORE + '}\n' + FOOT


def variants():
    for ks in KINDS:
        for kr in KINDS:
            for xs in 'br':
                for xr in 'br':
                    if ks == 'none' and kr == 'none':
                        continue
                    # a break arm needs a flag that the post-loop test can read
                    if xs == 'b' and ks not in BREAK_OK:
                        continue
                    if xr == 'b' and kr not in BREAK_OK:
                        continue
                    yield '|'.join((ks, kr, xs + xr)), build(ks, kr, xs, xr)
