"""Attempt 58: score build.o for type changes in the shared headers (and build.c), each crossed with
hint sets off (bdhints names).

python tools/wip/dehint/bdgen/a58lib.py <script.py> [-p 99] [-o set;set] [-k label]
  script.py defines V = {label: (hdr, c)}: hdr = {'xebuild.h': [(old, new), ..], ..} applied to copies
  of src/*.h in build/bd/a58/ov/<label>/ (put ahead of src on the include path), c = [(old, new), ..]
  applied to src/build.c.  -o gives the hint sets (comma-joined bdhints names; '-' = all kept);
  default: '-' and each hint alone.  Prints loose/strict per function for each (label, set)."""
import importlib.util, os, shutil, sys
from concurrent.futures import ThreadPoolExecutor
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import bdlib, bdrun, bdhints

OV = os.path.join(bdlib.R, 'build', 'bd', 'a58', 'ov')
SRCD = os.path.join(bdlib.R, 'src')


def overlay(label, hdr):
    d = os.path.join(OV, label)
    os.makedirs(d, exist_ok=True)
    for f in os.listdir(SRCD):
        if f.endswith('.h'):
            t = open(os.path.join(SRCD, f), newline='').read()
            for a, b in hdr.get(f, []):
                t = bdrun.sub(t, a, b, 1)
            open(os.path.join(d, f), 'w', newline='\n').write(t)
    for f in hdr:
        if not os.path.exists(os.path.join(SRCD, f)):
            raise ValueError('no header ' + f)
    return d


def score(text, flags, inc):
    ok, o, d = bdlib.compile_src(text, flags, extra=['-I' + inc])
    try:
        if not ok:
            return {'err': o[:400]}
        r = bdlib.ref()
        if open(o, 'rb').read() == r['bytes']:
            return {'identical': True, 'S': {}, 'L': {}, 'notes': []}
        fns, order = bdlib.disasm(o)
        S, L = {}, {}
        for n in r['order']:
            if n not in fns:
                S[n] = L[n] = 9999
                continue
            if fns[n] != r['fns'][n]:
                S[n] = bdrun.ndiff(r['fns'][n], fns[n])
                k = bdrun.ndiff(bdrun.loose(r['fns'][n]), bdrun.loose(fns[n]))
                if k:
                    L[n] = k
        for n in order:
            if n not in r['fns']:
                S[n] = L[n] = 9999
        notes = [s for s in ('.text', '.data', '.rdata', '.bss') if bdlib.section(o, s) != r['sec'][s]]
        return {'identical': not S and not notes, 'S': S, 'L': L, 'notes': notes}
    finally:
        bdlib.cleanup(d)


def main():
    a = sys.argv[1:]
    p, keep, sets = 99, None, None
    if '-p' in a:
        i = a.index('-p'); p = int(a[i + 1]); del a[i:i + 2]
    if '-k' in a:
        i = a.index('-k'); keep = a[i + 1]; del a[i:i + 2]
    if '-o' in a:
        i = a.index('-o'); sets = a[i + 1].split(';'); del a[i:i + 2]
    sets = sets or ['-'] + list(bdhints.H)
    spec = importlib.util.spec_from_file_location('v', a[0])
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    base = bdlib.read_src()
    fl = [] if p == 0 else ['--param', 'builtin-expect-probability=%d' % p]
    jobs = []
    for lab, (hdr, c) in m.V.items():
        try:
            inc = overlay(lab, hdr)
            t = base
            for x, y in c:
                t = bdrun.sub(t, x, y, 1)
        except ValueError as e:
            print(lab, 'SUBFAIL', e); continue
        if lab == keep:
            open(os.path.join(bdlib.R, 'build', 'bd', 'a58', lab + '.c'), 'w', newline='\n').write(t)
        for s in sets:
            try:
                tt = t if s == '-' else bdhints.off(t, *s.split(','))
            except ValueError as e:
                print(lab, s, 'SUBFAIL', e); continue
            jobs.append((lab, s, tt, inc))

    def one(j):
        lab, s, t, inc = j
        return lab, s, score(t, fl, inc)
    with ThreadPoolExecutor(4) as ex:
        for lab, s, r in ex.map(one, jobs):
            if 'err' in r:
                print('%-22s %-12s ERR %s' % (lab, s, r['err'][:300].replace('\n', ' | '))); continue
            if r['identical']:
                print('%-22s %-12s IDENTICAL' % (lab, s), flush=True); continue
            print('%-22s %-12s L%-4d S%-4d %s %s' % (lab, s, sum(r['L'].values()), sum(r['S'].values()),
                  ' '.join('%s:%d/%d' % (k[1:], r['L'].get(k, 0), v) for k, v in r['S'].items()), ','.join(r['notes'])), flush=True)


if __name__ == '__main__':
    main()
