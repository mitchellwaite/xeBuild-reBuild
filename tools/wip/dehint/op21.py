#!/usr/bin/env python3
"""Attempt 21: small constant-table loops that gcc unrolls completely, as a source of edge
probabilities (loop exit / loop iterations predictors, cunroll's frequency scaling).

python tools/wip/dehint/op21.py [-np|-p N] [-m] [-d dir] [-o out.c] [-v fn] variant ..
  a variant is `px:NAME` (parseButtonX replaced by BODIES[NAME]), or a name in VARIANTS,
  combined with `+`.
  -m      prints op20's xellbutton site counts too
  -d dir  dumps (profile_estimate, cunrolli, cunroll, optimized, bbro ...) of the last variant
  -o file writes the last variant's source
  -v fn   prints the diff of function fn"""
import os, re, subprocess, sys
from concurrent.futures import ThreadPoolExecutor
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import optlib
import op20

SRC = optlib.read_src(optlib.SRC)
PBX = op20.PBX

TAB4 = ('static const struct {\n\tconst char *name;\n\tint len;\n\tint button;\n} xellButtons[] = {\n'
        '\t{ "power", 5, 0x11 },\n\t{ "remopower", 9, 0x20 },\n\t{ "remox", 5, 0x22 },\n'
        '\t{ "winbutton", 9, 0x24 },\n};\n\n')
TAB1 = ('static const struct {\n\tconst char *name;\n\tint len;\n\tint button;\n} xellButtons[] = {\n'
        '\t{ "power", 5, 0x11 },\n};\n\n')
TAB2 = ('static const struct {\n\tconst char *name;\n\tint len;\n\tint button;\n} xellButtons[] = {\n'
        '\t{ "power", 5, 0x11 },\n\t{ "remopower", 9, 0x20 },\n};\n\n')
TAB3 = ('static const struct {\n\tconst char *name;\n\tint len;\n\tint button;\n} xellButtons[] = {\n'
        '\t{ "power", 5, 0x11 },\n\t{ "remopower", 9, 0x20 },\n\t{ "remox", 5, 0x22 },\n};\n\n')
HEAD = 'static int parseButtonX(const char *s)\n{\n'
ZF = '\t\tif (__builtin_constant_p(xb.xellButton + 1)) { if (__builtin_constant_p(xb.xellButton + 2) > 0) goto z; }\n'

LOOP_RET = ('\tint i;\n\n\tif (!s)\n\t\treturn 0;\n\tfor (i = 0; i < N; i++)\n'
            '\t\tif (!strnicmp(s, xellButtons[i].name, xellButtons[i].len))\n'
            '\t\t\treturn xellButtons[i].button;\n')
REST4 = '\treturn parseButtonPart(s, 0);\n}\n'
REST1 = ('\tif (!strnicmp(s, "remopower", 9))\n\t\treturn 0x20;\n\tif (!strnicmp(s, "remox", 5))\n'
         '\t\treturn 0x22;\n\tif (!strnicmp(s, "winbutton", 9))\n\t\treturn 0x24;\n' + REST4)
REST2 = ('\tif (!strnicmp(s, "remox", 5))\n\t\treturn 0x22;\n\tif (!strnicmp(s, "winbutton", 9))\n'
         '\t\treturn 0x24;\n' + REST4)
REST3 = '\tif (!strnicmp(s, "winbutton", 9))\n\t\treturn 0x24;\n' + REST4


def loop(tab, n, rest, core=LOOP_RET):
    return tab + HEAD + core.replace('N', str(n)) + rest


BODIES = {
    't4ret': loop(TAB4, 4, REST4),
    't1ret': loop(TAB1, 1, REST1),
    't2ret': loop(TAB2, 2, REST2),
    't3ret': loop(TAB3, 3, REST3),
    # sizeof-bounded
    't4sz': loop(TAB4, 4, REST4).replace('i < 4', 'i < sizeof(xellButtons) / sizeof(xellButtons[0])'),
}

VARIANTS = {'cur': []}

# macidSet: the one loop gcc already unrolls in applyIniOptions (cunroll, 6 copies)
MS0 = ('int macidSet(void)\n{\n\tint i;\n\n\tfor (i = 0; i < 6; i++)\n\t\tif (xb.macid[i] != 0xff)\n'
       '\t\t\treturn 1;\n\treturn 0;\n}\n')
assert MS0 in SRC


def ms(body, decl='\tint i;\n\n'):
    return 'int macidSet(void)\n{\n' + decl + body + '}\n'


MSF = {
    'brk': ms('\tfor (i = 0; i < 6; i++)\n\t\tif (xb.macid[i] != 0xff)\n\t\t\tbreak;\n\treturn i < 6;\n'),
    'brkne': ms('\tfor (i = 0; i < 6; i++)\n\t\tif (xb.macid[i] != 0xff)\n\t\t\tbreak;\n\treturn i != 6;\n'),
    'cond': ms('\tfor (i = 0; i < 6 && xb.macid[i] == 0xff; i++)\n\t\t;\n\treturn i < 6;\n'),
    'whc': ms('\ti = 0;\n\twhile (i < 6 && xb.macid[i] == 0xff)\n\t\ti++;\n\treturn i < 6;\n'),
    'set': ms('\tfor (i = 0; i < 6; i++)\n\t\tif (xb.macid[i] != 0xff)\n\t\t\tset = 1;\n\treturn set;\n',
              '\tint i, set = 0;\n\n'),
    'setb': ms('\tfor (i = 0; i < 6; i++)\n\t\tif (xb.macid[i] != 0xff) {\n\t\t\tset = 1;\n\t\t\tbreak;\n\t\t}\n\treturn set;\n',
               '\tint i, set = 0;\n\n'),
    'cont': ms('\tfor (i = 0; i < 6; i++) {\n\t\tif (xb.macid[i] == 0xff)\n\t\t\tcontinue;\n\t\treturn 1;\n\t}\n\treturn 0;\n'),
    'wh': ms('\ti = 0;\n\twhile (i < 6) {\n\t\tif (xb.macid[i] != 0xff)\n\t\t\treturn 1;\n\t\ti++;\n\t}\n\treturn 0;\n'),
    'do': ms('\ti = 0;\n\tdo {\n\t\tif (xb.macid[i] != 0xff)\n\t\t\treturn 1;\n\t} while (++i < 6);\n\treturn 0;\n'),
    'ptr': ms('\tfor (p = xb.macid; p < xb.macid + 6; p++)\n\t\tif (*p != 0xff)\n\t\t\treturn 1;\n\treturn 0;\n',
              '\tconst uint8_t *p;\n\n'),
    'lt': ms('\tfor (i = 0; i < 6; i++)\n\t\tif (xb.macid[i] < 0xff)\n\t\t\treturn 1;\n\treturn 0;\n'),
    'sz': ms('\tfor (i = 0; i < sizeof(xb.macid); i++)\n\t\tif (xb.macid[i] != 0xff)\n\t\t\treturn 1;\n\treturn 0;\n'),
    'and': ms('\tfor (i = 0; i < 6; i++)\n\t\tm &= xb.macid[i];\n\treturn m != 0xff;\n', '\tint i;\n\tuint8_t m = 0xff;\n\n'),
    'rev': ms('\tfor (i = 6; i--; )\n\t\tif (xb.macid[i] != 0xff)\n\t\t\treturn 1;\n\treturn 0;\n'),
    'eqr': ms('\tfor (i = 0; i < 6; i++)\n\t\tif (!(xb.macid[i] == 0xff))\n\t\t\treturn 1;\n\treturn 0;\n'),
    'cnt': ms('\tfor (i = 0; i < 6; i++)\n\t\tif (xb.macid[i] == 0xff)\n\t\t\tn++;\n\treturn n != 6;\n', '\tint i, n = 0;\n\n'),
    'ret0': ms('\tfor (i = 0; i < 6; i++)\n\t\tif (xb.macid[i] != 0xff)\n\t\t\treturn 1;\n\treturn i != 6;\n'),
}
for k, v in MSF.items():
    VARIANTS['ms_' + k] = [(MS0, v)]

# OPT sites as a table loop (calls guarded by the bit test, so off cunroll's hot path)
OPT2 = '\tOPT("nomobile", 0x20000000, 0);\n\tOPT("noremap", 0x40000000, 0);\n'
assert OPT2 in SRC
TOPT = ('static const struct {\n\tconst char *name;\n\tuint32_t set;\n} iniOpts[] = {\n'
        '\t{ "nomobile", 0x20000000 },\n\t{ "noremap", 0x40000000 },\n};\n\n')
VARIANTS['opt2'] = [(OPT2, '\tfor (i = 0; i < 2; i++)\n\t\tOPT(iniOpts[i].name, iniOpts[i].set, 0);\n'),
                    ('void applyIniOptions(void)\n{', TOPT + 'void applyIniOptions(void)\n{')]
OPT3 = ('\tif (!(xb.bootFlags & (0x4000000))) optIniBoolG("nosecurity", 0x4000000, 0, 0);\n'
        '\tOPT("nosusecurity", 0x1000000, 0);\n\tOPT("smcnocheck", 0x200000, 0);\n')
assert OPT3 in SRC
TOPT3 = ('static const struct {\n\tconst char *name;\n\tuint32_t set;\n} iniOpts[] = {\n'
         '\t{ "nosusecurity", 0x1000000 },\n\t{ "smcnocheck", 0x200000 },\n};\n\n')
VARIANTS['opt2b'] = [(OPT3, OPT3.split('\tOPT(')[0] + '\tfor (i = 0; i < 2; i++)\n\t\tOPT(iniOpts[i].name, iniOpts[i].set, 0);\n'),
                     ('void applyIniOptions(void)\n{', TOPT3 + 'void applyIniOptions(void)\n{')]

OPTD = '\t\tOPT("demon", 8, 0);\n\t\tOPT("patchsmc", 0x8000000, 0);\n'
assert OPTD in SRC
TOPTD = ('static const struct {\n\tconst char *name;\n\tuint32_t set;\n} iniOpts[] = {\n'
         '\t{ "demon", 8 },\n\t{ "patchsmc", 0x8000000 },\n};\n\n')
VARIANTS['optd'] = [(OPTD, '\t\tfor (i = 0; i < 2; i++)\n\t\t\tOPT(iniOpts[i].name, iniOpts[i].set, 0);\n'),
                    ('void applyIniOptions(void)\n{', TOPTD + 'void applyIniOptions(void)\n{')]
OPTN = ('\t\tif (!(xb.bootFlags & (0x400000))) optIniBoolG("smcnoeject", 0x400000, 0, 0);\n'
        '\t\tOPT("smcnoblink", 0x800000, 0);\n')
assert OPTN in SRC
OPTJ = '\t\tOPT("nodvd", 2, 4);\n\t\t/* no bit of its own: it clears nodvd\'s 4 */\n\t\toptIniBool("olddvd", 0, 4, 0);\n'
assert OPTJ in SRC
TOPTJ = ('static const struct {\n\tconst char *name;\n\tuint32_t set;\n} iniOpts[] = {\n'
         '\t{ "nodvd", 2 },\n\t{ "olddvd", 0 },\n};\n\n')
VARIANTS['optj'] = [(OPTJ, '\t\tfor (i = 0; i < 2; i++)\n\t\t\tif (!(xb.bootFlags & iniOpts[i].set))\n'
                     '\t\t\t\toptIniBool(iniOpts[i].name, iniOpts[i].set, 4, 0);\n'),
                    ('void applyIniOptions(void)\n{', TOPTJ + 'void applyIniOptions(void)\n{')]

OPTG = ('\tif (!(xb.bootFlags & 0x80000000)) optIniBoolG("noecdremap", 0x80000000, 0, 0);\n'
        '\tif (!(xb.bootFlags & (0x10000000))) optIniBoolG("nandmu", 0x10000000, 0, 0);\n'
        '\tif (!(xb.bootFlags & (0x4000000))) optIniBoolG("nosecurity", 0x4000000, 0, 0);\n')
assert OPTG in SRC
GL = OPTG.split('\n')


def tabg(entries):
    return ('static const struct {\n\tconst char *name;\n\tuint32_t set;\n} iniOpts[] = {\n' +
            ''.join('\t{ "%s", %s },\n' % e for e in entries) + '};\n\n')


GLOOP = '\tfor (i = 0; i < N; i++)\n\t\tif (!(xb.bootFlags & iniOpts[i].set))\n\t\t\toptIniBoolG(iniOpts[i].name, iniOpts[i].set, 0, 0);\n'
GE = [('noecdremap', '0x80000000'), ('nandmu', '0x10000000'), ('nosecurity', '0x4000000')]
VARIANTS['optg3'] = [(OPTG, GLOOP.replace('N', '3')), ('void applyIniOptions(void)\n{', tabg(GE) + 'void applyIniOptions(void)\n{')]
VARIANTS['optg12'] = [(OPTG, GLOOP.replace('N', '2') + GL[2] + '\n'),
                      ('void applyIniOptions(void)\n{', tabg(GE[:2]) + 'void applyIniOptions(void)\n{')]
VARIANTS['optg23'] = [(OPTG, GL[0] + '\n' + GLOOP.replace('N', '2')),
                      ('void applyIniOptions(void)\n{', tabg(GE[1:]) + 'void applyIniOptions(void)\n{')]

# parseOption's macid loop: its exit (1/6, loop iterations) is the competitor that the setBool
# edge must beat in connect_traces.  With the trip count unknown at profile_estimate the exit
# gets the loop exit heuristic alone (9%), below the natural setBool 9.2%.
PLOOP = ('\t\t\t\t\tfor (i = 0; i < 5; i++) {\n\t\t\t\t\t\tlog_printf(1, ":");\n'
         '\t\t\t\t\t\txb.macid[i + 1] = myatox8(val + i * 2);\n'
         '\t\t\t\t\t\tlog_printf(1, "%02x", xb.macid[i + 1]);\n\t\t\t\t\t}\n')
assert PLOOP in SRC
HLOOP = ('/* the rest of a macid after its first byte */\n'
         'static void macidRest(const char *val, int n)\n{\n\tint i;\n\n'
         '\tfor (i = 0; i < n; i++) {\n\t\tlog_printf(1, ":");\n'
         '\t\txb.macid[i + 1] = myatox8(val + i * 2);\n'
         '\t\tlog_printf(1, "%02x", xb.macid[i + 1]);\n\t}\n}\n\n')
HLOOP6 = ('/* bytes 1 .. n-1 of a macid */\n'
          'static void macidRest(const char *val, int n)\n{\n\tint i;\n\n'
          '\tfor (i = 1; i < n; i++) {\n\t\tlog_printf(1, ":");\n'
          '\t\txb.macid[i] = myatox8(val + (i - 1) * 2);\n'
          '\t\tlog_printf(1, "%02x", xb.macid[i]);\n\t}\n}\n\n')
PO = 'uint32_t parseOption(char *opt)\n{'
VARIANTS['hm5'] = [(PLOOP, '\t\t\t\t\tmacidRest(val, 5);\n'), (PO, HLOOP + PO)]
VARIANTS['hm6'] = [(PLOOP, '\t\t\t\t\tmacidRest(val, 6);\n'), (PO, HLOOP6 + PO)]
# a never-written static as the bound: promoted to read-only at IPA, folded after profile_estimate
VARIANTS['sv5'] = [(PLOOP, PLOOP.replace('i < 5', 'i < macidRestLen')),
                   (PO, 'static int macidRestLen = 5;\n\n' + PO)]
VARIANTS['sv6'] = [(PLOOP, PLOOP.replace('i < 5', 'i < macidLen - 1')),
                   (PO, 'static int macidLen = 6;\n\n' + PO)]

PL_PTR = ('\t\t\t\t\tfor (i = 0; i < macidRestLen; i++) {\n\t\t\t\t\t\tlog_printf(1, ":");\n'
          '\t\t\t\t\t\tm[i] = myatox8(val + i * 2);\n'
          '\t\t\t\t\t\tlog_printf(1, "%02x", m[i]);\n\t\t\t\t\t}\n')
VARIANTS['sp5'] = [(PLOOP, '\t\t\t\t\tm = &xb.macid[1];\n' + PL_PTR),
                   ('\tint i, len, vlen, ok;\n', '\tint i, len, vlen, ok;\n\tuint8_t *m;\n'),
                   (PO, 'static int macidRestLen = 5;\n\n' + PO)]
VARIANTS['spc5'] = [(PLOOP, '\t\t\t\t\tm = &xb.macid[1];\n' + PL_PTR.replace('macidRestLen', '5')),
                    ('\tint i, len, vlen, ok;\n', '\tint i, len, vlen, ok;\n\tuint8_t *m;\n')]
HPTR = ('/* the rest of a macid after its first byte */\n'
        'static void macidRest(uint8_t *mac, const char *val, int n)\n{\n\tint i;\n\n'
        '\tfor (i = 0; i < n; i++) {\n\t\tlog_printf(1, ":");\n'
        '\t\tmac[i] = myatox8(val + i * 2);\n'
        '\t\tlog_printf(1, "%02x", mac[i]);\n\t}\n}\n\n')
VARIANTS['hp5'] = [(PLOOP, '\t\t\t\t\tmacidRest(&xb.macid[1], val, 5);\n'), (PO, HPTR + PO)]
VARIANTS['hp5b'] = [(PLOOP, '\t\t\t\t\tmacidRest(xb.macid + 1, val, 5);\n'), (PO, HPTR + PO)]

VV = ('\tif (val && vlen) {\n\t\tlog_printf(1, "\\n\\n***** ERROR: unknown option \'%s\' with value \'%s\' provided on the command line!\\n", opt, val);\n'
      '\t\treturn 0;\n\t}\n')
assert VV in SRC, 'vv'
VARIANTS['vvn'] = [(VV, '\tif (val) {\n\t\tif (vlen) {\n\t\t\tlog_printf(1, "\\n\\n***** ERROR: unknown option \'%s\' with value \'%s\' provided on the command line!\\n", opt, val);\n'
                    '\t\t\treturn 0;\n\t\t}\n\t}\n')]
VARIANTS['vvl'] = [(VV, VV.replace('val && vlen', 'vlen && val'))]

# parseOption's '=' loop forms (its exits set the 450 that reaches the setBool test)
EQ_END = '\t\t\ti = len + 1;\n\t\t}\n\t}\n\tif (len == strlen(opt))\n'
assert EQ_END in SRC
EQ_HEAD = '\tlen = strlen(opt);\n\tfor (i = 0; i < len; i++) {\n\t\tif (opt[i] == \'=\') {\n'
assert EQ_HEAD in SRC
VARIANTS['eqbrk'] = [(EQ_END, '\t\t\tbreak;\n\t\t}\n\t}\n\tif (len == strlen(opt))\n')]
VARIANTS['eqwh'] = [(EQ_HEAD, '\tlen = strlen(opt);\n\ti = 0;\n\twhile (i < len) {\n\t\tif (opt[i] == \'=\') {\n'),
                    (EQ_END, '\t\t\ti = len;\n\t\t}\n\t\ti++;\n\t}\n\tif (len == strlen(opt))\n')]
VARIANTS['eqnv'] = [(EQ_HEAD, '\tlen = strlen(opt);\n\tfor (i = 0; i < len && !val; i++) {\n\t\tif (opt[i] == \'=\') {\n'),
                    (EQ_END, '\t\t}\n\t}\n\tif (len == strlen(opt))\n')]
VARIANTS['eqlen'] = [(EQ_END, '\t\t\ti = len;\n\t\t}\n\t}\n\tif (len == strlen(opt))\n')]

# setBool success without the early-return prediction, its "\n" block still first
SB = '\tif (__builtin_expect(setBoolOption(opt, val) == 1, 0)) {\n\t\tlog_printf(1, "\\n");\n\t\treturn 1;\n\t}\n'
assert SB in SRC, 'sb'
TAILR = '\treturn 0;\nbad:\n'
assert TAILR in SRC
VARIANTS['n1'] = [(SB, '\tif (setBoolOption(opt, val) == 1)\n\t\tlog_printf(1, "\\n");\n\telse {\n'),
                  (TAILR, '\treturn 0;\n\t}\n\treturn 1;\nbad:\n')]
VARIANTS['n1e'] = [(SB, '\tif (setBoolOption(opt, val) == 1)\n\t\tlog_printf(1, "\\n");\n\telse {\n'),
                   (TAILR, '\treturn 0;\n\t}\n\treturn 1;\nbad:\n'), ('if (setBoolOption(opt, val) == 1)', 'if (__builtin_expect(setBoolOption(opt, val) == 1, 0))')]
VARIANTS['n2'] = [(SB, '\tif (setBoolOption(opt, val) != 1) {\n'),
                  (TAILR, '\treturn 0;\n\t}\n\tlog_printf(1, "\\n");\n\treturn 1;\nbad:\n')]

EQ_BODY = SRC[SRC.index(EQ_HEAD):SRC.index(EQ_END) + len(EQ_END)]
EQ_SW = (EQ_BODY.replace("\t\tif (opt[i] == '=') {\n", "\t\tswitch (opt[i]) {\n\t\tcase '=':\n")
         .replace('\t\t\ti = len + 1;\n\t\t}\n\t}\n', '\t\t\ti = len + 1;\n\t\t\tbreak;\n\t\t}\n\t}\n'))
VARIANTS['eqsw'] = [(EQ_BODY, EQ_SW)]
VARIANTS['eqne'] = [(EQ_BODY, EQ_BODY.replace("\t\tif (opt[i] == '=') {\n", "\t\tif (opt[i] != '=')\n\t\t\tcontinue;\n\t\t{\n"))]

import op13
for k, v in op13.RM.items():
    VARIANTS.setdefault(k, v)


def build(name):
    t = SRC
    for part in name.split('+'):
        if part.startswith('px:'):
            t = t.replace(PBX, BODIES[part[3:]], 1)
            continue
        for old, new in VARIANTS[part]:
            if old not in t:
                raise KeyError('edit missing in %s: %r' % (part, old[:60]))
            t = t.replace(old, new, 1)
    return t


DUMPS = ['-fdump-tree-profile_estimate-details', '-fdump-tree-cunrolli-details',
         '-fdump-tree-cunroll-details', '-fdump-tree-ch2-details', '-fdump-tree-optimized-blocks-details',
         '-fdump-rtl-bbro-details', '-fdump-tree-vrp1-details', '-fdump-ipa-inline-details']


def dumps(text, d, flags):
    os.makedirs(d, exist_ok=True)
    p = os.path.join(d, 'o.c')
    with open(p, 'w', newline='\n') as f:
        f.write('#line 1 "options.c"\n' + text)
    env = dict(os.environ)
    tc = os.path.join(optlib.R, 'tools', 'toolchain-4745', 'mingw32', 'bin')
    env['PATH'] = tc + os.pathsep + env['PATH']
    subprocess.run([os.path.join(tc, 'gcc.exe'), '-c', '-O3'] + flags +
                   ['-I' + os.path.join(optlib.R, 'src'), 'o.c', '-o', 'o.o'] + DUMPS, cwd=d, env=env)


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
    names = a or list(VARIANTS)

    def one(n):
        try:
            t = build(n)
        except KeyError as e:
            return n, {'compile': str(e)}, ''
        return n, optlib.score_text(t, flags), (op20.metric(t, flags) if m else '')
    if not vf:
        with ThreadPoolExecutor(6) as ex:
            for n, r, mm in ex.map(one, names):
                print('%-28s %s %s' % (n, optlib.fmt(r), mm), flush=True)
    else:
        for n in names:
            optlib.vdiff(build(n), flags, vf)
    if out:
        with open(out, 'w', newline='\n') as f:
            f.write(build(names[-1]))
    if d:
        dumps(build(names[-1]), d, flags)


if __name__ == '__main__':
    main()
