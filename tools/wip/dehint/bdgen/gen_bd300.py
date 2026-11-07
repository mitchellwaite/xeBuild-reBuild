"""Attempt 19, diagnostics for t5le through S / Xc (attempt 18's closed form): what the signature block's three factors
(Psig: the 5/17/11 test, Pk: the pub1bl test, Pf: the verify test) do to the failed log, bb 111 and the score when they
move.  None of these is a shape to land: `!= 1` changes the compare, the `if (type)` wrappers are dead tests.
t5le off, everything else as src.  Runs on src as of 9210177c.  `python gen_bd300.py` writes each case to build/bd/a19/."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import bdhints, bdrun

FAIL = '\t\t\t\t\tlog_printf(0, "\\n***** ERROR: loaded %s, but signature check failed!\\n", e->name);\n'
PASS = '\t\t\t\t\tlog_printf(1, "loaded %s, signature check passed!\\n", e->name);\n'
NOKEY = '\t\t\t\tlog_printf(1, "loaded %s, could not check signature rsa key not present!\\n", e->name);\n'
VER = '\t\t\t\tif (!cbVerifySig(e->data, xb.pub1bl)) {\n'
KEY = '\t\t\tif (xb.pub1bl) {\n'


def base(b):
    return bdhints.off(b, 'lab_t5le')


def ne1(b):  # Pf 51.2%: nonequal with the call
    return bdrun.sub(base(b), VER, '\t\t\t\tif (cbVerifySig(e->data, xb.pub1bl) != 1) {\n')


def fail50(b):  # Pf 50%: no call in the failed arm's first block
    return bdrun.sub(base(b), VER + FAIL, VER + '\t\t\t\t\tif (type)\n\t' + FAIL)


def nokey_t(b):  # Pk 69.8%: no call in the no-key arm's first block
    return bdrun.sub(base(b), '\t\t\t} else\n' + NOKEY, '\t\t\t} else if (type)\n' + NOKEY)


def key_t(b):  # Pk 93.3%: no call in the key arm's first block
    t = bdrun.sub(base(b), KEY + VER, KEY + '\t\t\t\tif (type) {\n' + VER)
    return bdrun.sub(t, '\t\t\t} else\n' + NOKEY, '\t\t\t\t}\n\t\t\t} else\n' + NOKEY)


def CASES(b):
    return [('base', base), ('ne1', ne1), ('fail50', fail50), ('nokey_t', nokey_t), ('key_t', key_t),
            ('key_t+fail50', lambda b: bdrun.sub(key_t(b), VER + FAIL, VER + '\t\t\t\t\tif (type)\n\t' + FAIL)),
            ('key_t+ne1', lambda b: bdrun.sub(key_t(b), VER, '\t\t\t\tif (cbVerifySig(e->data, xb.pub1bl) != 1) {\n'))]


FOCUS = ['_loadBlFiles']

if __name__ == '__main__':
    import bdlib
    b = bdlib.read_src(os.path.join(bdlib.R, 'src/build.c'))
    os.makedirs(os.path.join(bdlib.BUILD, 'a19'), exist_ok=True)
    for lab, f in CASES(b):
        open(os.path.join(bdlib.BUILD, 'a19', 'g300_' + lab.replace('+', '_') + '.c'), 'w', newline='\n').write(f(b))
