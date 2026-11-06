"""mode_client attempt 6: count-neutral walk over the asm goto label lists in mode_client
(drop a label, add a label to a list), from a base with counted hints removed.  The lists
are counted per statement, so editing their labels keeps the count; the walk looks for a
list configuration that brings the base back to IDENTICAL.

python tools/wip/dehint/mc6walk.py BASE.c OUT_PREFIX [-j 4] [-steps 30] [-lists RX]
  greedy best-improvement; on a plateau takes the best equal move not seen before.
  States -> OUT_PREFIX_<step>.c, log on stdout."""
import os, re, sys
from concurrent.futures import ThreadPoolExecutor

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import mc1, mc1lib

LIST_RX = [r'(JMP\()([\w, ]+)(\))', r'(__asm__ goto \("" [^;]*?: ?: ?)([\w, ]+)(\);)']
ADD = ['c1', 'c2', 'c3', 't4', 's4', 'hdd4', 't5', 's5', 'hdd5', 'c7', 'p1', 'c9', 'c10',
       'c11', 'c12', 'i1', 'cdef', 'dsp', 'ndl', 'dtg', 'fail', 'u2', 'k61l', 'rok', 'fkN']


def lists(text):
    start = text.index('int mode_client(')
    out = []
    for rx in LIST_RX:
        for m in re.finditer(rx, text):
            if m.start() > start:
                out.append((m.start(2), m.end(2), m.group(2)))
    return sorted(out)


def defined(text):
    start = text.index('int mode_client(')
    return set(re.findall(r'(?<![\w:])(\w+):(?!:)', text[start:]))


def moves(text):
    out = []
    labs = defined(text)
    for k, (a, b, s) in enumerate(lists(text)):
        sep = ', ' if ', ' in s else ','
        items = [x.strip() for x in s.split(',')]
        for i, x in enumerate(items):
            if len(items) > 1:
                n = items[:i] + items[i + 1:]
                out.append(('L%d-%s' % (k, x), text[:a] + sep.join(n) + text[b:]))
        for x in ADD:
            if x in labs and x not in items:
                n = items + [x]
                out.append(('L%d+%s' % (k, x), text[:a] + sep.join(n) + text[b:]))
    return out


def score(item):
    name, text = item
    s = mc1lib.score_text(text)
    if 'compile' in s:
        return name, 99999, text
    return name, 0 if s['identical'] else s['total'], text


def main():
    a = sys.argv[1:]
    base, pre = a[0], a[1]
    jobs = int(a[a.index('-j') + 1]) if '-j' in a else 4
    steps = int(a[a.index('-steps') + 1]) if '-steps' in a else 30
    cur = mc1lib.read_src(base)
    _, d0, _ = score(('base', cur))
    print('base', d0, mc1.count(cur)['total'], flush=True)
    seen = {cur}
    path = []
    for st in range(steps):
        mv = [m for m in moves(cur) if m[1] not in seen]
        with ThreadPoolExecutor(jobs) as ex:
            res = sorted(ex.map(score, mv), key=lambda r: r[1])
        best = res[0]
        print('step', st, 'moves', len(mv), 'top', [(r[0], r[1]) for r in res[:6]], flush=True)
        if best[1] >= d0:
            print('stuck at', d0, path, flush=True)
            break
        cur, d0 = best[2], best[1]
        seen.add(cur)
        path.append(best[0])
        open('%s_%d.c' % (pre, st), 'w', newline='\n').write(cur)
        print('took', best[0], d0, flush=True)
        if d0 == 0:
            print('IDENTICAL', path, mc1.count(cur)['total'], flush=True)
            break


if __name__ == '__main__':
    main()
