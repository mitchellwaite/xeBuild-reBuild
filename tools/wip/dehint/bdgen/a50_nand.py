"""Attempt 50: useNandData (a50_share.py's nand) at subsets of its sites, and its forms.
python tools/wip/dehint/bdgen/a46run.py tools/wip/dehint/bdgen/a50_nand.py [-p 95,99]
Label: B<fields in loadBlFiles>_C<fields in loadConsoleBlFiles>[_form]_<hint off>; fields k = kv, a = kvAlt, s = smc."""
import itertools, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import a46_m1hints as H
from a50_share import NAND_FN, ANCHOR, nand_old, split, sub, OFF

BASE = H.BASE
F = {'k': 'kv', 'a': 'kvAlt', 's': 'smc'}
FORMS = {
    'p': NAND_FN,
    # size first, then data (the stores in the other order)
    'z': NAND_FN.replace('\te->data = f->data;\n\te->size = f->size;\n\tf->data = NULL;\n\tf->size = 0;\n',
                         '\te->data = f->data;\n\te->size = f->size;\n\tf->size = 0;\n\tf->data = NULL;\n'),
    # returns the new size (console's case 2 passes it to smcSetLoad)
    'r': NAND_FN.replace('static void useNandData', 'static uint32_t useNandData')
                .replace('\tf->size = 0;\n}\n', '\tf->size = 0;\n\treturn e->size;\n}\n'),
}


def mk(bf, cf, form='p'):
    def g(t):
        pre, lb, lc, post = split(t)
        for c in bf:
            lb = sub(lb, nand_old(5, F[c]), '\t\t\t\t\tuseNandData(e, &xb.%s);\n' % F[c])
        for c in cf:
            lc = sub(lc, nand_old(5, F[c]), '\t\t\t\t\tuseNandData(e, &xb.%s);\n' % F[c])
        pre = sub(pre, ANCHOR, FORMS[form] + ANCHOR)
        return pre + lb + lc + post
    return g


subsets = [''.join(c) for n in range(0, 4) for c in itertools.combinations('kas', n)]
V = {}
offs = os.environ.get('A50_OFF', 'all').split(',')
forms = os.environ.get('A50_FORM', 'p').split(',')
for bf in subsets:
    for cf in subsets:
        if not bf and not cf:
            continue
        for form in forms:
            for k in offs:
                def f(t, bf=bf, cf=cf, form=form, p=OFF[k]):
                    t = mk(bf, cf, form)(t)
                    for a, b in p:
                        t = sub(t, a, b)
                    return t
                V['B%s_C%s_%s_%s' % (bf or '-', cf or '-', form, k)] = f
