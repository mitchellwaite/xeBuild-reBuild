#!/usr/bin/env python3
"""Attempt 30: trace lists of two dumps side by side, by block name (op13bb's naming with
the line number dropped), so different block ids don't matter.

python tools/wip/dehint/op30tr.py TAGA TAGB [-r N]   (only round N)
  prints both head sequences (round, head name[freq]) and marks the rows that differ"""
import os, re, subprocess, sys
H = os.path.dirname(os.path.abspath(__file__))
R = os.path.join(H, '..', '..', '..', 'build', 'v', 'aio_p1')


def traces(tag):
    t = subprocess.run([sys.executable, os.path.join(H, 'op13bb.py'), os.path.join(R, tag)],
                       capture_output=True, text=True).stdout
    out = []
    for line in t.splitlines():
        m = re.match(r'T(\d+)\s+r(\d)\s+(.*)$', line)
        if not m:
            continue
        items = re.findall(r'(\d+)\[(\d+)\](\S*)', m.group(3))
        nm = lambda s: re.sub(r'^\d+', '', s)
        out.append((int(m.group(2)), [(int(b), int(f), nm(s)) for b, f, s in items]))
    return out


def label(tr):
    b, f, s = tr[0]
    names = [x[2] for x in tr if x[2] not in ('', '-')]
    return '%d[%d]%s (%d)' % (b, f, names[0] if names else '-', len(tr))


if __name__ == '__main__':
    a = sys.argv[1:]
    rd = None
    if '-r' in a:
        i = a.index('-r'); rd = int(a[i + 1]); del a[i:i + 2]
    A, B = traces(a[0]), traces(a[1])
    if rd:
        A = [x for x in A if x[0] == rd]
        B = [x for x in B if x[0] == rd]
    n = max(len(A), len(B))
    for i in range(n):
        la = 'r%d %s' % (A[i][0], label(A[i][1])) if i < len(A) else ''
        lb = 'r%d %s' % (B[i][0], label(B[i][1])) if i < len(B) else ''
        sa = re.sub(r'^r\d \d+', '', la)
        sb = re.sub(r'^r\d \d+', '', lb)
        print('%s %-62s | %s' % (' ' if sa == sb else '*', la, lb))
