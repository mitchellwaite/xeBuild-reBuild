"""Attempt 57: the two loaders as one static loop `loadFiles(int console)` (wrappers
loadBlFiles() / loadConsoleBlFiles() call it with 0 / 1), the two switches under `if (console)`
in the loop body.  Variants: which switch first (inside the none test), r at the top or in the body,
console's precheck kept for both or dropped (rows bl_* / con_*); and (rows ent_*) the per-entry
work as a static loadEntry(e, console) with the two switches and r.
python tools/wip/dehint/bdgen/a46run.py tools/wip/dehint/bdgen/a57_merge.py"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from a57lib import *

LB = 'int loadBlFiles(void)\n{'
CB = 'int loadConsoleBlFiles(void)\n{'
PH = 'void patchHeaderOpts(void)'


def switches(t):
    i = t.index(LB); j = t.index(CB); k = t.index(PH)
    lb = t[i:j]; cb = t[j:k]
    def sw(f):
        a = f.index('\t\t\tswitch (type) {')
        b = f.index('\t\t\t}\n\t\t}\n\t\tif (r) {', a)
        return f[a:b + 5]
    return t[:t.rindex('/* load the input files', 0, i)], sw(lb), sw(cb), t[k:]


def ind(s, n=1):
    return ''.join(('\t' * n + l) if l.strip() else l for l in s.splitlines(True))


def merge(first='bl', where='in', pre=False, rtop=False, vol=True, lab=True, pr=True, ret='int'):
    def f(t):
        head, sb, sc, tail = switches(t)
        if not vol:
            sb = sb.replace('\t\t\t\t__asm__ __volatile__("");\n', '')
        if not lab:
            sb = sb.replace('\t\t\t\tdevgl: __attribute__((hot));\n', '')
        if not pr:
            sb = sb.replace('if (__builtin_expect(r != 0, 0))\n', 'if (r != 0)\n')
        a, b = (sb, sc) if first == 'bl' else (sc, sb)
        cond = '!console' if first == 'bl' else 'console'
        if where == 'in':
            body = '\t\t\tif (%s) {\n%s\t\t\t} else {\n%s\t\t\t}\n' % (cond, ind(a), ind(b))
            loopbody = ('\t\te = &xb.files[i];\n' + ('' if rtop else '') +
                        '\t\tif (strnicmp(e->name, "none", 4) || e->crc) {\n\t\t\tint type = e->type;\n\n' + body + '\t\t}\n')
        s = '/* load the input files by their type, from the files or (console) from the\n   console\'s dump */\n'
        s += 'static int loadFiles(int console)\n{\n\tstruct fileent *e;\n\tuint32_t i;\n'
        if rtop:
            s += '\tuint32_t r;\n'
        s += '\n'
        if pre:
            s += '\tif ((uint32_t)xb.nFiles <= 1)\n\t\treturn 0;\n'
        s += '\tfor (i = 1; i < (uint32_t)xb.nFiles; i++) {\n'
        s += ('\t\tr = 0;\n' if rtop else '\t\tuint32_t r = 0;\n\n')
        s += loopbody
        lg = t[t.index('\t\tif (r) {\n\t\t\tlog_printf(0, "'):]
        lg = lg[:lg.index('\t\t}\n') + 4]
        s += lg + '\t}\n\treturn 0;\n}\n\n'
        s += 'int loadBlFiles(void)\n{\n\treturn loadFiles(0);\n}\n\nint loadConsoleBlFiles(void)\n{\n\treturn loadFiles(1);\n}\n\n'
        return head + s + tail
    return f


V = {}
for first in ('bl', 'con'):
    for pre in (0, 1):
        for rtop in (0, 1):
            for hints in ('all', 'none'):
                on = hints == 'all'
                V['%s_pre%d_r%d_%s' % (first, pre, rtop, hints)] = merge(first, 'in', pre, rtop, on, on, on)


# the same with the per-entry work as a static helper loadEntry(e, console) (the switches and r),
# each loop calling it: ipa-cp clones it per constant, each clone called once
def entry(first='bl', on=True):
    def f(t):
        head, sb, sc, tail = switches(t)
        if not on:
            sb = sb.replace('\t\t\t\t__asm__ __volatile__("");\n', '').replace('\t\t\t\tdevgl: __attribute__((hot));\n', '')
            sb = sb.replace('if (__builtin_expect(r != 0, 0))\n', 'if (r != 0)\n')
        sb = sb.replace("xb.files[i].data + 2", "e->data + 2")
        dd = lambda s: ''.join(l[2:] if l.startswith('\t\t') else l for l in s.splitlines(True))
        a, b = (sb, sc) if first == 'bl' else (sc, sb)
        cond = '!console' if first == 'bl' else 'console'
        s = 'static uint32_t loadEntry(struct fileent *e, int console)\n{\n\tuint32_t r = 0;\n\tint type = e->type;\n\n'
        s += '\tif (%s) {\n%s\t} else {\n%s\t}\n\treturn r;\n}\n\n' % (cond, ind(dd(a)), ind(dd(b)))
        i = t.index(LB); j = t.index(CB); k = t.index(PH)
        def loop(fn, c):
            a = fn.index('\t\t\tswitch (type) {'); b = fn.index('\t\t\t}\n\t\t}\n\t\tif (r) {', a) + 5
            pre = fn[:a]
            pre = pre.replace('\t\t\tint type = e->type;\n\n', '')
            return pre + '\t\t\tr = loadEntry(e, %d);\n' % c + fn[b:]
        lb = loop(t[i:j], 0); cb = loop(t[j:k], 1)
        if not on:
            cb = cb.replace('\tif ((uint32_t)xb.nFiles <= 1)\n\t\tgoto none;\n', '').replace('none: __attribute__((cold));\n\treturn 0;\n', '')
        return t[:i] + s + lb + cb + tail
    return f


for first in ('bl', 'con'):
    for on in (1, 0):
        V['ent_%s_%s' % (first, 'all' if on else 'none')] = entry(first, on)
