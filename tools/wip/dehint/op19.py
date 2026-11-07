#!/usr/bin/env python3
"""Attempt 19: whole-function shapes of parseOption (po1 = setBool expect, po2 = vlen expect).

python tools/wip/dehint/op19.py [-np|-p N] [-d dir] [-o out.c] [-v] variant ..
  a variant is a name in VARIANTS (edits on today's src, applied in order; `a+b` combines).
  -d dir  also writes profile_estimate / bbro dumps of the last variant into dir
  -o file writes the last variant's source
  -v      prints parseOption's diff (optlib.vdiff)"""
import os, re, subprocess, sys
from concurrent.futures import ThreadPoolExecutor
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import optlib

# the attempt's start: src with the vlen expect put back (attempt 19 landed `vv`, so
# `vv+X` is today's src with X)
SRC = optlib.read_src(optlib.SRC).replace('\tif (val && vlen) {', '\tif (__builtin_expect(vlen, 0)) {', 1)

PO1 = ('if (__builtin_expect(setBoolOption(opt, val) == 1, 0)) {',
       'if (setBoolOption(opt, val) == 1) {')
PO2 = ('if (__builtin_expect(vlen, 0)) {', 'if (vlen) {')

UNK = ('log_printf(1, "\\n\\n***** ERROR: unknown option \'%s\' with value \'%s\' provided on '
       'the command line!\\n", opt, val);')
INC = ('log_printf(1, "\\n\\n***** ERROR: unknown or incomplete option \'%s\' provided on the '
       'command line!\\n", opt);')
BAD = ('log_printf(1, "\\n\\n***** ERROR: parsing option \'%s\', value \'%s\' is incorrect!\\n", '
       'opt, val);')

TAIL = ('\tif (__builtin_expect(vlen, 0)) {\n\t\t' + UNK + '\n\t\treturn 0;\n\t}\n\t' + INC +
        '\n\treturn 0;\nbad:\n\t' + BAD + '\n\treturn 0;\n}\n')
assert TAIL in SRC, 'tail'

SB = ('\tif (__builtin_expect(setBoolOption(opt, val) == 1, 0)) {\n\t\tlog_printf(1, "\\n");\n'
      '\t\treturn 1;\n\t}\n')
END = 'bad:\n\t' + BAD + '\n\treturn 0;\n}\n'
NL = '\tlog_printf(1, "\\n");\n\treturn 1;\n'
assert SB in SRC and END in SRC


def okarm(field, fmt):
    return ('\t\t\txb.%s = myatou32(val, -1);\n\t\t\tok = 0;\n\t\t\tif (xb.%s != -1) {\n'
            '\t\t\t\tlog_printf(1, "%s", xb.%s);\n\t\t\t\tok = 1;\n\t\t\t}\n'
            '\t\t\tif (!ok)\n\t\t\t\tgoto bad;\n\t\t\treturn 1;\n' % (field, field, fmt, field),
            '\t\t\txb.%s = myatou32(val, -1);\n\t\t\tif (xb.%s == -1)\n\t\t\t\tgoto bad;\n'
            '\t\t\tlog_printf(1, "%s", xb.%s);\n\t\t\treturn 1;\n' % (field, field, fmt, field))


NOOK = [okarm('cpuTemp', 'Using CPUTEMP option, value %d\\n'),
        okarm('gpuTemp'.replace('gpuTemp', 'gpuFan'), 'Using GPUFAN option, value %d\\n')]
MACNL = ('\t\t\t\t\tlog_printf(1, "\\n");\n\t\t\t\t\treturn 1;\n', '\t\t\t\t\tgoto done;\n')
assert MACNL[0] in SRC

VARIANTS = {
    'cur': [],
    'po1': [PO1],
    'po2': [PO2],
    'both': [PO1, PO2],
    'nook': NOOK,
    # the setBool success after everything: its block is the return block's prev (no early return)
    'end': [(SB, '\tif (setBoolOption(opt, val) != 1) {\n'),
            (END, END[:-2] + '\t}\n' + NL + '}\n')],
    'endeq': [(SB, '\tif (setBoolOption(opt, val) == 1)\n\t\tgoto done;\n'),
              (END, END[:-2] + 'done:\n' + NL + '}\n')],
    'macnl': [MACNL],
    # the tail tests val again: the val-null path reaches the incomplete block without the vlen
    # test, so the vlen test's incomplete edge has no call prediction
    'vv': [(PO2[0], 'if (val && vlen) {')],
    'vvn': [(PO2[0] + '\n\t\t' + UNK + '\n\t\treturn 0;\n\t}\n',
             'if (val) {\n\t\tif (vlen) {\n\t\t\t' + UNK + '\n\t\t\treturn 0;\n\t\t}\n\t}\n')],
    'vlv': [(PO2[0], 'if (vlen && val) {')],
    # attempt 19's lever on parseButtonX (after the tail landed): the caller tests s too
    'bxe': [('if (__builtin_expect(!strnicmp(s, "power", 5), 1)) {', 'if (!strnicmp(s, "power", 5)) {')],
    'bxz': [('\t\tif (__builtin_constant_p(xb.xellButton + 1)) { if (__builtin_constant_p(xb.xellButton + 2) > 0) goto z; }\n', '')],
    'bxs': [('\t\t\txb.xellButton = parseButtonX(getIniValue("xellbutton"));\n',
             '\t\t\ts = getIniValue("xellbutton");\n\t\t\tif (s)\n\t\t\t\txb.xellButton = parseButtonX(s);\n')],
    'bxs2': [('\t\t\txb.xellButton = parseButtonX(getIniValue("xellbutton"));\n',
              '\t\t\ts = getIniValue("xellbutton");\n\t\t\txb.xellButton = s ? parseButtonX(s) : 0;\n')],
    # measurement only: the vlen edge as a cold label (first match), so -p N moves setBool alone
    'coldu': [(PO2[0], 'if (vlen) {\n\t\tif (0) goto cu;\ncu: __attribute__((cold));\n')],
    # macid's success shares the setBool block: not dominated by the setBool test (no call heuristic)
    'lab': [(SB, '\tif (setBoolOption(opt, val) == 1) {\ndone:\n' + NL.replace('\t', '\t\t') + '\t}\n'),
            MACNL],
}


def tail(t):
    VARIANTS[t[0]] = [PO1] * ('1' in t[1]) + [(TAIL, t[2])]


def build(name):
    t = SRC
    for part in name.split('+'):
        for old, new in VARIANTS[part]:
            if old not in t:
                raise KeyError('edit missing in %s: %r' % (part, old[:60]))
            t = t.replace(old, new, 1)
    return t


def dumps(text, d, flags):
    os.makedirs(d, exist_ok=True)
    p = os.path.join(d, 'o.c')
    with open(p, 'w', newline='\n') as f:
        f.write('#line 1 "options.c"\n' + text)
    env = dict(os.environ)
    tc = os.path.join(optlib.R, 'tools', 'toolchain-4745', 'mingw32', 'bin')
    env['PATH'] = tc + os.pathsep + env['PATH']
    subprocess.run([os.path.join(tc, 'gcc.exe'), '-c', '-O3'] + flags +
                   ['-I' + os.path.join(optlib.R, 'src'), 'o.c', '-o', 'o.o',
                    '-fdump-tree-profile_estimate-details', '-fdump-tree-optimized-blocks-details', '-fdump-rtl-jump2-blocks-details',
                    '-fdump-rtl-bbro-details', '-fdump-tree-vrp1-details'], cwd=d, env=env)


def main():
    a = sys.argv[1:]
    flags = optlib.P83
    d = out = None
    v = False
    if '-np' in a:
        a.remove('-np'); flags = []
    if '-p' in a:
        i = a.index('-p'); flags = ['--param', 'builtin-expect-probability=' + a[i + 1]]; del a[i:i + 2]
    if '-d' in a:
        i = a.index('-d'); d = a[i + 1]; del a[i:i + 2]
    if '-o' in a:
        i = a.index('-o'); out = a[i + 1]; del a[i:i + 2]
    if '-v' in a:
        a.remove('-v'); v = True
    names = a or list(VARIANTS)

    def one(n):
        try:
            t = build(n)
        except KeyError as e:
            return n, {'compile': str(e)}
        return n, optlib.score_text(t, flags)
    if not v:
        with ThreadPoolExecutor(6) as ex:
            for n, r in ex.map(one, names):
                print('%-14s %s' % (n, optlib.fmt(r)), flush=True)
    else:
        for n in names:
            optlib.vdiff(build(n), flags, '_parseOption')
    if out:
        with open(out, 'w', newline='\n') as f:
            f.write(build(names[-1]))
    if d:
        dumps(build(names[-1]), d, flags)


if __name__ == '__main__':
    main()
