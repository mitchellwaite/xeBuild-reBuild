"""fl10c.py: 2D probe.  n dead tail tests (n_exits = 2 + n, PROBE ONLY) x one expect axis with a value.  For each state: per-getter score, and from
.optimized the (entry, pre, header, tail) of iniU32Invalid.  Output sorted, per-getter columns, in a10/map.txt.  Never a candidate."""
import os, re, sys, glob, subprocess, tempfile, shutil
from concurrent.futures import ThreadPoolExecutor
import fllib as L, fl10lib as F, fl10a as A

DEAD = ['if (key == NULL) return -1;', 'if (len < 0) return -1;', 'if (i < 0) return -1;']
GET = ['getIniBool', 'iniBoolInvalid', 'getIniU32', 'iniU32Invalid']


def body(n, ax):
    H = 'buf[i] == key[0]'
    M = 'j == len'
    T = '*q != 0'
    Lp = 'i < xb.iniSize - len'
    if 'H' in ax:
        H = '__builtin_expect(%s, 1)' % H
    if 'M' in ax:
        M = '__builtin_expect(%s, 1)' % M
    if 'T' in ax:
        T = '__builtin_expect(%s, 1)' % T
    if 'l' in ax:
        Lp = '__builtin_expect(%s, 1)' % Lp
    return """static int findKey(unsigned char *buf, const char *key)
{
	int i, j, len;
	unsigned char *p;
	len = strlen(key);
	for (i = 0; %s; i++) {
		if (%s) {
			p = &buf[i];
			for (j = 0; j < len; j++)
				if (p[j] != key[j])
					j = len + 1;
			if (%s) {
				unsigned char *q = &buf[i + len];

				%s
				if (%s)
					return i + len;
			}
		}
	}
	return -1;
}
""" % (Lp, H, M, ' '.join(DEAD[:n]), T)


def one(a):
    n, ax, pr = a
    src = F.fk(body(n, ax))
    tag = 'c%d%s_%d' % (n, ax, pr)
    d = os.path.join(F.A10, 'c', tag)
    os.makedirs(d, exist_ok=True)
    inp = ('#line 1 "filelist_ini.c"\n' + src).encode()
    fl = ['-O3', '-fdump-tree-optimized-blocks-details'] + (['--param', 'builtin-expect-probability=%d' % pr] if ax else [])
    subprocess.run([L.GCC, '-c'] + fl + ['-I' + os.path.join(L.R, 'src'), '-x', 'c', '-', '-o', 'x.o'], input=inp, cwd=d, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    o = os.path.join(d, 'x.o')
    if not os.path.exists(o):
        return (n, ax, pr, 10**7, {}, [])
    sc = F.nscore(o)
    fr = [b['freq'] for b in A.blocks(F.fn_part(d, 'optimized', 'iniU32Invalid'))]
    for f in glob.glob(os.path.join(d, '*')):
        os.remove(f)
    return (n, ax, pr, sc[0], sc[1], fr)


if __name__ == '__main__':
    axes = sys.argv[1].split(',')
    grid = [int(x) for x in sys.argv[2].split(',')]
    ns = [int(x) for x in sys.argv[3].split(',')]
    todo = [(n, a, p) for n in ns for a in axes for p in grid]
    with ThreadPoolExecutor(4) as ex:
        rs = list(ex.map(one, todo))
    with open(os.path.join(F.A10, 'map.txt'), 'a', newline='\n') as f:
        for n, ax, pr, sc, d, fr in rs:
            line = 'n=%d %-3s p=%-3d %5d  %s  [%s] freqs(entry pre.. )=%s' % (n, ax, pr, sc, ' '.join('%3d' % d.get(g, 0) for g in GET), 'o' if d.get('loadUserIni') else '', fr[:5] + fr[11:13])
            print(line)
            f.write(line + '\n')
