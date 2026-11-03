"""Attempt 11, family 4e: more arms for the helper's `!len`. With J 282 and g .869 only log 280-281 works (above 281 the tie or J's single-block trace gives the store priority; below 280 got's IRA cost drops a REG_FREQ step, margin -2). ne tail needs Q(len) .940-.943, eq tail .845-.848."""
import os, sys, itertools
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gen_nr105 as g
E = '(uint8_t *)&netEmpty'
F = 'free(buf);\n\t\t'
N = 'netFree(buf);\n\t\t'
L = g.L2
ARMS = {
 'log-buf': L + 'return buf;', 'free-null': F + 'return NULL;', 'free-const': F + 'return ' + E + ';', 'free-buf0': F + 'buf = NULL;\n\t\treturn buf;',
 'net-const': N + 'return ' + E + ';', 'net-buf0': N + 'buf = NULL;\n\t\treturn buf;',
 'log-free-null': L + F + 'return NULL;', 'log-net-null': L + N + 'return NULL;', 'log-net-const': L + N + 'return ' + E + ';', 'log-free-const': L + F + 'return ' + E + ';',
 'free-log-null': F + L + 'return NULL;', 'net-log-null': N + L + 'return NULL;', 'put-null': "putchar('" + g.BS + "n');\n\t\treturn NULL;", 'put-const': "putchar('" + g.BS + "n');\n\t\treturn " + E + ';',
 'vlog-null': g.NL1 + L + 'return NULL;', 'vlog-const': g.NL1 + L + 'return ' + E + ';', 'vlog-free': g.NL1 + L + g.FREE + 'return NULL;',
 'one': 'return (uint8_t *)1;', 'neg': 'return (uint8_t *)-1;', 'log-one': L + 'return (uint8_t *)-1;', 'exit': L + 'exit(1);', 'abort': 'abort();',
 'store0': 'return buf ? buf : NULL;', 'logbuf0': L + 'buf = NULL;\n\t\treturn buf;',
}
g.ARMS.update(ARMS)


def variants():
    for an, tl in itertools.product(ARMS, g.TAILS):
        yield an + '|' + tl, g.mk(an, 'not', 'afternl', tl, 'ifnot2')
