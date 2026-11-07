"""Attempt 57: shared pieces.  OFFS = the four loader hints, each removable; cross(name, edits) gives
V rows name, name_pr, name_bar, name_lab, name_none, name_all (all four off).  Text helpers cut the
static helpers block (defaultBl60, loadXell, loadBl24) out of src and put it elsewhere."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import a46_m1hints as H
import bdrun
BASE = H.BASE
LAB = ('\t\t\t\tdevgl: __attribute__((hot));\n', '')
OFFS = {'': [], 'pr': [H.PR], 'bar': [H.BAR], 'lab': [LAB], 'none': [H.NONE, H.NONE2],
        'all': [H.PR, H.BAR, LAB, H.NONE, H.NONE2]}


def cross(name, edits, offs=None):
    V = {}
    for k, ed in OFFS.items():
        if offs is not None and k not in offs:
            continue
        if callable(edits):
            V[name + ('_' + k if k else '')] = (lambda f, e: lambda t: H_apply(f(t), e))(edits, ed)
        else:
            V[name + ('_' + k if k else '')] = list(edits) + ed
    return V


def H_apply(t, ed):
    for a, b in ed:
        t = bdrun.sub(t, a, b, 1)
    return t


HB = '/* the default 0x60-byte bootloader (type 24) */\n'
HE = '/* load the input files by their type;'


def helpers(t):
    i = t.index(HB); j = t.index(HE)
    return t[i:j], t[:i] + t[j:]


PROTO = 'static int defaultBl60(struct fileent *e);\nstatic int loadXell(struct fileent *e);\nstatic int loadBl24(struct fileent *e);\n\n'
