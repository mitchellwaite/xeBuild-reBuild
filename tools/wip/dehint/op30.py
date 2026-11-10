#!/usr/bin/env python3
"""Attempt 30: variants of src/options.c for the whole-function model.

python tools/wip/dehint/op30.py [-d] [-o out.c] [-v fn] variant ..
  a variant is names from V joined by `+`, applied in order to commit 80a383bf's
  src/options.c (the 15-trick source; `src` alone is today's file).
    dzall   the dummy group gone (memset, both asm gotos, rev feeds, dz1/dz2)
    natx    parseButtonX gone: the xellbutton site calls parseButton
    nat     dzall+natx (no trick left in the file)
    intb..  optIniInt forms called directly, the INI_INT macro gone (ifnb..: the form
            alone; icalls: the calls alone)
    pbfoldi parseButtonPart folded back into parseButton (after int*; pbfold before)
    f_SITE  OPT <-> optIniBoolG at one site; allopt: every site through OPT
  -d also writes p1/run.sh dumps (plain -O3) under build/v/aio_p1/a30_<variant>."""
import os, re, subprocess, sys
from concurrent.futures import ThreadPoolExecutor
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import optlib

R = optlib.R
# the variants are edits on the source attempt 30 started from (commit 80a383bf: 15 tricks);
# today's src/options.c is `nat+intb+pbfoldi` with new comments
BASE_REV = '80a383bf'
SRC = subprocess.run(['git', 'show', BASE_REV + ':src/options.c'], cwd=R, capture_output=True).stdout.decode().replace('\r\n', '\n')

MS = '\t\t\t\t\t__builtin_memset(s, 0, __builtin_constant_p(xb.macid[1] + 9));\n'
AG1 = '\t\t\t\t\t__asm__ goto ("" :::: dz1);\n'
AG2 = '\t\t\t\t__asm__ goto ("" :::: dz2);\n'
i0 = SRC.index('\t\t\t/* dead feeds that key the dummies')
i1 = SRC.index('\t\t}\n\t}\n\treturn;\n\t/* the dummy heap')
FEEDS = SRC[i0:i1]
END = 'dz1:\n\t__builtin_unreachable();\n}\n'
TAIL = SRC[i1:SRC.index(END) + len(END)]
PBX0 = SRC.index('/* applyIniOptions\' copy of parseButton for xellbutton')
PBX1 = SRC.index('int parseButton(const char *s)\n')
PBX = SRC[PBX0:PBX1]
XCALL = 'xb.xellButton = parseButtonX(getIniValue("xellbutton"));'
for x in (MS, AG1, AG2, FEEDS, TAIL, PBX, XCALL):
    assert SRC.count(x) == 1, x[:40]

V = {}
V['base'] = []
V['dzall'] = [(MS, ''), (AG1, ''), (AG2, ''), (FEEDS, ''), (TAIL, '\t\t}\n\t}\n}\n')]
V['natx'] = [(PBX, ''), (XCALL, XCALL.replace('parseButtonX', 'parseButton'))]
V['nat'] = V['dzall'] + V['natx']

# optIniInt forms, called directly (the INI_INT macro goes)
IH = 'int optIniInt(const char *name, int def)\n{\n'
II0 = SRC.index(IH)
IFN = SRC[II0:SRC.index('\n}\n', II0) + 3]
IW = '\t\tlog_printf(0, "***** WARNING: options.ini setting \'%s\' invalid value \'%s\', discarding!\\n", name, bad);\n'
assert IW in IFN
IM0 = SRC.index('/* optIniInt\'s body for applyIniOptions\' int options, as a macro.')
IMAC = SRC[IM0:SRC.index('#define OPT(')]
IFORMS = {
    # early return on the good path (10.1% in the callee's own profile)
    'b': IH + '\tchar *bad;\n\n\tbad = iniU32Invalid(name);\n\tif (!bad)\n\t\treturn getIniU32(name, def);\n' + IW[1:] + '\treturn def;\n}\n',
    'c': IH + '\tchar *bad;\n\tint v;\n\n\tbad = iniU32Invalid(name);\n\tif (bad) {\n' + IW + '\t\tv = def;\n\t} else\n\t\tv = getIniU32(name, def);\n\treturn v;\n}\n',
    'd': IH + '\tchar *bad;\n\tint v;\n\n\tbad = iniU32Invalid(name);\n\tif (!bad)\n\t\tv = getIniU32(name, def);\n\telse {\n' + IW + '\t\tv = def;\n\t}\n\treturn v;\n}\n',
    'e': IH + '\tchar *bad;\n\n\tbad = iniU32Invalid(name);\n\tif (!bad)\n\t\tdef = getIniU32(name, def);\n\telse\n' + IW + '\treturn def;\n}\n',
}
ISITES = re.findall(r'\t+INI_INT\(xb\.\w+, "\w+", -?\d+\);\n', SRC)
assert len(ISITES) == 12
ICALLS = [(x, re.sub(r'INI_INT\((xb\.\w+), ("\w+"), (-?\d+)\);', r'\1 = optIniInt(\2, \3);', x)) for x in ISITES]
V['icalls'] = ICALLS + [(IMAC, '')]
for k, fn in IFORMS.items():
    V['int' + k] = [(IFN, fn)] + V['icalls']
    V['ifn' + k] = [(IFN, fn)]

# parseButtonPart folded back into parseButton (gcc's own split; needs natx)
PP0 = SRC.index('/* parseButton after its first four names')
PPART = SRC[PP0:SRC.index('int baseFileExists(const char *name)\n')]
PBODY = PPART[PPART.index('\tif (!strnicmp(s, "wirelessx", 9))'):PPART.index('\treturn b;\n}\n')]
PCALL = '\telse\n\t\tb = parseButtonPart(s, 0);\n\treturn b;\n}\n\n/* optIniInt'
V['pbfold'] = [(PPART, ''), (PCALL, '\telse ' + PBODY.lstrip('\t') + '\treturn b;\n}\n\n/* optIniInt')]
V['pbfoldi'] = [(PPART, ''), (PCALL.replace('\n\n/* optIniInt', '\n\n#define OPT('), '\telse ' + PBODY.lstrip('\t') + '\treturn b;\n}\n\n#define OPT(')]

# OPT <-> optIniBoolG per site
SITES = {
    'nomobile': ('\tOPT("nomobile", 0x20000000, 0);\n', 0x20000000),
    'noremap': ('\tOPT("noremap", 0x40000000, 0);\n', 0x40000000),
    'noecdremap': ('\tif (!(xb.bootFlags & 0x80000000)) optIniBoolG("noecdremap", 0x80000000, 0, 0);\n', 0x80000000),
    'nandmu': ('\tif (!(xb.bootFlags & (0x10000000))) optIniBoolG("nandmu", 0x10000000, 0, 0);\n', 0x10000000),
    'nosecurity': ('\tif (!(xb.bootFlags & (0x4000000))) optIniBoolG("nosecurity", 0x4000000, 0, 0);\n', 0x4000000),
    'nosusecurity': ('\tOPT("nosusecurity", 0x1000000, 0);\n', 0x1000000),
    'smcnocheck': ('\tOPT("smcnocheck", 0x200000, 0);\n', 0x200000),
    'cygnos': ('\t\tif (!(xb.bootFlags & (1))) optIniBoolG("cygnos", 1, 0, 0);\n', 1),
    'demon': ('\t\tOPT("demon", 8, 0);\n', 8),
    'patchsmc': ('\t\tOPT("patchsmc", 0x8000000, 0);\n', 0x8000000),
    'smcnoeject': ('\t\tif (!(xb.bootFlags & (0x400000))) optIniBoolG("smcnoeject", 0x400000, 0, 0);\n', 0x400000),
    'smcnoblink': ('\t\tOPT("smcnoblink", 0x800000, 0);\n', 0x800000),
    'nodvd': ('\t\tOPT("nodvd", 2, 4);\n', 2),
}
GSITES = [n for n, (line, bit) in SITES.items() if 'optIniBoolG' in line]
for n, (line, bit) in SITES.items():
    assert line in SRC, n
    ind = line[:len(line) - len(line.lstrip('\t'))]
    clear = 4 if n == 'nodvd' else 0
    hx = '0x%x' % bit if bit > 9 else str(bit)
    g = '%sif (!(xb.bootFlags & (%s))) optIniBoolG("%s", %s, %d, 0);\n' % (ind, hx, n, hx, clear)
    o = '%sOPT("%s", %s, %d);\n' % (ind, n, hx, clear)
    V['f_' + n] = [(line, o if 'optIniBoolG' in line else g)]
G0 = SRC.index('/* optIniBool for noecdremap, nandmu, nosecurity, cygnos and smcnoeject.')
GFN = SRC[G0:SRC.index('int optIniInt(const char *name, int def)\n')]
V['allopt'] = [x for n in GSITES for x in V['f_' + n]] + [(GFN, '')]


def apply(text, names):
    for n in names.split('+'):
        for a, b in V[n]:
            assert a in text, (n, a[:50])
            text = text.replace(a, b, 1)
    return text


def dump(text, tag):
    p = os.path.join(optlib.BUILD, 'a30', tag + '.c')
    os.makedirs(os.path.dirname(p), exist_ok=True)
    open(p, 'w', newline='\n').write(text)
    env = dict(os.environ, GFL='-O3')
    q = subprocess.run(['sh', os.path.join(R, 'tools', 'wip', 'aio', 'p1', 'run.sh'), p, tag],
                       capture_output=True, text=True, env=env)
    return q.stdout.strip().splitlines()[-1] if q.stdout.strip() else q.stderr[-200:]


def score(text):
    r = optlib.score_text(text)
    if r.get('identical'):
        return 'IDENTICAL'
    if 'total' in r:
        return '%s %s %s' % (r.get('total'), r.get('per'), ' '.join(r.get('notes', [])))
    return str(r)


def run(names, dmp=False, out=None, vfn=None):
    t = open(optlib.SRC).read() if names == 'src' else apply(SRC, names)
    if out:
        open(out, 'w', newline='\n').write(t)
    if vfn is not None:
        optlib.vdiff(t, only=vfn or None)
        return names, None
    s = score(t)
    if dmp:
        tag = 'a30_' + names.replace('+', '_').replace(':', '-')
        s += '  [dump %s: %s]' % (tag, dump(t, tag))
    return names, s


if __name__ == '__main__':
    a = sys.argv[1:]
    dmp = '-d' in a
    if dmp:
        a.remove('-d')
    out = None
    if '-o' in a:
        i = a.index('-o'); out = a[i + 1]; del a[i:i + 2]
    vfn = None
    if '-v' in a:
        i = a.index('-v')
        vfn = a[i + 1] if i + 1 < len(a) and a[i + 1] not in V and '+' not in a[i + 1] else ''
        del a[i:i + (2 if vfn else 1)]
    if vfn is not None or out:
        for n in a:
            run(n, dmp, out, vfn)
        sys.exit()
    with ThreadPoolExecutor(8) as ex:
        for n, s in ex.map(lambda n: run(n, dmp), a):
            print('%-40s %s' % (n, s), flush=True)
