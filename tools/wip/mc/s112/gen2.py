import sys
src = open('b0.c', newline='').read()
anchor = 'if (__builtin_constant_p(i + 320) && __builtin_constant_p(i + 321)) goto u2;'
assert src.count(anchor) == 1
def cp(base, k): return ' && '.join('__builtin_constant_p(i + %d)' % (base + j * 50000) for j in range(k))
tgt = sys.argv[1]; pre = sys.argv[2]
for k in range(1, 13):
    s = src.replace(anchor, anchor + ' if (%s) goto %s;' % (cp(880, k), tgt))
    open('%s%d.c' % (pre, k), 'w', newline='').write(s)
