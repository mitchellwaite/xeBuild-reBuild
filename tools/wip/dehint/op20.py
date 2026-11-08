#!/usr/bin/env python3
"""Attempt 20: attempt 19's VRP1-threading lever (a live, redundant re-test) on parseButtonX's
z feed (bxz) and other block-count tricks.

python tools/wip/dehint/op20.py [-np|-p N] [-d dir] [-o out.c] [-v fn] variant ..
  a variant is a name in VARIANTS (edits on today's src, in order; `a+b` combines), or
  `px:NAME` for a whole parseButtonX body from BODIES (z feed gone).
  -d dir  writes profile_estimate / vrp1 / optimized / bbro dumps of the last variant
  -o file writes the last variant's source
  -v fn   prints the diff of function fn (optlib.vdiff)"""
import os, re, subprocess, sys
from concurrent.futures import ThreadPoolExecutor
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import optlib

SRC = optlib.read_src(optlib.SRC)

BXZ = ('\t\tif (__builtin_constant_p(xb.xellButton + 1)) { if (__builtin_constant_p(xb.xellButton + 2) > 0) goto z; }\n', '')
BXE = ('if (__builtin_expect(!strnicmp(s, "power", 5), 1)) {', 'if (!strnicmp(s, "power", 5)) {')

i0 = SRC.index('static int parseButtonX(const char *s)\n{\n')
i1 = SRC.index('\treturn b;\n}\n', i0) + len('\treturn b;\n}\n')
PBX = SRC[i0:i1]

PW = '__builtin_expect(!strnicmp(s, "power", 5), 1)'
REST = ('if (!strnicmp(s, "remopower", 9))\n\t\t\tb = 0x20;\n\t\telse if (!strnicmp(s, "remox", 5))\n'
        '\t\t\tb = 0x22;\n\t\telse if (!strnicmp(s, "winbutton", 9))\n\t\t\tb = 0x24;\n'
        '\t\telse\n\t\t\tb = parseButtonPart(s, 0);\n')
HEAD = 'static int parseButtonX(const char *s)\n{\n\tint b = 0;\n\n'


def body(code):
    return HEAD + code + '\treturn b;\n}\n'


BODIES = {
    # natural (no z feed)
    'nat': body('\tif (!s)\n\t\treturn 0;\n\tif (' + PW + ') {\n\t\tb = 0x11;\n\t} else {\n\t\t' + REST + '\t}\n'),
    # s tested with power, then again for the rest
    'sand': body('\tif (s && ' + PW + ')\n\t\tb = 0x11;\n\telse if (s) {\n\t\t' + REST + '\t}\n'),
    # s re-tested on every name
    'sall': body('\tif (s && ' + PW + ')\n\t\tb = 0x11;\n'
                 '\telse if (s && !strnicmp(s, "remopower", 9))\n\t\tb = 0x20;\n'
                 '\telse if (s && !strnicmp(s, "remox", 5))\n\t\tb = 0x22;\n'
                 '\telse if (s && !strnicmp(s, "winbutton", 9))\n\t\tb = 0x24;\n'
                 '\telse if (s)\n\t\tb = parseButtonPart(s, 0);\n'),
    # nested: s around power; s again around the rest
    'snest': body('\tif (s) {\n\t\tif (' + PW + ')\n\t\t\tb = 0x11;\n\t}\n\tif (!b && s) {\n\t\t' + REST + '\t}\n'),
    'snest2': body('\tif (s) {\n\t\tif (' + PW + ')\n\t\t\tb = 0x11;\n\t}\n\tif (s && !b) {\n\t\t' + REST + '\t}\n'),
    # flag form: b re-tested
    'bflag': body('\tif (!s)\n\t\treturn 0;\n\tif (' + PW + ')\n\t\tb = 0x11;\n\tif (!b) {\n\t\t' + REST + '\t}\n'),
    # !s re-tested at the power-fail head
    'srt': body('\tif (s && ' + PW + ')\n\t\tb = 0x11;\n\telse if (!s)\n\t\treturn 0;\n\telse {\n\t\t' + REST + '\t}\n'),
    # s tested at the end
    'send': body('\tif (s) {\n\t\tif (' + PW + ')\n\t\t\tb = 0x11;\n\t\telse {\n\t\t\t' + REST.replace('\n\t\t', '\n\t\t\t') + '\t\t}\n\t}\n'),
    # power result as a flag tested with s
    'pflag': body('\tint p = s && ' + PW + ';\n\n\tif (p)\n\t\tb = 0x11;\n\telse if (s) {\n\t\t' + REST + '\t}\n'),
}

CALL = '\t\t\txb.xellButton = parseButtonX(getIniValue("xellbutton"));\n\t\t\tif (!xb.xellButton) {\n'
assert CALL in SRC


def call(code):
    return [(CALL, code)]


# each arm returns (early returns everywhere)
BODIES['ret'] = ('static int parseButtonX(const char *s)\n{\n\tif (!s)\n\t\treturn 0;\n'
                 '\tif (' + PW + ')\n\t\treturn 0x11;\n\tif (!strnicmp(s, "remopower", 9))\n\t\treturn 0x20;\n'
                 '\tif (!strnicmp(s, "remox", 5))\n\t\treturn 0x22;\n\tif (!strnicmp(s, "winbutton", 9))\n'
                 '\t\treturn 0x24;\n\treturn parseButtonPart(s, 0);\n}\n')
# returns per arm, b only for the rest
BODIES['ret2'] = ('static int parseButtonX(const char *s)\n{\n\tif (!s)\n\t\treturn 0;\n'
                  '\tif (' + PW + ')\n\t\treturn 0x11;\n\tif (!strnicmp(s, "remopower", 9))\n\t\treturn 0x20;\n'
                  '\telse if (!strnicmp(s, "remox", 5))\n\t\treturn 0x22;\n\telse if (!strnicmp(s, "winbutton", 9))\n'
                  '\t\treturn 0x24;\n\telse\n\t\treturn parseButtonPart(s, 0);\n}\n')
# no null test in the body (the caller tests s)
BODIES['nos'] = body('\tif (' + PW + ') {\n\t\tb = 0x11;\n\t} else {\n\t\t' + REST + '\t}\n')

ZF = '\t\tif (__builtin_constant_p(xb.xellButton + 1)) { if (__builtin_constant_p(xb.xellButton + 2) > 0) goto z; }\n'
PWN = '!strnicmp(s, "power", 5)'
ZHEAD = 'static int parseButtonX(const char *s)\n{\n\tint b = 0;\n\n\tif (!s) {\nz:\n\t\treturn 0;\n\t}\n'
# z feed kept, power expect gone, the else arm as a re-test of b (flag form)
BODIES['zb1'] = ZHEAD + '\tif (' + PWN + ')\n\t\tb = 0x11;\n\tif (!b) {\n' + ZF + '\t\t' + REST + '\t}\n\treturn b;\n}\n'
BODIES['zb2'] = ZHEAD + '\tif (' + PWN + ')\n\t\tb = 0x11;\n\tif (b == 0) {\n' + ZF + '\t\t' + REST + '\t}\n\treturn b;\n}\n'
BODIES['zb3'] = ZHEAD + '\tif (' + PWN + ')\n\t\tb = 0x11;\n\telse if (!b) {\n' + ZF + '\t\t' + REST + '\t}\n\treturn b;\n}\n'
# the strnicmp result kept and re-tested
BODIES['zr1'] = (ZHEAD.replace('\tint b = 0;\n', '\tint b = 0, r;\n') + '\tr = strnicmp(s, "power", 5);\n\tif (!r)\n\t\tb = 0x11;\n'
                 '\tif (r) {\n' + ZF + '\t\t' + REST + '\t}\n\treturn b;\n}\n')
BODIES['zr2'] = (ZHEAD.replace('\tint b = 0;\n', '\tint b = 0, r;\n') + '\tr = strnicmp(s, "power", 5);\n\tif (!r)\n\t\tb = 0x11;\n'
                 '\telse {\n' + ZF + '\t\t' + REST + '\t}\n\treturn b;\n}\n')
# no z feed, re-test of b (bflag) with expect gone
BODIES['b1'] = HEAD + '\tif (!s)\n\t\treturn 0;\n\tif (' + PWN + ')\n\t\tb = 0x11;\n\tif (!b) {\n\t\t' + REST + '\t}\n\treturn b;\n}\n'

VARIANTS = {
    'cur': [],
    'bxz': [BXZ],
    'bxe': [BXE],
    # call site spellings
    'cs_s': call('\t\t\ts = getIniValue("xellbutton");\n\t\t\txb.xellButton = parseButtonX(s);\n\t\t\tif (!xb.xellButton) {\n'),
    'cs_ors': call('\t\t\ts = getIniValue("xellbutton");\n\t\t\txb.xellButton = parseButtonX(s);\n\t\t\tif (!s || !xb.xellButton) {\n'),
    'cs_ors2': call('\t\t\ts = getIniValue("xellbutton");\n\t\t\txb.xellButton = parseButtonX(s);\n\t\t\tif (!xb.xellButton || !s) {\n'),
    'cs_if': call('\t\t\ts = getIniValue("xellbutton");\n\t\t\tif (s)\n\t\t\t\txb.xellButton = parseButtonX(s);\n\t\t\tif (!xb.xellButton) {\n'),
    'cs_ifel': call('\t\t\ts = getIniValue("xellbutton");\n\t\t\tif (s)\n\t\t\t\txb.xellButton = parseButtonX(s);\n\t\t\telse\n\t\t\t\txb.xellButton = 0;\n\t\t\tif (!xb.xellButton) {\n'),
    'cs_tern': call('\t\t\ts = getIniValue("xellbutton");\n\t\t\txb.xellButton = s ? parseButtonX(s) : 0;\n\t\t\tif (!xb.xellButton) {\n'),
    'cs_i': call('\t\t\ti = parseButtonX(getIniValue("xellbutton"));\n\t\t\txb.xellButton = i;\n\t\t\tif (!i) {\n'),
    'cs_asg': call('\t\t\tif (!(xb.xellButton = parseButtonX(getIniValue("xellbutton")))) {\n'),
    'cs_eq': call('\t\t\txb.xellButton = parseButtonX(getIniValue("xellbutton"));\n\t\t\tif (xb.xellButton == 0) {\n'),
}


def build(name):
    t = SRC
    for part in name.split('+'):
        if part.startswith('px:'):
            t = t.replace(PBX, BODIES[part[3:]], 1)
            continue
        if part.startswith('pxe:'):
            t = t.replace(PBX, BODIES[part[4:]].replace(PW, '!strnicmp(s, "power", 5)'), 1)
            continue
        for old, new in VARIANTS[part]:
            if old not in t:
                raise KeyError('edit missing in %s: %r' % (part, old[:60]))
            t = t.replace(old, new, 1)
    return t


DUMPS = ['-fdump-tree-profile_estimate-details', '-fdump-tree-optimized-blocks-details',
         '-fdump-rtl-bbro-details', '-fdump-tree-vrp1-details', '-fdump-tree-fab1-details',
         '-fdump-ipa-inline-details', '-fdump-rtl-cprop_hardreg-blocks-details']


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


def blocks_of(dump, fn):
    t = dump[dump.index(';; Function %s ' % fn):]
    t = t[:t.index(';; Function', 10)] if ';; Function' in t[10:] else t
    bl = {}
    for m in re.finditer(r';;   basic block (\d+), loop depth \d+, count \d+, freq (\d+)(.*?)(?=;;   basic block|\Z)', t, re.S):
        bl[int(m.group(1))] = (int(m.group(2)), m.group(3))
    return bl


def metric(text, flags=optlib.P83):
    """xellbutton site counts after the tree passes: const-0 store block, remopower, remox,
    winbutton, part call; and the part's node (unlikely or not)"""
    import tempfile, shutil
    d = tempfile.mkdtemp(dir=optlib.BUILD, prefix='m')
    try:
        with open(os.path.join(d, 'o.c'), 'w', newline='\n') as f:
            f.write('#line 1 "options.c"\n' + text)
        env = dict(os.environ)
        tc = os.path.join(optlib.R, 'tools', 'toolchain-4745', 'mingw32', 'bin')
        env['PATH'] = tc + os.pathsep + env['PATH']
        r = subprocess.run([os.path.join(tc, 'gcc.exe'), '-c', '-O3'] + flags +
                           ['-I' + os.path.join(optlib.R, 'src'), 'o.c', '-o', 'o.o',
                            '-fdump-tree-optimized-blocks-details'], cwd=d, env=env, capture_output=True)
        if r.returncode:
            return 'compile error'
        fn = [x for x in os.listdir(d) if x.endswith('.optimized')][0]
        dump = open(os.path.join(d, fn)).read()
        bl = blocks_of(dump, 'applyIniOptions')
        var = None
        out = {}
        for b, (fq, body) in sorted(bl.items()):
            m = re.search(r'(\w+) = getIniValue \("xellbutton"\)', body)
            if m:
                var = m.group(1); out['call'] = fq
        for b, (fq, body) in sorted(bl.items()):
            if re.search(r'^  xb\.xellButton = 0;', body, re.M):
                out.setdefault('c0', []).append(fq)
            if var:
                for nm in ('power', 'remopower', 'remox', 'winbutton'):
                    if 'strnicmp (%s, "%s"' % (var, nm) in body:
                        out.setdefault(nm, []).append(fq)
                if 'parseButtonPart.constprop (%s)' % var in body:
                    out.setdefault('part', []).append(fq)
            if 'default console DVD' in body:
                out['log'] = fq
        return ' '.join('%s=%s' % (k, out[k]) for k in ('call', 'c0', 'power', 'remopower', 'remox', 'winbutton', 'part', 'log') if k in out)
    finally:
        shutil.rmtree(d, ignore_errors=True)


def main():
    a = sys.argv[1:]
    if '-m' in a:
        a.remove('-m')
        def onem(n):
            return n, metric(build(n)), optlib.fmt(optlib.score_text(build(n), optlib.P83)).split(' {')[0]
        with ThreadPoolExecutor(6) as ex:
            for n, m, s in ex.map(onem, a):
                print('%-24s %-8s %s' % (n, s, m), flush=True)
        return
    flags = optlib.P83
    d = out = vf = None
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
            return n, {'compile': str(e)}
        return n, optlib.score_text(t, flags)
    if not vf:
        with ThreadPoolExecutor(6) as ex:
            for n, r in ex.map(one, names):
                print('%-24s %s' % (n, optlib.fmt(r)), flush=True)
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
