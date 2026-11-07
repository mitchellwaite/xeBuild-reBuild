"""Attempt 27, exp_t10 through the type-11 block's frequency.  Read from bbro (build/bd/a27/e1_80.bbro, e1_82.bbro): with
exp_t10 off, the CG flow that vrp1 threads into chk with type 10 known is taken out of the shared checkBl copy's
type == 11 test, so the type-11 block (bbro 24) drops from 22 to 18 and loses its round-4 tie with block 18 (21), which
moves it to the end; and the merged checkBl call block (116) goes over the duplication threshold (99 >= 88), so bbro
copies the `if (r)` test into it.  The type-11 block's other source is the __builtin_constant_p entry, whose weight
comes from its test's form (attempt 14's gen_bd253), so cross the weights with exp_t10 off.  The entry's type value
(`(type & 1) + 18`, 18, 19, type) is an axis too.  Runs on src as of 7a9a2b41, on gen_bd380.c2base."""
import itertools, os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import bdhints, bdrun
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gen_bd380 as g380

CP_SRC = '(char *)__builtin_constant_p(i) == (char *)1 && (char *)__builtin_constant_p(type) == (char *)1'
I = {
    'pi': '(char *)__builtin_constant_p(i) == (char *)1',
    'ii': '__builtin_constant_p(i) == 1',
    'bi': '__builtin_constant_p(i)',
    'x': None,
}
T = {
    'pt': '(char *)__builtin_constant_p(type) == (char *)1',
    'it': '__builtin_constant_p(type) == 1',
    'bt': '__builtin_constant_p(type)',
    'x': None,
}
TY = {'t18': '(type & 1) + 18', '18': '18', 'ty': 'type'}


def mk(t, a, b, op, t10, ty):
    t = g380.c2base(t)
    parts = [p for p in (I[a], T[b]) if p]
    t = bdrun.sub(t, CP_SRC, (' %s ' % op).join(parts), 1)
    t = bdrun.sub(t, '\t\t\ttype = (type & 1) + 18;\n', '\t\t\ttype = %s;\n' % TY[ty], 1)
    if t10 == 'no10':
        t = bdhints.off(t, 'exp_t10')
    return t


def CASES(base):
    out = []
    for a, b, op, t10, ty in itertools.product(I, T, ('&&', '||'), ('t10', 'no10'), TY):
        if (I[a] is None or T[b] is None) and op == '||':
            continue
        if I[a] is None and T[b] is None:
            continue
        out.append(('%s %s %s %s %s' % (a, b, op, t10, ty), lambda x, a=(a, b, op, t10, ty): mk(x, *a)))
    return out


FOCUS = ['_loadBlFiles']
