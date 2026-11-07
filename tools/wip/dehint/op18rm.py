#!/usr/bin/env python3
"""Attempt 18: single trick removals (op12x/op13 tables) re-measured on a base (default src).

python tools/wip/dehint/op18rm.py [-b base.c] [name|a+b ..]   (no names: every removal)"""
import os, sys
from concurrent.futures import ThreadPoolExecutor
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import optlib
import op13

RM = op13.RM


def run(base, combo):
    t = base
    for n in combo.split('+'):
        for old, new in RM[n]:
            if old not in t:
                return combo, {'compile': 'edit missing: ' + n}
            t = t.replace(old, new, 1)
    return combo, optlib.score_text(t)


def main():
    a = sys.argv[1:]
    base = optlib.SRC
    if '-b' in a:
        i = a.index('-b'); base = a[i + 1]; del a[i:i + 2]
    base = optlib.read_src(base)
    names = a or [n for n in RM if n not in ('pbe',)]
    with ThreadPoolExecutor(6) as ex:
        for c, r in ex.map(lambda c: run(base, c), names):
            print('%-12s %s' % (c, optlib.fmt(r)), flush=True)


if __name__ == '__main__':
    main()
