"""Attempt 7: a helper's own profile_estimate (predictions, block frequencies, edges, code).

python tools/wip/dehint/op7pe.py file.c fn [fn...] [-c]
For each function: the 'Predictions for bb' summaries, then every block's frequency with
its succ edges and probabilities; -c also prints the block bodies (calls, conds, returns).
Used to read the probabilities the hinted copies give and to compare natural helpers."""
import os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import opfq

BB = re.compile(r'^;; basic block (\d+), loop depth \d+, count \d+, freq (\d+)')
SUCC = re.compile(r'^;;\s+(?:succ:)?\s+(\w+) \[([0-9.]+)%\]')


def show(dt, name, code=False):
    i = dt.find(';; Function %s ' % name)
    if i < 0:
        print('no', name)
        return
    j = i
    while True:   # the dump repeats the header for the same function
        j = dt.find('\n;; Function ', j + 1)
        if j < 0 or not dt.startswith(';; Function %s ' % name, j + 1):
            break
    body = dt[i:j if j > 0 else None]
    lines = body.split('\n')
    for l in lines:
        if l.startswith('Predictions for bb'):
            print('  ' + l)
        elif 'heuristics' in l and 'ignored' not in l and 'first match' not in l:
            print('    ' + l.strip())
    cur = None
    insucc = False
    out = []
    for l in lines:
        if re.match(r'^\d+ basic blocks', l):
            out = []
            cur = None
            continue
        m = BB.match(l)
        if m:
            if cur:
                out.append(cur)
            cur = [int(m.group(1)), int(m.group(2)), []]
            insucc = False
            continue
        if cur is None:
            continue
        if l.startswith(';;  succ:'):
            insucc = True
        elif l.startswith(';;  pred:') or l.startswith(';;  prev'):
            insucc = False
        if insucc:
            s = SUCC.match(l)
            if s:
                cur[2].append('%s[%s]' % (s.group(1), s.group(2)))
        if not l.startswith(';;'):
            if cur:
                out.append(cur)
            cur = None
            if re.match(r'^\d+ basic blocks', l):
                out = []
    if cur:
        out.append(cur)
    for bb, fr, su in out:
        print('  bb%-3d f%-6d -> %s' % (bb, fr, ' '.join(su)))
    if code:
        k = body.find('\n{')
        for l in body[k:].split('\n'):
            ls = l.strip()
            if ls.startswith('<bb') or ls.startswith('if ') or 'goto' in ls or '(' in ls and ';' in ls and not ls.startswith(';;') or ls.startswith('return'):
                print('    ' + ls[:100])


def main():
    a = sys.argv[1:]
    code = '-c' in a
    a = [x for x in a if x != '-c']
    dt, d = opfq.dump(open(a[0]).read())
    if dt is None:
        return
    for n in a[1:]:
        print('==== ' + n)
        show(dt, n, code)


if __name__ == '__main__':
    main()
