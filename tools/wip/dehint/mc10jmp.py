"""mode_client attempt 10: a 2-term feed replaced by its target label in asm goto lists or
by one new JMP(target) (2 cp -> 0 or 1 asm goto).

Removes the statement matched by -rm, then: the target added to every existing list (AT
or plain label, either end), and a new `JMP(target);` at every position of mode_client.

python tools/wip/dehint/mc10jmp.py BASE.c -rm REGEX -t LABEL [-j 4] [-o DIR]"""
import os, re, sys
from concurrent.futures import ThreadPoolExecutor

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import mc1, mc1lib, mc7j2l, mc7reloc


def main():
    a = sys.argv[1:]
    t = mc1lib.read_src(a[0])
    rx = re.compile(a[a.index('-rm') + 1])
    lab = a[a.index('-t') + 1]
    jobs = int(a[a.index('-j') + 1]) if '-j' in a else 4
    odir = a[a.index('-o') + 1] if '-o' in a else None
    m = rx.search(t)
    assert m, 'no match'
    b = t[:m.start()] + t[m.end():]
    todo = [('none', b)]
    for j, o in enumerate(mc7j2l.stmts(b)):
        if o[0] == 'mc' and lab not in o[5]:
            todo.append(('list%d.s' % j, b[:o[3]] + lab + ', ' + b[o[3]:]))
            todo.append(('list%d.e' % j, b[:o[4]] + ', ' + lab + b[o[4]:]))
    for p in mc7reloc.positions(b, 'mode_client'):
        todo.append(('jmp@%d' % p, b[:p] + ' JMP(%s);' % lab + b[p:]))
    print(len(todo), 'variants', mc1.count(t)['total'], '->', mc1.count(b)['total'], flush=True)
    with ThreadPoolExecutor(jobs) as ex:
        res = list(ex.map(lambda it: (it[0], mc1lib.score_text(it[1], []), it[1]), todo))
    rows = sorted((0 if s.get('identical') else s.get('total', 99999), k, x) for k, s, x in res)
    for d, k, x in rows[:10]:
        p = int(k.split('@')[1]) if '@' in k else 0
        print(d, k, mc1.count(x)['total'], repr(b[max(0, p - 50):p]) if p else '', flush=True)
    if odir and rows[0][0] == 0:
        os.makedirs(odir, exist_ok=True)
        open(os.path.join(odir, 'h_jmp_%s.c' % lab), 'w', newline='\n').write(rows[0][2])


if __name__ == '__main__':
    main()
