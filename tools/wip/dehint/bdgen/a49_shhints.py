"""Attempt 49: each remaining hint off on the shared-helper equal bases (a49_share.py's L_x1,
L_x2, L_x1_24, L_x2_24), and case 24's second arm through loadBl24 too.
python tools/wip/dehint/bdgen/a46run.py tools/wip/dehint/bdgen/a49_shhints.py [-p 95,99]"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from a49_share import BASE, mk
import a46_m1hints as H

LAB = ('\t\t\t\tdevgl: __attribute__((hot));\n', '')
A2 = '''					r = 0;
					if (loadBaseFile(e->name, e))
						r = defaultBl60(e);
					else if (e->size != 0x60)
						r = defaultBl60(e);
'''


def arm2(t):
    a = t.index('\t\t\t\tdevgl: __attribute__((hot));\n')
    b = t.index(A2, a)
    return t[:b] + '\t\t\t\t\tr = loadBl24(e);\n' + t[b + len(A2):]


def sub(t, pairs):
    for a, b in pairs:
        assert a in t, a
        t = t.replace(a, b, 1)
    return t


OFF = {'all': [], 't10': [H.T10], 'pr': [H.PR], 'bar': [H.BAR], 'none': [H.NONE, H.NONE2],
       'dev': [H.DEV], 'pin': [H.PIN], 'lab': [LAB]}
V = {}
for base in ('x1', 'x2', 'x1_24', 'x2_24', 'x1_24a2', 'x2_24a2'):
    x = base[:2]
    b24 = '24' in base
    a2 = base.endswith('a2')
    for k, p in OFF.items():
        def f(t, x=x, b24=b24, a2=a2, p=p):
            t = mk(x, False, b24, True)(t)
            if a2:
                t = arm2(t)
            return sub(t, p)
        V[base + '_' + k] = f

# second stage: x2_24 with exp_t10 off (IDENTICAL), each other hint off on top
if os.environ.get('A49_STAGE') == '2':
    V = {}
    for k, p in OFF.items():
        if k == 't10':
            continue
        V['x2_24t_' + k] = (lambda p: lambda t: sub(mk('x2', False, True, True)(t), [H.T10] + p))(p)
    V['x2_24t_prbar'] = lambda t: sub(mk('x2', False, True, True)(t), [H.T10, H.PR, H.BAR])
