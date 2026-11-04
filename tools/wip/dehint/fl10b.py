"""fl10b.py: map which of findKey's edge probabilities give the target, using __builtin_expect + --param builtin-expect-probability
PURELY AS A PROBE (it is never a candidate).  Each axis sets one edge's probability:
  H: head compare true    M: j == len true    T: *q != 0 true (tail exit)    L: i < n false (latch exit)    J: inner mismatch true
Prints whole-object nscore per p and getter, and pre/tail frequencies from a dump for the best."""
import os, re, subprocess, sys
from concurrent.futures import ThreadPoolExecutor
import fllib as L, fl10lib as F


def body(ax):
    H = 'buf[i] == key[0]'
    M = 'j == len'
    T = '*q != 0'
    Lp = 'i < xb.iniSize - len'
    J = 'p[j] != key[j]'
    # expect(x, 1) => p; expect(x, 0) => 1-p.  Axis value is the probability the condition is TRUE
    if 'H' in ax:
        H = '__builtin_expect(%s, 1)' % H
    if 'M' in ax:
        M = '__builtin_expect(%s, 1)' % M
    if 'T' in ax:
        T = '__builtin_expect(%s, 1)' % T
    if 'L' in ax:
        Lp = '__builtin_expect(%s, 0)' % Lp  # loop stays with prob 1-p... see note
    if 'l' in ax:
        Lp = '__builtin_expect(%s, 1)' % Lp
    if 'J' in ax:
        J = '__builtin_expect(%s, 1)' % J
    return """static int findKey(unsigned char *buf, const char *key)
{
	int i, j, len;
	unsigned char *p;
	len = strlen(key);
	for (i = 0; %s; i++) {
		if (%s) {
			p = &buf[i];
			for (j = 0; j < len; j++)
				if (%s)
					j = len + 1;
			if (%s) {
				unsigned char *q = &buf[i + len];

				if (%s)
					return i + len;
			}
		}
	}
	return -1;
}
""" % (Lp, H, J, M, T)


def one(a):
    ax, pr = a
    src = F.fk(body(ax))
    tag = 'b%s_%d' % (ax, pr)
    o = L.compile(src, ['-O3', '--param', 'builtin-expect-probability=%d' % pr], tag)
    if o is None:
        return ax, pr, 10**7, {}, False
    n = F.nscore(o)
    return ax, pr, n[0], n[1], L.same(o)


if __name__ == '__main__':
    axes = sys.argv[1].split(',') if len(sys.argv) > 1 else ['H', 'M', 'T', 'l', 'J', 'HM', 'Ml', 'Hl', 'lT']
    grid = [10, 20, 28, 35, 40, 45, 50, 55, 60, 65, 70, 72, 75, 80, 85, 90, 91, 93, 94, 95, 96, 97, 98, 99]
    with ThreadPoolExecutor(4) as ex:
        rs = list(ex.map(one, [(a, p) for a in axes for p in grid]))
    with open(os.path.join(F.A10, 'probe_%s.txt' % '_'.join(axes)[:40]), 'w', newline='\n') as f:
        for ax, pr, n, d, s in rs:
            line = '%-3s p=%-3d %s %s' % (ax, pr, 'MATCH' if s else n, d)
            f.write(line + '\n')
            print(line)
