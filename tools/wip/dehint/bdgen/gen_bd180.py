"""exp_upd: isUpdateBl's own profile decides.  The front end folds `a == x || a == y` pairs into one non-short-circuit test, so type == 23 shares its test with the next type at 39% (early return alone).
A lone == test gets nonequal as well: 19.9%, under the 23.8% rotate_loop needs against the bit test's edge.  Parentheses change the pairing."""
import itertools

OLD = 'return __builtin_expect(type == 23 || type == 15, 0) || type == 16 || type == 9 || type == 10 || type == 24 || type == 25;'
PAIRS = {'a': (9, 10), 'b': (15, 16), 'c': (24, 25)}


def eq(x):
    return 'type == %d' % x


def CASES(base):
    out = []
    for order in itertools.permutations('abc'):
        for flips in itertools.product((0, 1), repeat=3):
            ps = []
            for g, fl in zip(order, flips):
                x, y = PAIRS[g]
                ps.append((y, x) if fl else (x, y))
            flat = [v for p in ps for v in p]
            forms = {
                'rest': 'type == 23 || (' + ' || '.join(map(eq, flat)) + ')',
                'pairs': 'type == 23 || ' + ' || '.join('(%s || %s)' % (eq(a), eq(b)) for a, b in ps),
                'both': 'type == 23 || (' + ' || '.join('(%s || %s)' % (eq(a), eq(b)) for a, b in ps) + ')',
                'tail': 'type == 23 || ' + eq(flat[0]) + ' || (' + ' || '.join(map(eq, flat[1:])) + ')',
                'right': 'type == 23 || (' + eq(flat[0]) + ' || (' + eq(flat[1]) + ' || (' + eq(flat[2]) + ' || (' + eq(flat[3]) + ' || (' + eq(flat[4]) + ' || ' + eq(flat[5]) + ')))))',
            }
            for n, s in forms.items():
                out.append(('%s %s %s' % (n, ''.join(order), ''.join(map(str, flips))), base.replace(OLD, 'return ' + s + ';')))
    return out


FOCUS = ['_addUpdateBls', '_isUpdateBl']
