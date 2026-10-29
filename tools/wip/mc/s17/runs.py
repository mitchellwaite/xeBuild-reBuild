"""s17: s10 best.json (or a design) + gcda --runs=R (probably-never-executed cutoff count*20 < R).
python tools/wip/mc/s17/runs.py SLOT design.json R [extra overrides...]"""
import json, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 's10'))
import run as r10
def go(slot, design, runs, extra=()):
    x = dict(design)
    f, inv, pre, o = r10.run(slot, x) if not runs and not extra else run2(slot, x, runs, extra)
    order = [l for l in o.splitlines() if l.startswith('order')]
    return f, inv, pre, order[0] if order else o[-500:]
def run2(slot, x, runs, extra):
    old = r10.FAKE
    r10.FAKE = old + (['--runs=%d' % runs] if runs else []) + list(extra)
    try:
        return r10.run(slot, x)
    finally:
        r10.FAKE = old
if __name__ == '__main__':
    print(*go(sys.argv[1], json.load(open(sys.argv[2])), int(sys.argv[3]), sys.argv[4:]))
