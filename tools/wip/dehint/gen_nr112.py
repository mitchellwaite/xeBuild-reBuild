"""Attempt 12: gen_nr111 ok|sr with test spellings. Left in that shape: cmp order of the verbose latch (SSA numbering), so spellings and scopes of the flag and compares."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gen_nr110 import HEAD, FOOT, FREE, LOGS, NLOGR, PRINT, TAILCORE, SEL, RECV

SCOPES = {
    'decl': ('int ok = 1;', '', ''),
    'pre': ('int ok;', 'ok = 1;\n', ''),
    'body': ('', '', 'int ok = 1;\n'),
}
FLAGS = {'ok': ('ok = 0;', '!ok'), 'ok==0': ('ok = 0;', 'ok == 0')}
HEADS = ('got < size', 'size > got')
BOTS = {'none': '', 'ge': 'if (got >= size)\n break;\n', 'le': 'if (size <= got)\n break;\n', 'nlt': 'if (!(got < size))\n break;\n'}
ORDER = ('ap', 'pa')  # got += r before or after the print (with got + r)
LOOPS = ('while', 'for', 'for2', 'wh1', 'do')


def build(scope, flag, head, bot, ex, loop, tailsw):
    decl, pre, body = SCOPES[scope]
    a, t = FLAGS[flag]
    x = 'if (' + t + ')\n' + {'return': 'return NULL;', 'break': 'break;'}[ex] + '\n'
    inner = (body + SEL + LOGS + FREE + a + '\n}\n' + x + RECV + NLOGR + FREE + a + '\n}\n' + x + 'got += r;\n' + PRINT)
    if loop == 'while':
        lp = 'got = 0;\n' + pre + 'while (' + head + ') {\n' + inner + BOTS[bot] + '}\n'
    elif loop == 'for':
        lp = pre + 'for (got = 0; ' + head + ';) {\n' + inner + BOTS[bot] + '}\n'
    elif loop == 'for2':
        lp = pre + 'got = 0;\nfor (; ' + head + ';) {\n' + inner + BOTS[bot] + '}\n'
    elif loop == 'wh1':
        lp = 'got = 0;\n' + pre + 'if (size > 0)\nfor (;;) {\n' + inner + (BOTS[bot] or 'if (got >= size)\n break;\n') + '}\n'
    else:
        lp = 'got = 0;\n' + pre + 'if (size > 0)\ndo {\n' + inner + BOTS[bot] + '} while (' + head + ');\n'
    tail = TAILCORE
    if tailsw:
        tail = tail.replace('got == size', 'size == got')
    h = HEAD.replace('uint8_t *buf;', 'uint8_t *buf;\n' + decl) if decl else HEAD
    p = ''
    if ex != 'return':
        if scope == 'body':
            return None
        p = 'if (' + t + ')\n return NULL;\n'
    return h + 'buf = calloc(size, 1);\nif (verbose)\n printf("waiting for 0x%x bytes\\n", size);\n' + lp + p + tail + '}\n' + FOOT


def variants():
    for scope in SCOPES:
        for flag in FLAGS:
            for head in HEADS:
                for bot in BOTS:
                    for ex in ('return', 'break'):
                        for loop in LOOPS:
                            for ts in (0, 1):
                                s = build(scope, flag, head, bot, ex, loop, ts)
                                if s:
                                    yield '|'.join((scope, flag, head.replace(' ', ''), bot, ex, loop, str(ts))), s
