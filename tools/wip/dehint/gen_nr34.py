"""Attempt 5: verbose-only exit with its own destination, so J (the clone's join) isn't inflated. Model check of the stale lever; none of these read naturally."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from nrflip import *
BS = chr(92)
PRC = 'printf("received 0x%08x of 0x%08x' + BS + 'r", got, size);'
PR = 'if (verbose)\n\t\t\t\t' + PRC
NLC = "putchar('" + BS + "n');"
AFTER = "\t\tif (verbose)\n\t\t\t" + NLC + "\n\t\tif (got == size) {"
FAILNL2 = "\t\t}\n\t\tif (verbose)\n\t\t\t" + NLC + "\n\t\tlog_printf(0, \"received only"
FORMS = {
 'check': ('if (verbose) {\n' + PRC + '\nif (got >= size) {\n' + NLC + '\ngoto check;\n}\n}', [(AFTER, "\t\tif (verbose)\n\t\t\t" + NLC + "\ncheck:\n\t\tif (got == size) {")]),
 'check-nl': ('if (verbose) {\n' + PRC + '\nif (got >= size)\ngoto nl;\n}', [(AFTER, "\t\tif (verbose)\nnl:\n\t\t\t" + NLC + "\n\t\tif (got == size) {")]),
 'nl-break': ('if (verbose) {\n' + PRC + '\nif (got >= size) {\n' + NLC + '\nbreak;\n}\n}', [(AFTER, "\t\tif (verbose && got < size)\n\t\t\t" + NLC + "\n\t\tif (got == size) {")]),
 'done': ('if (verbose) {\n' + PRC + '\nif (got >= size) {\n' + NLC + '\nif (got == size) {\n*len = size;\nreturn buf;\n}\ngoto fail;\n}\n}', [(FAILNL2, "\t\t}\n\t\tif (verbose)\nfail:\n\t\t\t" + NLC + "\n\t\tlog_printf(0, \"received only")]),
 'flag': ('if (verbose) {\n' + PRC + '\nif (got >= size)\nbreak;\n}', []),
}
SELS = {'plain': SEL, 'side': 'if ((r = select(0, &fds, NULL, NULL, &tv)) == SOCKET_ERROR || r == 0) {'}


def variants():
    for fn, (f, rs) in FORMS.items():
        for sn, se in SELS.items():
            yield fn + '|' + sn, rep(FLIP, (PR, f), (SEL, se), *rs)
