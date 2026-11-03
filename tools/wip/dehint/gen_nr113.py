"""Attempt 12: simplifying gen_nr112's match (body-scoped ok, `if (!ok) return NULL;` after each arm, bottom `got >= size` break).
Where the free sits, the 4th exit's spelling and place, one flag or two, arm forms, other markers."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gen_nr110 import HEAD, FOOT, FREE, LOGS, NLOGR, PRINT, TAILCORE, SEL, RECV

CALLOC = 'buf = calloc(size, 1);\nif (verbose)\n printf("waiting for 0x%x bytes\\n", size);\n'
BOTS = {
    'ge': 'if (got >= size)\n break;\n',
    'eq': 'if (got == size)\n break;\n',
    'ltc': 'if (got < size)\n continue;\nbreak;\n',
    'none': '',
    'ifadd': None,
}
TESTS = {
    'ok': ('int ok = 1;\n', 'ok = 0;', '!ok'),
    'failed': ('int failed = 0;\n', 'failed = 1;', 'failed'),
    'bool': ('BOOL ok = TRUE;\n', 'ok = FALSE;', '!ok'),
    'u8': ('uint8_t ok = 1;\n', 'ok = 0;', '!ok'),
    'u32': ('uint32_t ok = 1;\n', 'ok = 0;', '!ok'),
}
FR = ('arm', 'exit', 'smix', 'rmix')  # free in the arm, or in the block after the exit test (both, or one arm)


def build(flag, fr, bot, armorder='log'):
    decl, a, t = TESTS[flag]
    fs = fr in ('exit', 'smix')
    frr = fr in ('exit', 'rmix')
    arm_s = LOGS + ('' if fs else FREE) + a + '\n'
    arm_r = NLOGR + ('' if frr else FREE) + a + '\n'
    if armorder == 'flagfirst':
        arm_s = a + '\n' + LOGS + ('' if fs else FREE)
        arm_r = a + '\n' + NLOGR + ('' if frr else FREE)
    ex_s = 'if (' + t + ') {\n' + (FREE if fs else '') + 'return NULL;\n}\n'
    ex_r = 'if (' + t + ') {\n' + (FREE if frr else '') + 'return NULL;\n}\n'
    b = BOTS[bot]
    if bot == 'ifadd':
        addp = 'got += r;\nif (verbose)\n printf("received 0x%08x of 0x%08x\\r", got, size);\nif (got >= size)\n break;\n'
    else:
        addp = 'got += r;\n' + PRINT + b
    inner = decl + SEL + arm_s + '}\n' + ex_s + RECV + arm_r + '}\n' + ex_r + addp
    return HEAD + CALLOC + 'got = 0;\nwhile (got < size) {\n' + inner + '}\n' + TAILCORE + '}\n' + FOOT


def variants():
    for flag in TESTS:
        for fr in FR:
            for bot in BOTS:
                for o in ('log', 'flagfirst'):
                    yield '|'.join((flag, fr, bot, o)), build(flag, fr, bot, o)
