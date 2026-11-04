"""fl10lib: attempt 10's helpers.  Base is src/filelist_ini.c, split round findKey.

fk(body, pre='', post='') -> source with findKey's definition (not FIND's macro) replaced by pre + body
run({name: src}) -> sorted whole-object scores (nscore: branch targets blanked), logged in build/filelist_ini/a10/
dump(src, tag, fn=None, passes=...) -> dict of pass -> text of function fn from gcc's dumps
"""
import difflib, glob, os, re, subprocess, sys, json
from concurrent.futures import ThreadPoolExecutor
import fllib as L

A10 = os.path.join(L.BD, 'a10')
os.makedirs(A10, exist_ok=True)
O3 = ['-O3']
S0 = open(os.path.join(L.R, 'src', 'filelist_ini.c'), newline='').read()
A = S0.index("/* getters' own helper (not memFindStr) */")
B = S0.index("#define FIND findKey(xb.iniBuf, key)")
HEAD, TAIL = S0[:A], S0[B:]

KF_NONE = """static int findKey(unsigned char *buf, const char *key)
{
	int i, j, len;
	unsigned char *p;
	len = strlen(key);
	for (i = 0; i < xb.iniSize - len; i++) {
		if (buf[i] == key[0]) {
			p = &buf[i];
			for (j = 0; j < len; j++)
				if (p[j] != key[j])
					j = len + 1;
			if (j == len) {
				unsigned char *q = &buf[i + len];

				if (*q != 0)
					return i + len;
			}
		}
	}
	return -1;
}
"""

MATCHAT = """static int matchAt(unsigned char *p, const char *key, int len)
{
	int j;

	for (j = 0; j < len; j++)
		if (p[j] != key[j])
			j = len + 1;
	if (j == len)
		return 1;
	return 0;
}

static int findKey(unsigned char *buf, const char *key)
{
	int i, len;
	len = strlen(key);
	for (i = 0; i < xb.iniSize - len; i++) {
		if (buf[i] == key[0]) {
			if (matchAt(&buf[i], key, len)) {
				unsigned char *q = &buf[i + len];

				if (*q != 0)
					return i + len;
			}
		}
	}
	return -1;
}
"""


def fk(body, pre=''):
    return HEAD + pre + body + TAIL


def norm(fns):
    return {k: [re.sub(r'\.[0-9a-f]+$', '.L', l) if l.startswith('j') or 'j' == l[:1] else l for l in v] for k, v in fns.items()}


def nscore(o):
    if o is None:
        return 10**7, {}
    a, b = norm(L.dis(L.REF)), norm(L.dis(o))
    r = {}
    for k in a:
        if a[k] != b.get(k):
            r[k.lstrip('_')] = sum(1 for x in difflib.ndiff(a[k], b.get(k, [])) if x[0] in '+-')
    secs = L.secdiff(o)
    return sum(r.values()), r, secs


def run(V, name, workers=4, show=25):
    def one(kv):
        n, s = kv
        tag = 'a10_%s_%d' % (re.sub(r'\W', '_', n)[:60], os.getpid())
        o = L.compile(s, O3, tag)
        if o is None:
            return n, (10**7, {}, []), False
        return n, nscore(o), L.same(o)
    with ThreadPoolExecutor(workers) as ex:
        rs = list(ex.map(one, V.items()))
    rs.sort(key=lambda x: (not x[2], x[1][0]))
    with open(os.path.join(A10, name + '.txt'), 'w', newline='\n') as f:
        for n, sc, same in rs:
            f.write('%s %s %s %s\n' % ('MATCH' if same else sc[0], n, sc[1], sc[2] if len(sc) > 2 else ''))
    for n, sc, same in rs[:show]:
        print('MATCH' if same else sc[0], n, sc[1], sc[2] if len(sc) > 2 else '')
    return rs


def diff(src, tag='a10show', n=1):
    o = L.compile(src, O3, tag)
    print('==', nscore(o), 'same' if L.same(o) else '')
    a, b = norm(L.dis(L.REF)), norm(L.dis(o))
    for k in a:
        if a[k] != b.get(k):
            print('--', k)
            print('\n'.join(l for l in difflib.unified_diff(a[k], b.get(k, []), lineterm='', n=n) if not l.startswith(('---', '+++'))))


DEF_DUMPS = ['-fdump-tree-einline-blocks-details', '-fdump-tree-profile_estimate-blocks-details', '-fdump-tree-optimized-blocks-details',
             '-fdump-ipa-inline-details', '-fdump-rtl-ira', '-fdump-rtl-reload']


def dumps(src, tag, flags=DEF_DUMPS):
    d = os.path.join(A10, 'd', tag)
    os.makedirs(d, exist_ok=True)
    for f in glob.glob(os.path.join(d, '*')):
        os.remove(f)
    inp = ('#line 1 "filelist_ini.c"\n' + src).encode()
    p = subprocess.run([L.GCC, '-c', '-O3'] + list(flags) + ['-I' + os.path.join(L.R, 'src'), '-x', 'c', '-', '-o', 'x.o'],
                       input=inp, cwd=d, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if p.returncode:
        print(p.stderr.decode(errors='replace')[:800])
    return d


def fn_part(d, suf, fn):
    fs = glob.glob(os.path.join(d, '*' + suf))
    t = open(fs[0], errors='replace').read()
    for part in re.split(r'(?m)^(?=;; Function )', t):
        if part.startswith(';; Function %s ' % fn):
            return part
    return ''


if __name__ == '__main__':
    what = sys.argv[1]
    if what == 'base':
        run({'src': S0, 'none': fk(KF_NONE), 'matchAt': fk(MATCHAT)}, 'base')
    elif what == 'diff':
        diff({'none': fk(KF_NONE), 'matchAt': fk(MATCHAT), 'src': S0}[sys.argv[2]])
