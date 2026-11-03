# attempt 6: c2: every order of partial's three conditions with & or && between them (bitwise binds tighter)
import itertools, os
PART = "		partial = (len < 0x4000) & (type != 0) & (type != '0');\n"
C = ['(len < 0x4000)', '(type != 0)', "(type != '0')"]
F = []
for o in itertools.permutations(C):
    for a, b in itertools.product(('&', '&&'), repeat=2):
        F.append('%s %s %s %s %s' % (o[0], a, o[1], b, o[2]))
    F.append('%s && (%s & %s)' % o)
    F.append('(%s && %s) & %s' % o)
AXES = [[('f%d' % i, [(PART, '		partial = %s;\n' % f)]) for i, f in enumerate(F)],
        [('', []), ('b', [('	int partial;\n', '	_Bool partial;\n')])]]
BASE = os.environ.get('IWB', 'build/iw/a6/c2.c')
FLAGS = []
if __name__ == '__main__':
    for i, f in enumerate(F):
        print(i, f)
