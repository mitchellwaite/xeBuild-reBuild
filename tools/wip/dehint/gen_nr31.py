"""Attempt 5, angle 2: verbose-only structure (the clone's frequencies are the original's estimate; only the function's output has to stay fixed)."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from nrflip import *
BS = chr(92)
NL = "if (verbose)\n\t\t\tputchar('" + BS + "n');"
WAIT = 'if (verbose)\n\t\t\tprintf("waiting for 0x%x bytes' + BS + 'n", size);\n\t\tgot = 0;'
PR = 'if (verbose)\n\t\t\t\tprintf("received 0x%08x of 0x%08x' + BS + 'r", got, size);'
PRC = 'printf("received 0x%08x of 0x%08x' + BS + 'r", got, size);'
FAILNL = "if (verbose)\n\t\t\t\t\tputchar('" + BS + "n');"
TAIL = "if (verbose)\n\t\t\tputchar('" + BS + "n');\n\t\tif (got == size) {\n\t\t\t*len = size;\n\t\t\treturn buf;\n\t\t}\n\t\tif (verbose)\n\t\t\tputchar('" + BS + "n');"
TAILS = {
 'plain': TAIL,
 'block': "if (verbose) {\n putchar('" + BS + "n');\n }\n if (got == size) {\n*len = size;\nreturn buf;\n}\n if (verbose) {\nputchar('" + BS + "n');\n}",
 'nested': "if (verbose) {\n putchar('" + BS + "n');\n if (got != size)\n putchar('" + BS + "n');\n }\n if (got == size) {\n*len = size;\nreturn buf;\n}",
 'ne-first': "if (verbose)\n putchar('" + BS + "n');\n if (got != size) {\n if (verbose)\n putchar('" + BS + "n');\n log_printf(0, \"received only %x of %x bytes! fail" + BS + "n\", got, size);\n if (buf != (uint8_t *)&netEmpty)\n free(buf);\n return NULL;\n }\n *len = size;\n return buf;\n@CUT@",
 'puts': "if (verbose)\n putchar('" + BS + "n');\n if (got == size) {\n*len = size;\nreturn buf;\n}\n if (verbose)\n printf(\"" + BS + "n\");",
 'twoputs': "if (verbose)\n printf(\"" + BS + "n\");\n if (got == size) {\n*len = size;\nreturn buf;\n}\n if (verbose)\n printf(\"" + BS + "n\");",
 'else': "if (verbose)\n putchar('" + BS + "n');\n if (got == size) {\n*len = size;\nreturn buf;\n} else if (verbose)\n putchar('" + BS + "n');",
}
LOOPV = {
 'plain': PR,
 'block': 'if (verbose) {\n' + PRC + '\n}',
 'cont': 'if (!verbose)\n continue;\n' + PRC,
 'cont2': 'if (verbose) {\n' + PRC + '\n continue;\n}',
}
WAITS = {
 'plain': WAIT,
 'gotfirst': 'got = 0;\nif (verbose)\n printf("waiting for 0x%x bytes' + BS + 'n", size);',
 'block': 'if (verbose) {\n printf("waiting for 0x%x bytes' + BS + 'n", size);\n}\n got = 0;',
}
FAILS = {
 'plain': FAILNL,
 'block': "if (verbose) {\nputchar('" + BS + "n');\n}",
}
VARS = {
 'plain': None,
 'copy': 'const uint32_t v = verbose;',
}


def norm(s):
    return s


def variants():
    base = FLIP.replace('\t', '\t')
    for tn, t in TAILS.items():
        for ln, l in LOOPV.items():
            for wn, w in WAITS.items():
                for fn, f in FAILS.items():
                    s = base
                    s = rep(s, (TAIL, t), (PR, l), (WAIT, w), (FAILNL, f))
                    if '@CUT@' in s:
                        a = s.index('@CUT@')
                        b = s.index('*len = 0;\n\treturn (uint8_t *)&netEmpty;') if 0 else s.rindex('\t}\n\t*len = 0;')
                        s = s[:a] + s[b:]
                    yield '|'.join((tn, ln, wn, fn)), s
