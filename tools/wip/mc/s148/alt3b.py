import sys, ast
sys.argv = ['x', sys.argv[1], '0']; exec(open('alt.py').read())
P = [ast.literal_eval(l.split(' ', 2)[2]) for l in open('alt2.out') if l.startswith('2 2 ')]
best = 99
for p in P:
    for c in CH:
        cs = list(p) + [c]
        if c in p or not ok(cs): continue
        s = score(run(cs)); best = min(best, s)
        if s <= 1: print(s, cs)
print('best', best)
