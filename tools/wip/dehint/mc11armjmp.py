"""mode_client attempt 11: a mode-chain arm dropped (mc11arm.drop_arm), repaired by
  lists: one list edit (mc8comp.edits, AT labels included since attempt 11),
  jmp:   one new `JMP(L);` at every position of mode_client (+1 asm goto) for L in -t,
  less:  one cp(V + N) -> cp(V) toggle, perm: fail's feeds (mc9loop).
Arm 11 has 5 terms, arm 7 4, so a JMP repair is still a gain of 4 / 3.

python tools/wip/dehint/mc11armjmp.py BASE.c -arm 11 [-t c11,i1] [-r lists,jmp,less,perm] [-j 4] [-o DIR]"""
import os, re, sys
from concurrent.futures import ThreadPoolExecutor

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import mc1, mc1lib, mc7j2l, mc7reloc, mc8comp, mc9loop, mc11arm


def variants(b, reps, tg):
    out = []
    if 'lists' in reps:
        out += [(k, mc7j2l.apply(b, ed)) for k, ed in mc8comp.edits(b)]
    if 'jmp' in reps:
        for lab in tg:
            for p in mc7reloc.positions(b, 'mode_client'):
                out.append(('JMP(%s)@%d' % (lab, p), b[:p] + ' JMP(%s);' % lab + b[p:]))
    if 'less' in reps:
        out += [('less%d' % n, x) for n, x in enumerate(mc9loop.less(b, 1))]
    if 'perm' in reps:
        out += [('perm%d' % n, x) for n, x in enumerate(mc9loop.perms(b))]
    return out


def main():
    a = sys.argv[1:]
    t = mc1lib.read_src(a[0])
    arm = int(a[a.index('-arm') + 1])
    tg = (a[a.index('-t') + 1] if '-t' in a else 'c%d' % arm).split(',')
    reps = (a[a.index('-r') + 1] if '-r' in a else 'lists,jmp,less,perm').split(',')
    jobs = int(a[a.index('-j') + 1]) if '-j' in a else 4
    odir = a[a.index('-o') + 1] if '-o' in a else None
    b = mc11arm.drop_arm(t, arm)
    print('arm %d dropped: count %d, %s' % (arm, mc1.count(b)['total'], mc1lib.fmt(mc1lib.score_text(b, []))[:80]), flush=True)
    todo = variants(b, reps, tg)
    print(len(todo), 'variants', flush=True)
    with ThreadPoolExecutor(jobs) as ex:
        res = list(ex.map(lambda it: (it[0], mc1lib.score_text(it[1], []), it[1]), todo))
    rows = sorted((0 if s.get('identical') else s.get('total', 99999), k, x) for k, s, x in res)
    for d, k, x in rows[:15]:
        print(d, k, mc1.count(x)['total'], flush=True)
    if odir:
        os.makedirs(odir, exist_ok=True)
        for d, k, x in rows[:5]:
            open(os.path.join(odir, 'aj%d_%s.c' % (arm, re.sub(r'\W+', '_', k))), 'w', newline='\n').write(x)


if __name__ == '__main__':
    main()
