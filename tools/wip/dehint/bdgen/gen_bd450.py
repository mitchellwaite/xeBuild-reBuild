"""Attempt 33: real types in loadBl / loadBlFiles / loadConsoleBlFiles (never swept there: attempt 17's gen_bd282 retyped
isUpdateBl, gen_bd283 calcBlAreaSize, gen_bd192 buildFlash's fuse), crossed with every loadBl-side trick off alone, so a
type that frees one trick shows up.  Types: loadBl's `type` local (int / uint32_t / unsigned), its `i` parameter (uint32_t /
int), the result (`uint32_t *pr` + `uint32_t r` / `int`), the loop counters (uint32_t with the cast / int without), and
the console loop's r and i.  Runs on src as of 5a0bc459.  `python tools/wip/dehint/bdrun.py tools/wip/dehint/bdgen/gen_bd450.py`."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bdhints, bdrun

FOCUS = ['_loadBlFiles', '_loadConsoleBlFiles']

LB_HEAD = 'static void loadBl(struct fileent *e, uint32_t i, uint32_t *pr)\n{\n\tint type;\n'


def lb_type(t, ty):
    return bdrun.sub(t, LB_HEAD, LB_HEAD.replace('\tint type;', '\t%s type;' % ty), 1)


def lb_i(t, ty):
    return bdrun.sub(t, LB_HEAD, LB_HEAD.replace('uint32_t i,', '%s i,' % ty), 1)


def pr_int(t):
    t = bdrun.sub(t, LB_HEAD, LB_HEAD.replace('uint32_t *pr', 'int *pr'), 1)
    a, b = bdrun.fnspan(t, 'int loadBlFiles(void)')
    s = t[a:b].replace('\tuint32_t r;\n', '\tint r;\n')
    return t[:a] + s + t[b:]


def lbf_i_int(t):
    a, b = bdrun.fnspan(t, 'int loadBlFiles(void)')
    s = t[a:b].replace('\tuint32_t i;\n', '\tint i;\n').replace('i < (uint32_t)xb.nFiles', 'i < xb.nFiles')
    return t[:a] + s + t[b:]


def con(t, what):
    a, b = bdrun.fnspan(t, 'int loadConsoleBlFiles(void)')
    s = t[a:b]
    if what == 'r':
        s = s.replace('\tuint32_t r;\n', '\tint r;\n')
    elif what == 'i':
        s = s.replace('\tuint32_t i;\n', '\tint i;\n').replace('i < (uint32_t)xb.nFiles', 'i < xb.nFiles').replace(
            'if ((uint32_t)xb.nFiles <= 1)', 'if (xb.nFiles <= 1)')
    elif what == 'type':
        s = s.replace('\t\t\tint type = e->type;', '\t\t\tuint32_t type = e->type;')
    return t[:a] + s + t[b:]


VARIANTS = {
    'src': lambda t: t,
    'type_u32': lambda t: lb_type(t, 'uint32_t'),
    'type_uns': lambda t: lb_type(t, 'unsigned'),
    'i_int': lambda t: lb_i(t, 'int'),
    'pr_int': pr_int,
    'lbf_i_int': lbf_i_int,
    'lbf_i_int+i_int': lambda t: lb_i(lbf_i_int(t), 'int'),
    'con_r': lambda t: con(t, 'r'),
    'con_i': lambda t: con(t, 'i'),
    'con_type': lambda t: con(t, 'type'),
    'type_u32+pr_int': lambda t: pr_int(lb_type(t, 'uint32_t')),
}

ETYPE = ('\t\t\t\t} else if (type)\n', '\t\t\t\t} else\n')
CP = ('if ((char *)__builtin_constant_p(i) == (char *)1 && (char *)__builtin_constant_p(type) == (char *)1) {',
      'if (0) {')


def off(t, k):
    if k == 'none':
        return t
    if k == 'etype':
        return bdrun.sub(t, *ETYPE)
    if k == 'cp':
        return bdrun.sub(t, *CP)
    return bdhints.off(t, k)


OFFS = os.environ.get('BDOFFS', 'none,exp_t10,exp_pr,lab_t5le,pin_d,vol_fail,lab_none,etype,cp').split(',')


def CASES(base):
    out = []
    for v, f in VARIANTS.items():
        for k in OFFS:
            out.append(('%s|%s' % (v, k), lambda b, f=f, k=k: off(f(b), k)))
    return out
