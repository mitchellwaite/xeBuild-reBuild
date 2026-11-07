"""Attempt 54: the signature check as an IPA-inlined helper (it holds calls) whose own profile
sets the signature-failed flow S that vrp1's joiner formula for the SE copy uses (exp_pr), with
the tail's r test as the expect, plain `r`, or `(int)r < 0`.
python tools/wip/dehint/bdgen/a46run.py tools/wip/dehint/bdgen/a54_sig.py [-p 0,99] [-k label]"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import a46_m1hints as H
from a50_share import ANCHOR, sub
from a50_sig import OLD, HEAD, FAIL, PASS, NOKEY

BASE = H.BASE
PRX = 'if (__builtin_expect(r != 0, 0))\n'
TAILS = {'x': PRX, 'r': 'if (r)\n', 'n': 'if ((int)r < 0)\n'}
H1 = '/* a CB/CF/SB\'s signature, by the 1BL key */\nstatic int %s(struct fileent *e)\n{\n'
BODIES = {
    # returns 1 when the check failed
    'f1': (H1 % 'sigFailed' + '\tif (!xb.pub1bl) {\n' + NOKEY + '\t\treturn 0;\n\t}\n\tif (!cbVerifySig(e->data, xb.pub1bl)) {\n' + FAIL +
           '\t\treturn 1;\n\t}\n' + PASS + '\treturn 0;\n}\n\n',
           '\t\t\t\tif ((type == 5 || type == 17 || type == 11) && sigFailed(e))\n\t\t\t\t\tr = -1;\n'),
    'f1n': (H1 % 'sigFailed' + '\tif (!xb.pub1bl) {\n' + NOKEY + '\t\treturn 0;\n\t}\n\tif (!cbVerifySig(e->data, xb.pub1bl)) {\n' + FAIL +
           '\t\treturn 1;\n\t}\n' + PASS + '\treturn 0;\n}\n\n',
           '\t\t\t\tif (type == 5 || type == 17 || type == 11) {\n\t\t\t\t\tif (sigFailed(e))\n\t\t\t\t\t\tr = -1;\n\t\t\t\t}\n'),
    # pass last
    'f2': (H1 % 'sigFailed' + '\tif (!xb.pub1bl) {\n' + NOKEY + '\t\treturn 0;\n\t}\n\tif (cbVerifySig(e->data, xb.pub1bl)) {\n' + PASS.replace('\t', '\t\t', 1) +
           '\t\treturn 0;\n\t}\n' + FAIL.replace('\t\t', '\t', 1) + '\treturn 1;\n}\n\n',
           '\t\t\t\tif ((type == 5 || type == 17 || type == 11) && sigFailed(e))\n\t\t\t\t\tr = -1;\n'),
    # returns 0 when the check failed
    'ok': (H1 % 'sigOk' + '\tif (!xb.pub1bl) {\n' + NOKEY + '\t\treturn 1;\n\t}\n\tif (!cbVerifySig(e->data, xb.pub1bl)) {\n' + FAIL +
           '\t\treturn 0;\n\t}\n' + PASS + '\treturn 1;\n}\n\n',
           '\t\t\t\tif ((type == 5 || type == 17 || type == 11) && !sigOk(e))\n\t\t\t\t\tr = -1;\n'),
    'okv': (H1 % 'sigOk' + '\tint ok = 1;\n\n\tif (xb.pub1bl) {\n\t\tif (!cbVerifySig(e->data, xb.pub1bl)) {\n\t' + FAIL +
           '\t\t\tok = 0;\n\t\t} else\n\t' + PASS + '\t} else\n' + NOKEY + '\treturn ok;\n}\n\n',
           '\t\t\t\tif ((type == 5 || type == 17 || type == 11) && !sigOk(e))\n\t\t\t\t\tr = -1;\n'),
    # returns -1 when failed, assigned to r
    'm1': (H1 % 'checkBlSig' + '\tif (!xb.pub1bl) {\n' + NOKEY + '\t\treturn 0;\n\t}\n\tif (cbVerifySig(e->data, xb.pub1bl)) {\n' + PASS.replace('\t', '\t\t', 1) +
           '\t\treturn 0;\n\t}\n' + FAIL.replace('\t\t', '\t', 1) + '\treturn -1;\n}\n\n',
           '\t\t\t\tif (type == 5 || type == 17 || type == 11)\n\t\t\t\t\tr = checkBlSig(e);\n'),
}
V = {}
for b, (body, call) in BODIES.items():
    for k, tl in TAILS.items():
        def f(t, body=body, call=call, tl=tl):
            t = sub(t, OLD, call)
            t = sub(t, ANCHOR, body + ANCHOR)
            if tl != PRX:
                t = sub(t, PRX, tl)
            return t
        V['%s_%s' % (b, k)] = f
