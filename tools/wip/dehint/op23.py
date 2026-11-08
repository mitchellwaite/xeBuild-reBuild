#!/usr/bin/env python3
"""Attempt 23: the remaining __builtin_expects (parseButtonX's power, the rev feeds' three):
their real windows and natural replacements.

python tools/wip/dehint/op23.py [-m] [-e] [-np|-p N] [-o out.c] [-v fn] variant ..
  a variant is names from V here joined by `+` (applied in order to src/options.c).
  -m  counts from the optimized dump: dz1/dz2 (the unreachable blocks), the rev block, and
      the xellbutton site (op20's metric)
  -e  profile_estimate predictions of applyIniOptions' feed tests and parseButtonX's power
  -v fn  diff of function fn"""
import os, re, subprocess, sys, tempfile, shutil
from concurrent.futures import ThreadPoolExecutor
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import optlib

# the attempt's start (src before attempt 23's feed change); feeds are replaced whole
SRC = open(os.path.join(optlib.BUILD, 'a23', 'start.c')).read()


def X(n):
    return '__builtin_constant_p(xb.blSuffix[1] + %d)' % n


F1 = ('\t\t\tif (%s) { if (__builtin_expect(%s, 0)) goto dz1; return; }\n' % (X(1), X(2)))
F2 = ('\t\t\tif (__builtin_expect(%s, 0)) { if (__builtin_expect(%s, 0)) goto dz2; }\n' % (X(15), X(16)))
FEED = F1 + F2
assert FEED in SRC, 'feed text'
V = {'base': []}


def feed(a, b):
    """replace the two feed lines: a and b are the bodies with {n} = X(n)"""
    return [(FEED, a.format(**{'n%d' % i: X(i) for i in range(1, 40)}) +
             b.format(**{'n%d' % i: X(i) for i in range(1, 40)}))]


T1 = '\t\t\tif ({n1}) {{ if (__builtin_expect({n2}, 0)) goto dz1; return; }}\n'
E = '__builtin_expect(%s, 0)'
# e2 (the outer dz2 test) natural forms, e3 kept
for k, c in {'e2': '{n15}', 'e2lt': '{n15} < 0', 'e2eq': '{n15} == 5', 'e2gt': '{n15} > 0',
             'e2ne': '{n15} != 5'}.items():
    V[k] = feed(T1, '\t\t\tif (%s) {{ if (__builtin_expect({n16}, 0)) goto dz2; }}\n' % c)
# e3 / e1 removed (noreturn: expected ~0 flow)
V['e3'] = feed(T1, '\t\t\tif (__builtin_expect({n15}, 0)) {{ if ({n16}) goto dz2; }}\n')
V['e1'] = feed('\t\t\tif ({n1}) {{ if ({n2}) goto dz1; return; }}\n',
               '\t\t\tif (__builtin_expect({n15}, 0)) {{ if (__builtin_expect({n16}, 0)) goto dz2; }}\n')
# D's other arm to dz1: noreturn on both of D's edges cancels (excluded from first match)
for k, (c, d) in {'dd': ('{n15}', '{n16}'), 'dd_lt': ('{n15}', '{n16} < 0'),
                  'dd_eq': ('{n15}', '{n16} == 5'), 'dd_e': (E % '{n15}', '{n16}'),
                  'dd_ee': (E % '{n15}', E % '{n16}'), 'dd_elt': (E % '{n15}', '{n16} < 0'),
                  'dd_eeq': (E % '{n15}', '{n16} == 5'), 'dd_egt': (E % '{n15}', '{n16} > 0'),
                  'dd_ltlt': ('{n15} < 0', '{n16} < 0'), 'dd_lteq': ('{n15} < 0', '{n16} == 5'),
                  'dd_eqlt': ('{n15} == 5', '{n16} < 0'), 'dd_eqeq': ('{n15} == 5', '{n16} == 5'),
                  }.items():
    V[k] = feed(T1, '\t\t\tif (%s) {{ if (%s) goto dz2; goto dz1; }}\n' % (c, d))

# parseButtonX power test without the expect
PW = '\tif (__builtin_expect(!strnicmp(s, "power", 5), 1)) {\n'
assert PW in SRC
V['bxe'] = [(PW, '\tif (!strnicmp(s, "power", 5)) {\n')]
# probe: the remopower call ahead of the z feed, so the power test's else edge sees a call
# (natural power 83.25%: call 71 + const return 67)
ZF = ('\t\tif (__builtin_constant_p(xb.xellButton + 1)) { if (__builtin_constant_p(xb.xellButton + 2) > 0) goto z; }\n'
      '\t\tif (!strnicmp(s, "remopower", 9))\n')
assert ZF in SRC
V['bxc'] = [(ZF, '\t\tint r = strnicmp(s, "remopower", 9);\n\n' + ZF.split('\n')[0] + '\n\t\tif (!r)\n')]


def build(name):
    t = SRC
    for part in name.split('+'):
        for old, new in V[part]:
            if old not in t:
                raise KeyError('edit missing in %s: %r' % (part, old[:70]))
            t = t.replace(old, new, 1)
    return t


def blocks_of(dump, fn):
    t = dump[dump.index(';; Function %s ' % fn):]
    t = t[:t.index(';; Function', 10)] if ';; Function' in t[10:] else t
    bl = {}
    for m in re.finditer(r';;   basic block (\d+), loop depth \d+, count \d+, freq (\d+)(.*?)(?=;;   basic block|\Z)', t, re.S):
        bl[int(m.group(1))] = (int(m.group(2)), m.group(3))
    return bl


def dumps(text, flags, opts):
    d = tempfile.mkdtemp(dir=optlib.BUILD, prefix='m')
    with open(os.path.join(d, 'o.c'), 'w', newline='\n') as f:
        f.write('#line 1 "options.c"\n' + text)
    env = dict(os.environ)
    tc = os.path.join(optlib.R, 'tools', 'toolchain-4745', 'mingw32', 'bin')
    env['PATH'] = tc + os.pathsep + env['PATH']
    subprocess.run([os.path.join(tc, 'gcc.exe'), '-c', '-O3'] + flags +
                   ['-I' + os.path.join(optlib.R, 'src'), 'o.c', '-o', 'o.o'] + opts,
                   cwd=d, env=env, capture_output=True)
    out = {}
    for x in os.listdir(d):
        for suf in ('optimized', 'profile_estimate'):
            if x.endswith(suf):
                out[suf] = open(os.path.join(d, x)).read()
    shutil.rmtree(d, ignore_errors=True)
    return out


def metric(text, flags):
    dm = dumps(text, flags, ['-fdump-tree-optimized-blocks-details'])
    if 'optimized' not in dm:
        return 'compile error'
    bl = blocks_of(dm['optimized'], 'applyIniOptions')
    out = {}
    var = None
    for b, (fq, body) in sorted(bl.items()):
        if '__builtin_unreachable' in body:
            out.setdefault('dz', []).append(fq)
        if 'sprintf (&xb.blSuffix' in body:
            out['rev'] = fq
        if re.search(r'^  return;', body, re.M):
            out.setdefault('ret', []).append(fq)
        m = re.search(r'(\w+) = getIniValue \("xellbutton"\)', body)
        if m:
            var = m.group(1)
            out['call'] = fq
    for b, (fq, body) in sorted(bl.items()):
        if re.search(r'^  xb\.xellButton = 0;', body, re.M):
            out.setdefault('c0', []).append(fq)
        if var:
            for nm in ('power', 'remopower', 'remox'):
                if 'strnicmp (%s, "%s"' % (var, nm) in body:
                    out.setdefault(nm, []).append(fq)
    return ' '.join('%s=%s' % (k, out[k]) for k in ('dz', 'rev', 'ret', 'call', 'c0', 'power', 'remopower', 'remox') if k in out)


def preds(text, flags):
    dm = dumps(text, flags, ['-fdump-tree-profile_estimate-blocks-details'])
    t = dm.get('profile_estimate', '')
    res = []
    for fn in ('parseButtonX', 'applyIniOptions'):
        parts = [m.start() for m in re.finditer(r';; Function %s ' % fn, t)]
        if len(parts) < 2:
            continue
        a = t[parts[0]:parts[1]]
        body = t[parts[1]:]
        body = body[:body.index(';; Function', 10)] if ';; Function' in body[10:] else body
        # blocks with a constant_p test or the power strnicmp
        want = set()
        for m in re.finditer(r';;   basic block (\d+), loop depth \d+, count \d+, freq (\d+)(.*?)(?=;;   basic block|\Z)', body, re.S):
            if re.search(r'__builtin_constant_p|"power"', m.group(3)):
                want.add(int(m.group(1)))
                sc = re.findall(r'(\d+) \[([\d.]+)%\]', m.group(3).split(';;    succ:')[-1])
                res.append('%s bb%s freq %s succ %s' % (fn, m.group(1), m.group(2), sc))
        for m in re.finditer(r'Predictions for bb (\d+)\n((?:  .*\n)+)', a):
            if int(m.group(1)) in want:
                res.append('%s bb%s: %s' % (fn, m.group(1), '; '.join(l.strip().replace(' heuristics', '') for l in m.group(2).strip().split('\n'))))
    return '\n'.join(res)


def main():
    a = sys.argv[1:]
    flags = optlib.P83
    out = vf = None
    m = e = False
    if '-m' in a:
        a.remove('-m'); m = True
    if '-e' in a:
        a.remove('-e'); e = True
    if '-np' in a:
        a.remove('-np'); flags = []
    if '-p' in a:
        i = a.index('-p'); flags = ['--param', 'builtin-expect-probability=' + a[i + 1]]; del a[i:i + 2]
    if '-o' in a:
        i = a.index('-o'); out = a[i + 1]; del a[i:i + 2]
    if '-v' in a:
        i = a.index('-v'); vf = a[i + 1]; del a[i:i + 2]
    names = a

    def one(n):
        try:
            t = build(n)
        except KeyError as ex:
            return n, {'compile': str(ex)}, '', ''
        return n, optlib.score_text(t, flags), (metric(t, flags) if m else ''), (preds(t, flags) if e else '')
    if vf:
        for n in names:
            optlib.vdiff(build(n), flags, vf)
    else:
        with ThreadPoolExecutor(6) as ex:
            for n, r, mm, ee in ex.map(one, names):
                s = optlib.fmt(r)
                print('%-20s %s %s' % (n, s, mm), flush=True)
                if ee:
                    print(ee)
    if out:
        with open(out, 'w', newline='\n') as f:
            f.write(build(names[-1]))


if __name__ == '__main__':
    main()
