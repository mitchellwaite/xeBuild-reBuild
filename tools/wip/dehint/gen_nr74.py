"""Attempt 8: guard + while (the while's own first test folds after profile_estimate, so its 3% stays stale) x tail helper x caller."""
import itertools, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gen_nr72 import *


def caller3(kind, lf):
    call = 'netRecvDone(buf, got, size, len, verbose)'
    d = {'ifwhile': '\t\tif (size > 0) {\n' + LOOP + '\t\t}\n', 'do': '\t\tif (size > 0)\n\t\tdo {\n' + BODY + '\t\t} while (got < size);\n', 'for': '\t\tif (size > 0)\n\t\t\tfor (got = 0; got < size;) {\n' + BODY + '\t\t\t}\n'}[lf]
    z = '\t*len = 0;\n\treturn (uint8_t *)&netEmpty;\n}\n\n'
    if kind == 'ret':
        return d + 'return ' + call + ';\n\t}\n' + z
    if kind == 'ifnot':
        return d + 'if (' + call + ')\n\t\t\treturn buf;\n\t\treturn NULL;\n\t}\n' + z
    if kind == 'ifnull':
        return d + 'if (!' + call + ')\n\t\t\treturn NULL;\n\t\treturn buf;\n\t}\n' + z
    if kind == 'nest':	# got == size only after the loop; the guard's else goes straight to the short path
        return d + 'return ' + call + ';\n\t}\n' + z


def variants():
    for hk, ck, lf in itertools.product(('eq', 'ne', 'eqs', 'nes', 'nesv', 'var', 'vars'), ('ret', 'ifnot', 'ifnull'), ('ifwhile', 'do', 'for')):
        yield '|'.join((hk, ck, lf)), helper(hk, True) + PRE + caller3(ck, lf)
