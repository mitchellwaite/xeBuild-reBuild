"""isUpdateBl with no expect: its adjacent types written as ranges.  A range test has no NONEQUAL prediction, so the bit test's stale last-edge probability
(reassoc keeps the last test's) rises from 29% and the loop rotation can pick it over type == 23's edge.  Groups in every order, 23 first or last in its place."""
import itertools

OLD = 'return __builtin_expect(type == 23 || type == 15, 0) || type == 16 || type == 9 || type == 10 || type == 24 || type == 25;'
G = {
    'a': {'e': 'type == 9 || type == 10', 'E': 'type == 10 || type == 9', 'r': '(type >= 9 && type <= 10)'},
    'b': {'e': 'type == 15 || type == 16', 'E': 'type == 16 || type == 15', 'r': '(type >= 15 && type <= 16)'},
    'c': {'e': 'type == 24 || type == 25', 'E': 'type == 25 || type == 24', 'r': '(type >= 24 && type <= 25)', 'R': 'type == 23 || (type >= 24 && type <= 25)'},
}


def CASES(base):
    out = []
    for order in itertools.permutations('abc'):
        for forms in itertools.product('eEr', repeat=3):
            s = ' || '.join(G[g][f] for g, f in zip(order, forms))
            for first in ('23', 'r23'):
                if first == '23':
                    x = 'return type == 23 || ' + s + ';'
                else:
                    x = 'return ' + s + ' || type == 23;'
                out.append(('%s %s %s' % (first, ''.join(order), ''.join(forms)), base.replace(OLD, x)))
    return out


FOCUS = ['_addUpdateBls', '_isUpdateBl']
