"""mode_client attempt 8: mc7comp's removal + free list edit search, with
- clientEraseBlockI's labels and asm goto lists in the edit set (cebi labels into cebi
  lists, mode_client labels into mode_client lists),
- more removals (cebi cold labels / feeds / JMPs, the X and m pins, hdd4/5, dsp),
- -two: pairs of edits drawn from the best TOP singles (default 60).

python tools/wip/dehint/mc8comp.py NAME [-base FILE] [-j 4] [-o DIR] [-two [TOP]]
python tools/wip/dehint/mc8comp.py list"""
import itertools, os, re, sys
from concurrent.futures import ThreadPoolExecutor

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import mc1, mc1lib, mc7comp, mc7j2l

REMOVALS = dict(mc7comp.REMOVALS)
REMOVALS.update({
    'efc': [(r' efc: __attribute__\(\(cold\)\);', '')],
    'einv': [(r' einv: __attribute__\(\(cold\)\);', '')],
    'dyfeed': [(r'if \(__builtin_constant_p\(block \+ 900\)\) goto dy; ', '')],
    'ybkfeed': [(r'if \(__builtin_constant_p\(block \+ 901\)\) goto ybk; ', '')],
    'efail1': [(r'JMP\(efail\); if \(block <', 'if (block <')],
    'efail2': [(r'  JMP\(efail\); \}', ' }')],
    'dyj': [(r' JMP\(dy\); \}', ' }')],
    'hdd45': [(r'JMP\(hdd4,hdd5\); ', '')],
    'dspj': [(r'JMP\(dsp\);', '')],
    'pinX': [(r'__asm__ \("" :: "X"\(&fkv\)\); ', '')],
    'pinm': [(r'__asm__ \("" :: "m"\(rko\)\); ', '')],
    'dyall': [(r'if \(__builtin_constant_p\(block \+ 900\)\) goto dy; ybk:;  ', ''),
              (r' JMP\(dy\); \}', ' }'),
              (r'if \(0\) \{ dy: if \(__builtin_constant_p\(block \+ 901\)\) goto ybk; __builtin_unreachable\(\); \} ', '')],
    'efall': [(r'JMP\(efail\); if \(block <', 'if (block <'), (r'  JMP\(efail\); \}', ' }'),
              (r'AT\(efail\) \{ efc: __attribute__\(\(cold\)\); \} ', '')],
    's4c12o':[(r'JMP\(s4, c12, ork6\); ', '')],
    'kk2': [(r'\tint kk = __builtin_constant_p\(argc\);\n', ''),
            (r' __builtin_memset\(argv, 0, kk\); if \(!kk\) \{ __asm__ goto \("" :: "a"\(i\) :: rk6, r5x, r3x\); \}', '')],
})


def labels(t, fn):
    for nm, s, e in mc7j2l.fn_ranges(t):
        if nm == fn:
            break
    # attempt 11: string literals and comments blanked (they gave junk labels such as
    # 'ERROR', '1', 'borderline'), and AT(x) labels included (they were missing)
    body = re.sub(r'"(?:[^"\\\n]|\\.)*"', '""', t[s:e])
    body = re.sub(r'/\*.*?\*/', ' ', body, flags=re.S)
    labs = []
    for m in re.finditer(r'(?<![:\w])(\w+):(?!:)|\bAT\((\w+)\)', body):
        lab = m.group(1) or m.group(2)
        if lab not in ('default', 'case', 'AT') and not lab.isdigit() and lab not in labs:
            labs.append(lab)
    return labs


def edits(t):
    st = mc7j2l.stmts(t)
    labs = {f: labels(t, f) for f in ('mc', 'cebi')}
    out = []
    for j, o in enumerate(st):
        for lab in labs[o[0]]:
            if lab in o[5]:
                continue
            out.append(('add %s>%d.s' % (lab, j), [(o[3], o[3], lab + ', ')]))
            out.append(('add %s>%d.e' % (lab, j), [(o[4], o[4], ', ' + lab)]))
        if len(o[5]) > 1:
            for k, lab in enumerate(o[5]):
                rest = o[5][:k] + o[5][k + 1:]
                out.append(('drop %s@%d' % (lab, j), [(o[3], o[4], ', '.join(rest))]))
    return out


def compatible(e1, e2):
    # no overlapping replaced ranges unless both are pure inserts at different points
    (s1, f1, _), (s2, f2, _) = e1[0], e2[0]
    if s1 == f1 and s2 == f2:
        return s1 != s2
    return f1 < s2 or f2 < s1


def remove(t, name):
    if '+' in name:
        for n in name.split('+'):
            t = remove(t, n) if t is not None else None
        return t
    for rx, rep in REMOVALS[name]:
        t, n = re.subn(rx, rep, t, count=1)
        if n != 1:
            return None
    return t


def run(t, jobs, two=0, odir=None, name='x', stop=True):
    eds = edits(t)
    todo = [('alone', t)] + [(k, mc7j2l.apply(t, ed)) for k, ed in eds]
    res = []

    def one(it):
        return it[0], mc1lib.score_text(it[1], []), it[1]

    hits = []
    with ThreadPoolExecutor(jobs) as ex:
        for i in range(0, len(todo), 64):
            for k, s, txt in ex.map(one, todo[i:i + 64]):
                if 'compile' in s:
                    continue
                if s['identical']:
                    hits.append((k, txt))
                    res.append((0, k))
                else:
                    res.append((s['total'], k))
            if hits and stop:
                return hits, sorted(res)
    res.sort()
    if two and not hits:
        ed = dict(eds)
        top = [k for sc, k in res if k != 'alone'][:two]
        pairs = [(a, b) for a, b in itertools.combinations(top, 2) if compatible(ed[a], ed[b])]
        todo2 = [('%s + %s' % (a, b), mc7j2l.apply(t, ed[a] + ed[b])) for a, b in pairs]
        with ThreadPoolExecutor(jobs) as ex:
            for i in range(0, len(todo2), 64):
                for k, s, txt in ex.map(one, todo2[i:i + 64]):
                    if 'compile' in s:
                        continue
                    if s['identical']:
                        hits.append((k, txt))
                        res.append((0, k))
                    else:
                        res.append((s['total'], k))
                if hits and stop:
                    break
        res.sort()
    if odir:
        for k, txt in hits:
            open(os.path.join(odir, 'c8_%s_%s.c' % (name, re.sub(r'\W', '_', k))), 'w', newline='\n').write(txt)
    return hits, res


def main():
    a = sys.argv[1:]
    name = a[0]
    if name == 'list':
        print(' '.join(REMOVALS))
        return
    base = mc1lib.read_src(a[a.index('-base') + 1] if '-base' in a else mc1.BASE)
    jobs = int(a[a.index('-j') + 1]) if '-j' in a else 4
    odir = a[a.index('-o') + 1] if '-o' in a else None
    two = 0
    if '-two' in a:
        k = a.index('-two')
        two = int(a[k + 1]) if k + 1 < len(a) and a[k + 1].isdigit() else 60
    t = base if name == 'none' else remove(base, name)
    assert t is not None, name
    hits, res = run(t, jobs, two, odir, name, stop=False)
    for k, _ in hits:
        print('HIT', name, k, flush=True)
    print(name, 'count', mc1.count(t)['total'], len(res), 'variants; best', res[:10], flush=True)


if __name__ == '__main__':
    main()
