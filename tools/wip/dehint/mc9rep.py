"""mode_client attempt 9: every count-neutral repair of one near-miss base.

python tools/wip/dehint/mc9rep.py BASE.c [-j 4] [-o DIR] [-r perm,less,lists,reloc,default]
  perm:    fail's feeds reordered / moved after the log call (mc9fail)
  default: the default case's feeds each before/after its log call
  less:    one cp(V + N) -> cp(V) toggle
  lists:   one asm goto list edit (mc8comp.edits: add any label at either end, drop one)
  reloc:   every 1-term mode_client feed moved to every position (mc7reloc.positions)
Prints the best scores per repair; IDENTICAL hits are written to DIR/h_<repair>_<n>.c."""
import os, re, sys
from concurrent.futures import ThreadPoolExecutor

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import mc1, mc1lib, mc7j2l, mc7reloc, mc8comp, mc9loop

FEED = r' ?if \(__builtin_constant_p\((?:mode|i)(?: \+ \d+)?\)\) goto (\w+);'


def default_variants(t):
    i = t.index('default:')
    j = t.index('break;', i)
    seg = t[i:j]
    feeds = re.findall(FEED[2:], seg)
    fs = [m.group(0).strip() for m in re.finditer(FEED, seg)]
    bare = seg
    for f in fs:
        bare = bare.replace(f, '', 1)
    k = bare.index(');', bare.index('please inform author')) + 2
    c = bare.index('AT(cdef) ') + len('AT(cdef) ')
    out = []
    import itertools
    for perm in itertools.permutations(fs):
        for cut in range(len(fs) + 1):
            pre = ' '.join(perm[:cut])
            post = ' '.join(perm[cut:])
            s = bare[:i - i] if False else bare
            s = s[:k] + (' ' + post if post else '') + s[k:]
            s = s.replace('default:', 'default:', 1)
            # pre goes before the cdef label (where the t5 feed sits in the base)
            ci = s.index('AT(cdef) ')
            s = s[:ci] + (pre + '\n\t\t\t\t' if pre else '') + s[ci:]
            out.append(t[:i] + s + t[j:])
    return [x for x in set(out) if x != t]


def reloc_variants(t):
    s0 = t.index('int mode_client(')
    out = []
    for m in re.finditer(FEED, t[s0:]):
        fs, fe = s0 + m.start(), s0 + m.end()
        b = t[:fs] + t[fe:]
        for p in mc7reloc.positions(b, 'mode_client'):
            out.append(b[:p] + ' ' + m.group(0).strip() + b[p:])
    return out


def retarget_variants(t):
    s0 = t.index('int mode_client(')
    labs = mc8comp.labels(t, 'mc')
    out = []
    for m in re.finditer(FEED, t[s0:]):
        for lab in labs:
            if lab != m.group(1):
                out.append(t[:s0 + m.start(1)] + lab + t[s0 + m.end(1):])
    return out


GENS = {
    'retarget': retarget_variants,
    'perm': mc9loop.perms,
    'default': default_variants,
    'less': lambda t: mc9loop.less(t, 1),
    'lists': lambda t: [mc7j2l.apply(t, ed) for _, ed in mc8comp.edits(t)],
    'reloc': reloc_variants,
}


def main():
    a = sys.argv[1:]
    t = mc1lib.read_src(a[0])
    jobs = int(a[a.index('-j') + 1]) if '-j' in a else 4
    odir = a[a.index('-o') + 1] if '-o' in a else None
    reps = (a[a.index('-r') + 1] if '-r' in a else 'perm,default,less,lists,reloc').split(',')
    if odir:
        os.makedirs(odir, exist_ok=True)
    print(a[0], 'count', mc1.count(t)['total'], mc1lib.fmt(mc1lib.score_text(t, []))[:30], flush=True)
    for r in reps:
        cands = GENS[r](t)
        with ThreadPoolExecutor(jobs) as ex:
            ss = list(ex.map(lambda x: mc1lib.score_text(x, []), cands))
        res = sorted((0 if s.get('identical') else s.get('total', 99999), n) for n, s in enumerate(ss))
        hits = [n for d, n in res if d == 0]
        print(r, len(cands), 'hits', len(hits), 'best', [d for d, n in res[:10]], flush=True)
        for n in hits[:5]:
            if odir:
                open(os.path.join(odir, 'h_%s_%d.c' % (r, n)), 'w', newline='\n').write(cands[n])
        if hits and '-stop' in a:
            break


if __name__ == '__main__':
    main()
