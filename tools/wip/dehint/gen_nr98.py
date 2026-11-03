"""Attempt 10: looking for the most natural spelling of the folded test after the calloc. Test x arm, single test, plain types; len/size/r tests; rejoining tests (expected to do nothing)."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from nrflip import *
CAL = 'buf = calloc(size, 1);\n'
E = '(uint8_t *)&netEmpty'
NEQ = 'if (buf != ' + E + ') free(buf);'
TESTS = {
 'nolen': '!len', 'len0': 'len == NULL', 'len00': 'len == 0',
 'z': '!size', 'm1': 'size == -1', 'r0': 'r == 0', 'rm1': 'r == SOCKET_ERROR', 'r0m1': 'r == SOCKET_ERROR || r == 0', 'r0m1v': 'r <= 0 && r >= -1',
 'z|m1': 'size == 0 || size == -1', 'nolen|z': '!len || !size', 'z|nolen': '!size || !len',
}
ARMS = {
 'neq': NEQ + ' return NULL;',
 'neq-buf0': NEQ + ' buf = NULL; return buf;',
 'netfree': 'netFree(buf); return NULL;',
 'neq-log': 'log_printf(0, "unable to fetch first 4 bytes, %d\\n", 0); ' + NEQ + ' return NULL;',
 'neq-err': NEQ + ' return (uint8_t *)NULL;',
 'neq-empty': NEQ + ' return ' + E + ';',
}
REJOIN = {
 'store': ('*len = size;', 'if (len) *len = size;'),
 'zero': ('*len = 0;\n\treturn (uint8_t *)&netEmpty;', 'if (len) *len = 0;\n\treturn (uint8_t *)&netEmpty;'),
}


def variants():
    for tn, t in TESTS.items():
        for an, a in ARMS.items():
            yield tn + '|' + an, rep(FLIP, (CAL, CAL + '\t\tif (' + t + ') { ' + a + ' }\n'))
    for n, (a, b) in REJOIN.items():
        yield 'rejoin|' + n, rep(FLIP, (a, b))
        # with the matching test too
        yield 'rejoin+nolen|' + n, rep(FLIP, (a, b), (CAL, CAL + '\t\tif (!len) { ' + NEQ + ' return NULL; }\n'))
