"""Attempt 21, measurement only: gen_ir254's forms under flags that say which pass stands between them and the reference.
python gen_ir255.py <flag> [<flag>...]"""
import itertools, multiprocessing, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ir17lib import put, score
from gen_ir254 import Z, S, C, T, text

FLAGS = sys.argv[1:]


def one(k):
    return ('.'.join(k), score(put(text(*k)), FLAGS))


if __name__ == '__main__':
    keys = list(itertools.product(Z, S, C, T))
    with multiprocessing.Pool(4) as p:
        res = p.map(one, keys, 8)
    res = [x for x in res if x[1][0] != 'E']
    res.sort(key=lambda x: (x[1][1], x[1][0]))
    print(FLAGS)
    for k, r in res[:8]:
        print(k, r[0], r[1], r[3])
