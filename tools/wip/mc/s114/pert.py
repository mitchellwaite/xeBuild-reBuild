# pert.py src out seed [scope]: randomize constants in __builtin_constant_p(var + K...) (semantics unchanged: never constant)
import re, sys, random
src, out, seed = sys.argv[1], sys.argv[2], int(sys.argv[3]); random.seed(seed)
t = open(src).read()
def rep(m):
    return '__builtin_constant_p(%s + %d)' % (m.group(1), random.randrange(1, 900000))
t = re.sub(r'__builtin_constant_p\((\w+) ?\+ ?\d+(?: \+ \d+)?\)', rep, t)
open(out, 'w', newline='\n').write(t)
