"""Attempt 17, exp_upd: a first pair that fold turns into a range test.  The front end pairs the `||` chain into
two-leaf blocks; a pair of adjacent constants (9|10, 15|16, 24|25) becomes `(unsigned)(type - c) <= 1`, a compare
against 1, which gets the opcode-positive heuristic (73%) on top of the early return (61%): about 19% for the first
block, under the 23.8% rotate_loop needs (attempt 8).  23 then sits in a later pair, where its compare may still be
reused by the body's `type == 23`.  Axes: the first pair (6 orders) x every order of the other five (120), no
expect.  Runs on src as of d09240ad."""
import itertools, os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import bdrun

OLD = '''	return __builtin_expect(type == 23 || type == 15, 0) || type == 16 || type == 9 || type == 10 || type == 24 || type == 25;
'''
FIRST = [(9, 10), (10, 9), (15, 16), (16, 15), (24, 25), (25, 24)]
ALL = [9, 10, 15, 16, 23, 24, 25]


def CASES(base):
    out = []
    for f in FIRST:
        rest = [t for t in ALL if t not in f]
        for p in itertools.permutations(rest):
            ts = list(f) + list(p)
            new = '\treturn ' + ' || '.join('type == %d' % t for t in ts) + ';\n'
            out.append((' '.join(map(str, ts)), lambda b, new=new: bdrun.sub(b, OLD, new, 1)))
    return out


FOCUS = ['_addUpdateBls', '_isUpdateBl']
