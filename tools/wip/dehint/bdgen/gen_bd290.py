"""Attempt 18, exp_upd: type == 23 alone in isUpdateBl's first block, kept alone by a second operand fold can't merge.

fold_truth_andor turns `a || b` into `a | b` only when both sides are simple comparisons; a parenthesized group of
three or more tests becomes `range | x` (a TRUTH_OR, not simple), so `type == 23 || (three tests) || ..` keeps 23 in a
block of its own with nonequal + early return (19.9%, under the 23.8% rotate_loop needs).  Attempt 7's gen_bd180 only
had groups of two (which fold makes a simple range test and merges with 23) or all six.  Axes: the group after 23
(every 3- and 4-subset of the other six, in sorted order or with the range pair first), and the order of what's left.
No expect.  Runs on src as of 8b56de61."""
import itertools, os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import bdrun

OLD = 'return __builtin_expect(type == 23 || type == 15, 0) || type == 16 || type == 9 || type == 10 || type == 24 || type == 25;'
REST = [15, 16, 9, 10, 24, 25]


def eq(x):
    return 'type == %d' % x


def CASES(base):
    out = []
    seen = set()
    for k in (3, 4):
        for grp in itertools.combinations(REST, k):
            left = [t for t in REST if t not in grp]
            for g in set(itertools.permutations(grp)):
                if len(out) > 4000:
                    break
                for lo in set(itertools.permutations(left)):
                    s = 'type == 23 || (' + ' || '.join(map(eq, g)) + ')' + ''.join(' || ' + eq(t) for t in lo)
                    if s in seen:
                        continue
                    seen.add(s)
                    out.append((s, lambda b, s=s: bdrun.sub(b, OLD, 'return ' + s + ';', 1)))
    return out


FOCUS = ['_addUpdateBls', '_isUpdateBl']
