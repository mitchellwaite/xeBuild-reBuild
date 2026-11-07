"""Attempt 34, diagnostics only (expects are tricks): does pin_size follow the arms' frequencies the way pin_d did
(gen_bd463)?  pin_size off; an expect on the JTAG or kit test, either way."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bdhints, bdrun

FOCUS = ['_calcBlAreaSize']
J = '\tif (xb.type == BUILD_JTAG) {\n\t\tx = findFile(5);'
K = '\t} else if (xb.type > BUILD_DEVGL16) {\n\t\tx = findFile(11);'


def PRE(b):
    return bdhints.off(b, 'pin_size')


def CASES(base):
    out = []
    for v in (0, 1):
        out.append(('jtag %d' % v, bdrun.sub(base, J, J.replace('if (xb.type == BUILD_JTAG)', 'if (__builtin_expect(xb.type == BUILD_JTAG, %d))' % v))))
        out.append(('kit %d' % v, bdrun.sub(base, K, K.replace('if (xb.type > BUILD_DEVGL16)', 'if (__builtin_expect(xb.type > BUILD_DEVGL16, %d))' % v))))
    out.append(('none', lambda b: b))
    return out
