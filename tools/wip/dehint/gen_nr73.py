"""Attempt 8: gen_nr72's best helper bodies x caller forms that lose the guard's early return (opcode + call, .869)."""
import itertools, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gen_nr72 import *


def caller2(kind):
    call = 'netRecvDone(buf, got, size, len, verbose)'
    d = '\t\tdo {\n' + BODY + '\t\t} while (got < size);\n'
    z = '\t*len = 0;\n\treturn (uint8_t *)&netEmpty;\n}\n\n'
    if kind == 'ret':
        return '\t\tif (size > 0)\n' + d + 'return ' + call + ';\n\t}\n' + z
    if kind == 'var2':	# zero arm sets the result, single return
        return '\t\tif (size > 0)\n' + d + 'buf = ' + call + ';\n\t} else {\n\t\t*len = 0;\n\t\tbuf = (uint8_t *)&netEmpty;\n\t}\n\treturn buf;\n}\n\n'
    if kind == 'var3':	# default result, single return
        return '\t\tif (size > 0)\n' + d + 'buf = ' + call + ';\n\t\treturn buf;\n\t}\n' + z
    if kind == 'head1':	# early returns kept in the head, one result var
        return '\t\tif (size > 0)\n' + d + 'ret = ' + call + ';\n\t} else {\n\t\t*len = 0;\n\t\tret = (uint8_t *)&netEmpty;\n\t}\n\treturn ret;\n}\n\n'
    if kind == 'zlast':	# zero arm first
        raise ValueError
    if kind == 'ifnot':	# status-like test on the pointer
        return '\t\tif (size > 0)\n' + d + 'if (' + call + ')\n\t\t\treturn buf;\n\t\treturn NULL;\n\t}\n' + z
    if kind == 'nest':	# helper call in the else of the guard and after the loop
        return '\t\tif (size > 0) {\n' + d + '\t\t}\n\t\tbuf = ' + call + ';\n\t\treturn buf;\n\t}\n' + z


def variants():
    for hk, ck in itertools.product(('eq', 'ne', 'eqs', 'nes', 'nesv', 'var', 'vars'), ('ret', 'var2', 'var3', 'head1', 'ifnot', 'nest')):
        p = PRE
        if ck == 'head1':
            p = p.replace('uint8_t *buf;', 'uint8_t *buf, *ret;')
        yield hk + '|' + ck, helper(hk, True) + p + caller2(ck)
