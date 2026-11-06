"""mode_client attempt 10: feeds to ndl replaced by self-edges at the ndl block.

Subsets of the three ndl feeds (rok's after netGetInfo, fail's two) removed, crossed with:
ndl added to the dtg reboot arm's JMP(fail) list (uncounted), a new JMP(ndl) at the ndl
block (+1 asm goto), and each with fail's remaining feeds permuted (mc9loop.perms).

python tools/wip/dehint/mc10self.py BASE.c [-j 4] [-o DIR]"""
import itertools, os, re, sys
from concurrent.futures import ThreadPoolExecutor

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import mc1, mc1lib, mc9loop

NDL = re.compile(r'[ \t]*if \(__builtin_constant_p\(mode \+ \d+\)\) goto ndl;\n?')
ARM = 'JMP(fail); ndl: netDisconnect();'
FORMS = {
    'none': ARM,
    'list': 'JMP(fail, ndl); ndl: netDisconnect();',
    'list2': 'JMP(ndl, fail); ndl: netDisconnect();',
    'after': 'JMP(fail); ndl: netDisconnect(); JMP(ndl);',
    'at': 'JMP(fail); ndl: JMP(ndl); netDisconnect();',
}


def main():
    a = sys.argv[1:]
    t = mc1lib.read_src(a[0])
    jobs = int(a[a.index('-j') + 1]) if '-j' in a else 4
    odir = a[a.index('-o') + 1] if '-o' in a else None
    assert ARM in t
    ms = list(NDL.finditer(t))
    todo = []
    for k in range(1, len(ms) + 1):
        for sub in itertools.combinations(range(len(ms)), k):
            x = t
            for i in sorted(sub, reverse=True):
                m = ms[i]
                keep = '\n' if m.group(0).endswith('\n') and m.group(0).startswith('\t') else ''
                x = x[:m.start()] + ('' if not keep else '') + x[m.end():]
            for fk, form in FORMS.items():
                y = x.replace(ARM, form)
                tag = 'rm%s %s' % (''.join(map(str, sub)), fk)
                todo.append((tag, y))
                for p in mc9loop.perms(y):
                    todo.append((tag + ' perm', p))
    print(len(todo), 'variants', flush=True)
    with ThreadPoolExecutor(jobs) as ex:
        res = list(ex.map(lambda it: (it[0], mc1lib.score_text(it[1], []), it[1]), todo))
    rows = sorted((0 if s.get('identical') else s.get('total', 99999), -mc1.count(x)['total'], k, x) for k, s, x in res)
    for d, c, k, _ in rows[:15]:
        print(d, -c, k, flush=True)
    if odir and rows[0][0] == 0:
        os.makedirs(odir, exist_ok=True)
        hits = sorted([r for r in rows if r[0] == 0], key=lambda r: -r[1])
        open(os.path.join(odir, 'h_self.c'), 'w', newline='\n').write(hits[0][3])
        print('BEST HIT', -hits[0][1], hits[0][2])


if __name__ == '__main__':
    main()
