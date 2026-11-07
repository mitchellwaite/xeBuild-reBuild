"""Attempt 51: exp_pr's last alignment (attempt 48: the SE block's profile_estimate frequency 7 needs
6, from 0.28^3 on its three == tests) with a size test in the SE condition (opcode-positive on
`e->size > 1`).  loadInputFile's buffers are calloc'd 0x10000 past the size, so data[1] of a
1-byte file is 0 and the test changes nothing.
python tools/wip/dehint/bdgen/a46run.py tools/wip/dehint/bdgen/a51_se.py -p 0,95,99"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import a46_m1hints as H
from a50_share import sub

BASE = H.BASE
OLD = "if (type == 9 && e->data[0] == 'S' && e->data[1] == 'E') {"
SE = {
    'src': OLD,
    'gt1a': "if (type == 9 && e->size > 1 && e->data[0] == 'S' && e->data[1] == 'E') {",
    'ge2a': "if (type == 9 && e->size >= 2 && e->data[0] == 'S' && e->data[1] == 'E') {",
    'gt1b': "if (e->size > 1 && type == 9 && e->data[0] == 'S' && e->data[1] == 'E') {",
    'gt1c': "if (type == 9 && e->data[0] == 'S' && e->size > 1 && e->data[1] == 'E') {",
    'nest': "if (type == 9 && e->size > 1) {\n\t\t\t\t\tif (e->data[0] == 'S' && e->data[1] == 'E') {",
}
PR = {'exp': None, 'ne': 'if (r != 0)\n', 'neg': 'if ((int)r < 0)\n'}
V = {}
for s, c in SE.items():
    for k, p in PR.items():
        def f(t, c=c, p=p, s=s):
            t = sub(t, OLD, c)
            if s == 'nest':
                # close the extra block after the SE arm
                a = "\t\t\t\t\txb.seReplacesCf = 1;\n\t\t\t\t}\n"
                t = sub(t, a, a + "\t\t\t\t}\n")
            if p:
                t = sub(t, 'if (__builtin_expect(r != 0, 0))\n', p)
            return t
        V['%s_%s' % (s, k)] = f
