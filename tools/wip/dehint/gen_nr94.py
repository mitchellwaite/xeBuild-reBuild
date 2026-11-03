"""Attempt 10, MODEL CHECK: a test on the converted name that VRP folds after profile_estimate, inside the flip's arm, before the calloc. The pre-loop block keeps the test's freq (stale).
Measures the margin and layout for each predicted P. These are dead tests: not shapes to land as they stand."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from nrflip import *
GET = 'size = getBeU32(hdr);\n\tif (size == -1)\n\t\treturn NULL;\n\tif (size) {\n\t\tbuf = calloc(size, 1);\n'
DECL = 'int size, got, r;'
Z0 = '*len = 0;\n\t\t\treturn (uint8_t *)&netEmpty;'
TESTS = {
 'none': '',
 'z-null': 'if (!size)\n\t\t\treturn NULL;\n',
 'z-empty': 'if (!size) {\n\t\t\t' + Z0 + '\n\t\t}\n',
 'z-zero': 'if (size == 0)\n\t\t\treturn 0;\n',
 'nz-nest': None,
 'm1-null': 'if (size == -1)\n\t\t\treturn NULL;\n',
 'm1-empty': 'if (size == -1) {\n\t\t\t' + Z0 + '\n\t\t}\n',
 'm1-log': 'if (size == -1) {\n\t\t\tlog_printf(0, "unable to fetch first 4 bytes, %d\\n", size);\n\t\t\treturn NULL;\n\t\t}\n',
 'z-log': 'if (!size) {\n\t\t\tlog_printf(0, "unable to fetch first 4 bytes, %d\\n", size);\n\t\t\treturn NULL;\n\t\t}\n',
 'z-free': 'if (!size) {\n\t\t\tfree(hdr);\n\t\t\treturn NULL;\n\t\t}\n',
}
HEADN = 'n = getBeU32(hdr);\n\tif (n == 0xffffffff)\n\t\treturn NULL;\n\tif (n) {\n\t\tsize = n;\n'
POS = ('before', 'after')  # before or after the calloc


def variants():
    for tn, t in TESTS.items():
        if t is None:
            continue
        for pos in POS:
            if pos == 'before':
                body = HEADN + '\t\t' + t + '\t\tbuf = calloc(size, 1);\n'
            else:
                body = HEADN + '\t\tbuf = calloc(size, 1);\n\t\t' + t
            yield tn + '|' + pos, rep(FLIP, (GET, body), (DECL, 'uint32_t n;\n\tint size, got, r;'))
