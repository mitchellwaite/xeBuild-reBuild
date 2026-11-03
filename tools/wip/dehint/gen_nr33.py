"""Attempt 5: exit edges that exist at profile_estimate only on the verbose path. n_exits and the exit sum go up, the clone loses the edge
but keeps the stale frequencies. Model check first: the extra tests are redundant."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from nrflip import *
BS = chr(92)
PRC = 'printf("received 0x%08x of 0x%08x' + BS + 'r", got, size);'
PR = 'if (verbose)\n\t\t\t\t' + PRC
FORMS = {
 'base': PR,
 'ge-break': 'if (verbose) {\n' + PRC + '\nif (got >= size)\nbreak;\n}',
 'eq-break': 'if (verbose) {\n' + PRC + '\nif (got == size)\nbreak;\n}',
 'gt-break': 'if (verbose) {\n' + PRC + '\nif (got > size)\nbreak;\n}',
 'lt-cont': 'if (verbose) {\n' + PRC + '\nif (got < size)\ncontinue;\nbreak;\n}',
 'and-break': 'if (verbose)\n' + PRC + '\nif (verbose && got >= size)\nbreak;',
 'ret': 'if (verbose) {\n' + PRC + '\nif (got >= size)\ngoto done;\n}',
}


def variants():
    for fn, f in FORMS.items():
        s = rep(FLIP, (PR, f))
        if 'goto done' in f:
            s = rep(s, ("\t\tif (verbose)\n\t\t\tputchar('" + BS + "n');\n\t\tif (got == size) {", "done:\n\t\tif (verbose)\n\t\t\tputchar('" + BS + "n');\n\t\tif (got == size) {"))
        yield fn, s
