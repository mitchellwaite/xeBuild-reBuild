"""Attempt 10: a test on len after *len = 0 (VRP folds it: non-null inferred from the store, after profile_estimate). Plain int size, no conversions. Exit arm x position, alone and in pairs."""
import itertools, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from nrflip import *
CAL = 'buf = calloc(size, 1);\n'
E = '(uint8_t *)&netEmpty'
ONE = {
 'null': 'if (!len) return NULL;\n\t\t',
 'buf': 'if (!len) return buf;\n\t\t',
 'empty': 'if (!len) return ' + E + ';\n\t\t',
 'free-null': 'if (!len) { free(buf); return NULL; }\n\t\t',
 'free-empty': 'if (!len) { free(buf); return ' + E + '; }\n\t\t',
 'neq-free': 'if (!len) { if (buf != ' + E + ') free(buf); return NULL; }\n\t\t',
 'log-null': 'if (!len) { log_printf(0, "received only %x of %x bytes! fail\\n", 0, size); return NULL; }\n\t\t',
 'log-free': 'if (!len) { log_printf(0, "received only %x of %x bytes! fail\\n", 0, size); free(buf); return NULL; }\n\t\t',
 'eq-null': 'if (len == NULL) return NULL;\n\t\t',
 'eq-buf': 'if (len == NULL) return buf;\n\t\t',
 'ne-buf': 'if (len != NULL) {\n',
 'one': 'if (!len) return (uint8_t *)1;\n\t\t',
}


def variants():
    for a in ONE:
        if a == 'ne-buf':
            continue
        yield a + '|calloc', rep(FLIP, (CAL, CAL + '\t\t' + ONE[a]))
        yield a + '|preloop', rep(FLIP, ('got = 0;\n', ONE[a] + 'got = 0;\n'))
    for a, b in itertools.permutations([k for k in ONE if k != 'ne-buf'], 2):
        yield a + '+' + b, rep(FLIP, (CAL, CAL + '\t\t' + ONE[a] + ONE[b]))
