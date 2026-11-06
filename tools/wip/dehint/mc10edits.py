"""mode_client attempt 10: asm goto list edits with the AT(x) labels.

mc8comp.labels only finds `name:` labels, so the case labels written AT(c1), AT(c3),
AT(t5), AT(u2) ... (and none of clientEraseBlockI's in mode_client lists) were never added
to a list by mc7comp/mc8comp/mc9loop/mc9rep.  edits_at() gives those adds (each AT label
at either end of every list of its function); -pairs adds pairs (new x new, or new x
mc8comp's).  Count-neutral: list labels are not counted.

python tools/wip/dehint/mc10edits.py BASE.c [BASE2.c ...] [-pairs] [-j 4] [-o DIR]"""
import itertools, os, re, sys
from concurrent.futures import ThreadPoolExecutor

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import mc1lib, mc7j2l, mc8comp


def at_labels(t, fn):
    for nm, s, e in mc7j2l.fn_ranges(t):
        if nm == fn:
            break
    labs = []
    for m in re.finditer(r'\bAT\((\w+)\)', t[s:e]):
        if m.group(1) not in labs:
            labs.append(m.group(1))
    return labs


def edits_at(t):
    st = mc7j2l.stmts(t)
    labs = {f: at_labels(t, f) for f in ('mc', 'cebi')}
    out = []
    for j, o in enumerate(st):
        for lab in labs[o[0]]:
            if lab in o[5]:
                continue
            out.append(('add %s>%d.s' % (lab, j), [(o[3], o[3], lab + ', ')]))
            out.append(('add %s>%d.e' % (lab, j), [(o[4], o[4], ', ' + lab)]))
    return out


def variants(t, pairs=False):
    eds = edits_at(t)
    out = [(k, mc7j2l.apply(t, ed)) for k, ed in eds]
    if pairs:
        for (k1, e1), (k2, e2) in itertools.combinations(eds, 2):
            if mc8comp.compatible(e1, e2):
                out.append((k1 + ' + ' + k2, mc7j2l.apply(t, e1 + e2)))
    return out


def main():
    a = sys.argv[1:]
    bases = [x for x in a if x.endswith('.c')]
    jobs = int(a[a.index('-j') + 1]) if '-j' in a else 4
    odir = a[a.index('-o') + 1] if '-o' in a else None
    for b in bases:
        t = mc1lib.read_src(b)
        todo = variants(t, '-pairs' in a)
        with ThreadPoolExecutor(jobs) as ex:
            res = list(ex.map(lambda it: (it[0], mc1lib.score_text(it[1], []), it[1]), todo))
        rows = sorted((0 if s.get('identical') else s.get('total', 99999), k, x) for k, s, x in res)
        print(b, len(todo), 'best', [(d, k) for d, k, _ in rows[:6]], flush=True)
        if odir and rows and rows[0][0] == 0:
            os.makedirs(odir, exist_ok=True)
            for n, (d, k, x) in enumerate(rows[:3]):
                if d == 0:
                    open(os.path.join(odir, 'h_%s_%d.c' % (os.path.basename(b)[:-2], n)), 'w', newline='\n').write(x)


if __name__ == '__main__':
    main()
