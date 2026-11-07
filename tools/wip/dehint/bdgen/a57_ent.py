"""Attempt 57: the per-entry work as a static helper that holds the switch *and* the could-not-read
log (so the arms' breaks reach the r test, not the return block), the loop calling it in the none
test's guarded block (which then holds a call: PRED_CALL on the strnicmp edge, the 0.86 factor of
attempts 45/46).  Axes: return form (neg: log, -1 / 0; r: log if r, return r; one: log, 1 / 0;
first: if (!r) return 0 first), call site (nest / and), which loaders (b = loadBlFiles only,
bc = both), hints (OFFS from a57lib, plus the loader's own).
python tools/wip/dehint/bdgen/a46run.py tools/wip/dehint/bdgen/a57_ent.py [-k label]"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from a57lib import *

LB = 'int loadBlFiles(void)\n{'
CB = 'int loadConsoleBlFiles(void)\n{'
PH = 'void patchHeaderOpts(void)'
LOGL = None


def dd(s, n=2):
    return ''.join(l[n:] if l.startswith('\t' * n) else l for l in s.splitlines(True))


def sw(fn):
    a = fn.index('\t\t\tswitch (type) {')
    b = fn.index('\t\t\t}\n\t\t}\n\t\tif (r) {', a)
    return fn[a:b + 5]


def logcall(fn):
    a = fn.index('**** could not read'); a = fn.rindex('\t\t\tlog_printf', 0, a)
    return fn[a:fn.index('\n', a) + 1].strip()


def helper(name, s, lg, ret):
    h = 'static int %s(struct fileent *e)\n{\n\tuint32_t r = 0;\n\tint type = e->type;\n\n' % name
    h += dd(s, 2)
    if ret == 'neg':
        h += '\tif (r) {\n\t\t%s\n\t\treturn -1;\n\t}\n\treturn 0;\n}\n\n' % lg
    elif ret == 'one':
        h += '\tif (r) {\n\t\t%s\n\t\treturn 1;\n\t}\n\treturn 0;\n}\n\n' % lg
    elif ret == 'r':
        h += '\tif (r)\n\t\t%s\n\treturn r;\n}\n\n' % lg
    elif ret == 'first':
        h += '\tif (!r)\n\t\treturn 0;\n\t%s\n\treturn -1;\n}\n\n' % lg
    return h


def loopfn(head, name, call, pre=''):
    s = head + '\n{\n\tuint32_t i;\n\n' + pre + '\tfor (i = 1; i < (uint32_t)xb.nFiles; i++) {\n\t\tstruct fileent *e = &xb.files[i];\n\n'
    if call == 'nest':
        s += '\t\tif (strnicmp(e->name, "none", 4) || e->crc) {\n\t\t\tif (%s(e))\n\t\t\t\treturn -1;\n\t\t}\n' % name
    else:
        s += '\t\tif ((strnicmp(e->name, "none", 4) || e->crc) && %s(e))\n\t\t\treturn -1;\n' % name
    s += '\t}\n\treturn 0;\n'
    return s


def make(ret='neg', call='nest', which='b'):
    def f(t):
        i = t.index(LB); j = t.index(CB); k = t.index(PH)
        lbf = t[i:j]; cbf = t[j:k]
        lg = logcall(lbf)
        sb = sw(lbf).replace('xb.files[i].data + 2', 'e->data + 2')
        hb = '/* load one input file by its type; the arms only set r, which is\n   tested once after the switch */\n' + helper('loadBl', sb, lg, ret)
        nb = loopfn('int loadBlFiles(void)', 'loadBl', call) + '}\n\n'
        if which == 'bc':
            sc = sw(cbf)
            hc = helper('loadConsoleBl', sc, lg, ret)
            pre = ''
            tailc = '}\n\n'
            if '\tif ((uint32_t)xb.nFiles <= 1)\n\t\tgoto none;\n' in cbf:
                pre = '\t/* the cold label gives the shrink-wrapped return 0 frequency 0, so\n\t   bb-reorder lays it out last */\n\tif ((uint32_t)xb.nFiles <= 1)\n\t\tgoto none;\n'
                tailc = 'none: __attribute__((cold));\n\treturn 0;\n}\n\n'
            nc = hc + loopfn('int loadConsoleBlFiles(void)', 'loadConsoleBl', call, pre) + tailc
        else:
            nc = cbf
        hs = t.rindex('/* load the input files', 0, i)
        return t[:hs] + hb + nb + nc + t[k:]
    return f


def comp(f, ed):
    return lambda t: f(H_apply(t, ed))


V = {}
for ret in ('neg', 'one', 'r', 'first'):
    for call in ('nest', 'and'):
        for which in ('b', 'bc'):
            for k, ed in OFFS.items():
                if which == 'b' and k == 'none':
                    continue
                V['%s_%s_%s%s' % (ret, call, which, '_' + k if k else '')] = comp(make(ret, call, which), ed)
