"""Attempt 37: gen_bd490 showed the route works: a load at retail's start (`n = xb.nFlashFiles;`, unused) flips the
kit sum and leaves 10 lines, all retail's five `cmp i,n` with the operands swapped (n's SSA version is now below the
loops' i, so fold puts n first; in src n is ch2's guard copy, a high version).  `n = xb.nFiles;` leaves 2 (only
findFile(25)'s cmp).  Here the load comes from the helpers themselves: findFileOffset / findFileSize / findFile read
the count into a local before the loop, so the inlined body's first block holds the load.  pin off.
Run: python tools/wip/dehint/bdorder.py tools/wip/dehint/bdgen/gen_bd491.py"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import bdhints, bdrun

HELP = {
    'off': ('uint32_t findFileOffset(int type)\n{\n\tint i;\n\n\tfor (i = 0; i < xb.nFlashFiles; i++)\n',
            'nFlashFiles'),
    'size': ('uint32_t findFileSize(int type)\n{\n\tint i;\n\n\tfor (i = 0; i < xb.nFlashFiles; i++)\n',
             'nFlashFiles'),
    'file': ('int findFile(int type)\n{\n\tint i;\n\n\tfor (i = 0; i < xb.nFiles; i++)\n', 'nFiles'),
}


def form(h, f):
    old, cnt = HELP[h]
    head = old.split('{')[0]
    if f == 'decl':
        return old, head + '{\n\tint i, n = xb.%s;\n\n\tfor (i = 0; i < n; i++)\n' % cnt
    if f == 'stmt':
        return old, head + '{\n\tint i, n;\n\n\tn = xb.%s;\n\tfor (i = 0; i < n; i++)\n' % cnt
    if f == 'comma':
        return old, head + '{\n\tint i, n;\n\n\tfor (i = 0, n = xb.%s; i < n; i++)\n' % cnt
    if f == 'decl2':
        return old, head + '{\n\tint n = xb.%s;\n\tint i;\n\n\tfor (i = 0; i < n; i++)\n' % cnt


def CASES(base):
    base = bdhints.off(base, 'pin_size')
    out = [('src', base)]
    for hs in (('off',), ('off', 'size'), ('off', 'size', 'file'), ('file',)):
        for f in ('decl', 'stmt', 'comma', 'decl2'):
            t = base
            for h in hs:
                a, b = form(h, f)
                t = bdrun.sub(t, a, b)
            out.append(('%s_%s' % ('+'.join(hs), f), t))
    return out
