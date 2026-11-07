"""Attempt 38: loadBl's signature block with `break` closing the arms that leave *pr at 0.  After the no-key log and
the passed log *pr is 0 and the type is 5, 11 or 17, so the tail does nothing for them (type <= 5: `*pr` is 0, break;
type > 5: not 14, break): a `break` there is the same behaviour.  It takes those paths off the tail's merge block at
profile_estimate (the merge's `<= 5` test and vrp1's joiner copies of it are what t5le / exp_pr set) and gives the
arms the early-return predictor.  The failed arm must still reach the tail (attempt 14).  Axes: which arms break x
`else if (type)` or a plain else x hints t5le / exp_pr / both kept or off.
Run: python tools/wip/dehint/bdrun.py tools/wip/dehint/bdgen/gen_bd501.py"""
import itertools, os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import bdhints, bdrun

PASS = '\t\t\t\t\tlog_printf(1, "loaded %s, signature check passed!\\n", e->name);\n'
NOKEY = '\t\t\t\tlog_printf(1, "loaded %s, could not check signature rsa key not present!\\n", e->name);\n'
DEAD = ('\t\t\t\t/* Borderline, for review: type is 5, 11 or 17 here, so this test\n'
        '\t\t\t\t   is always true; a plain else costs 54 lines */\n'
        '\t\t\t\t} else if (type)\n')


def mk(b, nk, ok, dead, offs):
    old = DEAD + PASS + '\t\t\t} else\n' + NOKEY + '\t\t}\n'
    g = '\t\t\t\t} else if (type)' if dead else '\t\t\t\t} else'
    if ok:
        p = g + ' {\n' + PASS + '\t\t\t\t\tbreak;\n\t\t\t\t}\n'
    else:
        p = g + '\n' + PASS
    if nk:
        n = '\t\t\t} else {\n' + NOKEY + '\t\t\t\tbreak;\n\t\t\t}\n'
    else:
        n = '\t\t\t} else\n' + NOKEY
    b = bdrun.sub(b, old, p + n + '\t\t}\n', 1)
    return bdhints.off(b, *offs) if offs else b


def CASES(base):
    out = []
    for nk, ok, dead in itertools.product([0, 1], [0, 1], [1, 0]):
        for offs in [(), ('lab_t5le',), ('exp_pr',), ('lab_t5le', 'exp_pr')]:
            if not nk and not ok and dead and not offs:
                lab = 'src'
            else:
                lab = 'nk%d ok%d dead%d -%s' % (nk, ok, dead, '-'.join(offs) or 'none')
            out.append((lab, lambda b, c=(nk, ok, dead, offs): mk(b, *c)))
    return out


FOCUS = ['_loadBlFiles']
