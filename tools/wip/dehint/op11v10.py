"""Attempt 11: attempt 10's vlen tail forms (op10po.py's V, with setBool's expect kept) with
the literal order of the three tail messages (u, i, b; the reference is uib).

python tools/wip/dehint/op11v10.py [V ...]"""
import os, sys
from concurrent.futures import ThreadPoolExecutor
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import optlib, op10po, op11tail


def run(v):
    t = op10po.make(optlib.read_src(optlib.SRC), 'E', v)
    return v, optlib.score_text(t), op11tail.order(t)


if __name__ == '__main__':
    vs = sys.argv[1:] or list(op10po.V)
    with ThreadPoolExecutor(8) as ex:
        for v, r, o in sorted(ex.map(run, vs), key=lambda x: x[1].get('total', 99999)):
            print('%-5s %-4s %s' % (v, o, optlib.fmt(r)))
