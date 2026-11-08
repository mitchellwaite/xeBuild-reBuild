#!/usr/bin/env python3
"""Attempt 22: po1 (parseOption's setBool __builtin_expect) on top of attempt 21's sp5/hp5 + vvn.

python tools/wip/dehint/op22.py [-np|-p N] [-d dir] [-o out.c] [-v fn] variant ..
  a variant is op21 names and the names in VARIANTS here, joined by `+` (applied in order).
  Prints the score with parseOption's line count first.
  -d dir  dumps (profile_estimate, vrp1, optimized, bbro) of the last variant
  -o file writes the last variant's source
  -v fn   prints the diff of function fn"""
import os, sys
from concurrent.futures import ThreadPoolExecutor
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import optlib
import op21

SRC = op21.SRC
V = {}

SB = op21.SB  # the setBool test with the expect
SBP = SB.replace('__builtin_expect(setBoolOption(opt, val) == 1, 0)', 'setBoolOption(opt, val) == 1')
PO = 'uint32_t parseOption(char *opt)\n{'


def helper(text, call):
    return [(SB, call), (PO, text + PO)]


# setBool test as a helper (attempt 12's forms), now with the competitor and the unknown fixed
V['h1'] = helper('static int boolOption(char *opt, char *val)\n{\n\tif (setBoolOption(opt, val) == 1) {\n'
                 '\t\tlog_printf(1, "\\n");\n\t\treturn 1;\n\t}\n\treturn 0;\n}\n\n',
                 '\tif (boolOption(opt, val))\n\t\treturn 1;\n')
V['h2'] = helper('static int boolOption(char *opt, char *val)\n{\n\tint r = setBoolOption(opt, val);\n\n'
                 '\tif (r == 1)\n\t\tlog_printf(1, "\\n");\n\treturn r;\n}\n\n',
                 '\tif (boolOption(opt, val) == 1)\n\t\treturn 1;\n')
V['h2b'] = helper('static int boolOption(char *opt, char *val)\n{\n\tint r = setBoolOption(opt, val);\n\n'
                  '\tif (r == 1)\n\t\tlog_printf(1, "\\n");\n\treturn r == 1;\n}\n\n',
                  '\tif (boolOption(opt, val))\n\t\treturn 1;\n')
V['h3'] = helper('static int boolOption(char *opt, char *val)\n{\n\tif (setBoolOption(opt, val) != 1)\n'
                 '\t\treturn 0;\n\tlog_printf(1, "\\n");\n\treturn 1;\n}\n\n',
                 '\tif (boolOption(opt, val))\n\t\treturn 1;\n')
V['h4'] = helper('static int boolOption(char *opt, char *val)\n{\n\tint ok = 0;\n\n\tif (setBoolOption(opt, val) == 1) {\n'
                 '\t\tlog_printf(1, "\\n");\n\t\tok = 1;\n\t}\n\treturn ok;\n}\n\n',
                 '\tif (boolOption(opt, val))\n\t\treturn 1;\n')
V['h1u'] = [(a, b.replace('static int boolOption', 'static uint32_t boolOption')) for a, b in V['h1']]
V['h1b'] = [(a, b.replace('static int boolOption', 'static _Bool boolOption')) for a, b in V['h1']]
V['h1r'] = helper('static int boolOption(char *opt, char *val)\n{\n\tif (setBoolOption(opt, val) == 1) {\n'
                  '\t\tlog_printf(1, "\\n");\n\t\treturn 1;\n\t}\n\treturn 0;\n}\n\n',
                  '\tif (boolOption(opt, val) == 1)\n\t\treturn 1;\n')

# emulation only (not candidates): an expect on the val test, so -p sets P(val) with po1 on
VT = '\t\treturn 1;\n\t}\n\tif (val) {\n\t\tif (!stricmp(opt, "cputemp")) {\n'
assert VT in SRC
V['xval'] = [(VT, VT.replace('if (val) {', 'if (__builtin_expect(val != 0, 1)) {'))]
# the '=' test with an expect: -p sets P('=')
EQT = "\t\tif (opt[i] == '=') {\n"
assert EQT in SRC
V['xeq'] = [(EQT, "\t\tif (__builtin_expect(opt[i] == '=', 1)) {\n")]
V['xeq0'] = [(EQT, "\t\tif (__builtin_expect(opt[i] == '=', 0)) {\n")]

# the setBool success at the very end (after bad), reached by goto: its block is then the
# return block's next_bb, so no early-return prediction (13.7%); the "\n" literal moves?
BADT = ('bad:\n\tlog_printf(1, "\\n\\n***** ERROR: parsing option \'%s\', value \'%s\' is incorrect!\\n", opt, val);\n'
        '\treturn 0;\n}\n')
assert BADT in SRC
V['gd'] = [(SB, '\tif (setBoolOption(opt, val) == 1)\n\t\tgoto done;\n'),
           (BADT, BADT[:-2] + 'done:\n\tlog_printf(1, "\\n");\n\treturn 1;\n}\n')]
# the same with the whole rest inside `!= 1` and done after bad
V['gd2'] = [(SB, '\tif (setBoolOption(opt, val) != 1) {\n'),
            (BADT, BADT[:-2] + '\t}\n\tlog_printf(1, "\\n");\n\treturn 1;\n}\n')]

# the "\n" block early but not going straight to the return block: a join that tests a result
DECL = '\tint i, len, vlen, ok;\n'
assert DECL in SRC
V['rv'] = [(DECL, '\tint i, len, vlen, ok, set;\n')]
V['a1'] = V['rv'] + [(SB, '\tset = setBoolOption(opt, val);\n\tif (set == 1)\n\t\tlog_printf(1, "\\n");\n'
                          '\tif (set == 1)\n\t\treturn 1;\n')]
V['a2'] = [(SB, '\tok = 0;\n\tif (setBoolOption(opt, val) == 1) {\n\t\tlog_printf(1, "\\n");\n\t\tok = 1;\n\t}\n'
                '\tif (ok)\n\t\treturn 1;\n')]
V['a3'] = V['rv'] + [(SB, '\tset = setBoolOption(opt, val) == 1;\n\tif (set)\n\t\tlog_printf(1, "\\n");\n'
                          '\tif (set)\n\t\treturn 1;\n')]
V['a1x'] = V['rv'] + [(SB, '\tset = setBoolOption(opt, val);\n\tif (set == 1)\n\t\tlog_printf(1, "\\n");\n'
                           '\tif (__builtin_expect(set == 1, 0))\n\t\treturn 1;\n')]
# the "\n" arm and the value options as if / else if, the setBool result tested again after
# them (its join is threaded away by VRP1): the val test then gets bb11's whole false share
VHEAD = '\tif (val) {\n\t\tif (!stricmp(opt, "cputemp")) {\n'
assert VHEAD in SRC
CEND = '\t\t\txb.bootFlags |= 0x2000000;\n\t\t\treturn 1;\n\t\t}\n\t}\n'
assert CEND in SRC
V['c1'] = V['rv'] + [(SB + VHEAD, '\tset = setBoolOption(opt, val);\n\tif (set == 1)\n\t\tlog_printf(1, "\\n");\n'
                                  '\telse if (val) {\n\t\tif (!stricmp(opt, "cputemp")) {\n'),
                     (CEND, CEND + '\tif (set == 1)\n\t\treturn 1;\n')]
V['c2'] = V['rv'] + [(SB + VHEAD, '\tset = setBoolOption(opt, val) == 1;\n\tif (set)\n\t\tlog_printf(1, "\\n");\n'
                                  '\telse if (val) {\n\t\tif (!stricmp(opt, "cputemp")) {\n'),
                     (CEND, CEND + '\tif (set)\n\t\treturn 1;\n')]
V['c3'] = [(SB + VHEAD, '\tok = setBoolOption(opt, val);\n\tif (ok == 1)\n\t\tlog_printf(1, "\\n");\n'
                        '\telse if (val) {\n\t\tif (!stricmp(opt, "cputemp")) {\n'),
           (CEND, CEND + '\tif (ok == 1)\n\t\treturn 1;\n')]
V['c4'] = V['rv'] + [(SB + VHEAD, '\tset = 0;\n\tif (setBoolOption(opt, val) == 1) {\n\t\tlog_printf(1, "\\n");\n\t\tset = 1;\n'
                                  '\t} else if (val) {\n\t\tif (!stricmp(opt, "cputemp")) {\n'),
                     (CEND, CEND + '\tif (set)\n\t\treturn 1;\n')]
V['c5'] = [(SB + VHEAD, '\tok = 0;\n\tif (setBoolOption(opt, val) == 1) {\n\t\tlog_printf(1, "\\n");\n\t\tok = 1;\n'
                        '\t} else if (val) {\n\t\tif (!stricmp(opt, "cputemp")) {\n'),
           (CEND, CEND + '\tif (ok)\n\t\treturn 1;\n')]
V['vl'] = [(op21.VV, op21.VV.replace('val && vlen', 'vlen'))]
V['b1'] = V['rv'] + [(SB, '\tset = setBoolOption(opt, val);\n\tif (set == 1) {\n\t\tlog_printf(1, "\\n");\n'
                          '\t\treturn set;\n\t}\n')]
V['b2'] = V['rv'] + [(SB, '\tset = setBoolOption(opt, val);\n\tif (set == 1) {\n\t\tlog_printf(1, "\\n");\n'
                          '\t\tif (set)\n\t\t\treturn 1;\n\t}\n')]

VARS = dict(op21.VARIANTS)
for k, v in V.items():
    assert k not in VARS, k
    VARS[k] = v


def build(name):
    t = SRC
    for part in name.split('+'):
        if part.startswith('px:'):
            t = t.replace(op21.PBX, op21.BODIES[part[3:]], 1)
            continue
        for old, new in VARS[part]:
            if old not in t:
                raise KeyError('edit missing in %s: %r' % (part, old[:70]))
            t = t.replace(old, new, 1)
    return t


KEYS = [('C', '"cputemp")'), ('G', 'Using GPUTEMP'), ('nl', '(1, "\\n")'), ('unk', 'with value'),
        ('inc', 'unknown or incomplete')]


def metric(text, flags):
    """block frequencies in parseOption's optimized dump: C = the cputemp head (needs < 285),
    G = gputemp's success log (needs <= 27), nl = the "\n" blocks, unk = unknown (< 57), inc"""
    import re, tempfile, subprocess
    d = tempfile.mkdtemp(dir=optlib.BUILD, prefix='m')
    p = os.path.join(d, 'o.c')
    with open(p, 'w', newline='\n') as f:
        f.write('#line 1 "options.c"\n' + text)
    env = dict(os.environ)
    tc = os.path.join(optlib.R, 'tools', 'toolchain-4745', 'mingw32', 'bin')
    env['PATH'] = tc + os.pathsep + env['PATH']
    subprocess.run([os.path.join(tc, 'gcc.exe'), '-c', '-O3'] + flags + ['-I' + os.path.join(optlib.R, 'src'),
                    'o.c', '-o', 'o.o', '-fdump-tree-optimized-blocks-details'], cwd=d, env=env)
    fn = [x for x in os.listdir(d) if x.endswith('optimized')][0]
    t = open(os.path.join(d, fn)).read()
    optlib.cleanup(d)
    t = t[t.index(';; Function parseOption'):]
    t = t[:t.index(';; Function', 10)]
    blocks = re.split(r'\n;;   basic block ', t)[1:]
    res = {}
    for b in blocks:
        fr = int(re.search(r'freq (\d+)', b).group(1))
        for k, pat in KEYS:
            if pat in b:
                res.setdefault(k, []).append(fr)
    return ' '.join('%s=%s' % (k, ','.join(map(str, res.get(k, [])))) for k, _ in KEYS)


def main():
    a = sys.argv[1:]
    flags = optlib.P83
    d = out = vf = None
    m = False
    if '-m' in a:
        a.remove('-m'); m = True
    if '-np' in a:
        a.remove('-np'); flags = []
    if '-p' in a:
        i = a.index('-p'); flags = ['--param', 'builtin-expect-probability=' + a[i + 1]]; del a[i:i + 2]
    if '-d' in a:
        i = a.index('-d'); d = a[i + 1]; del a[i:i + 2]
    if '-o' in a:
        i = a.index('-o'); out = a[i + 1]; del a[i:i + 2]
    if '-v' in a:
        i = a.index('-v'); vf = a[i + 1]; del a[i:i + 2]
    names = a

    def one(n):
        try:
            t = build(n)
        except KeyError as e:
            return n, {'compile': str(e)}, ''
        return n, optlib.score_text(t, flags), (metric(t, flags) if m else '')
    if not vf:
        with ThreadPoolExecutor(6) as ex:
            for n, r, mm in ex.map(one, names):
                s = optlib.fmt(r)
                po = ''
                if r.get('per') is not None:
                    po = 'po=%s ' % r['per'].get('_parseOption', 0)
                print('%-34s %s%s %s' % (n, po, s if not s.startswith(str(r.get('total'))) else s.split(' {')[0], mm), flush=True)
    else:
        for n in names:
            optlib.vdiff(build(n), flags, vf)
    if out:
        with open(out, 'w', newline='\n') as f:
            f.write(build(names[-1]))
    if d:
        op21.dumps(build(names[-1]), d, flags)


if __name__ == '__main__':
    main()
