"""flfk2.py: findKey shape grid (no unreachable, pin optional), scored on the 4 getters."""
import itertools, sys
import fllib as L

s = L.base()
a = s.index('static int findKey(')
b = s.index('#define FIND')
HEAD = s[:a]
TAIL = s[b:]
PIN = '	__asm__("" :: "b"(val));\n'

SIG = {
 'buf': ('unsigned char *buf, const char *key', '', 'findKey(xb.iniBuf, key)', 'xb.iniSize'),
 'bufsize': ('unsigned char *buf, int size, const char *key', '', 'findKey(xb.iniBuf, xb.iniSize, key)', 'size'),
 'cbuf': ('const char *key', 'unsigned char *buf = xb.iniBuf;', 'findKey(key)', 'xb.iniSize'),
 'glob': ('const char *key', '#define buf xb.iniBuf', 'findKey(key)', 'xb.iniSize'),
}
COND = {
 'keyfirst': ('if (key[0] == buf[i]) {', '}'),
 'buffirst': ('if (buf[i] == key[0]) {', '}'),
 'cont': ('if (key[0] != buf[i]) continue; {', '}'),
}
LOOPJ = {
 'set': 'for (j = 0; j < len; j++) if (%s) j = len + 1;',
 'setbr': 'for (j = 0; j < len; j++) { if (%s) { j = len + 1; break; } }',
 'brk': 'for (j = 0; j < len; j++) if (%s) break;',
}
CMP = {'p': 'p[j] != key[j]', 'b': 'buf[i + j] != key[j]', 'r': 'key[j] != buf[i + j]', 'rp': 'key[j] != p[j]'}
CHECK = {
 'nest': 'if (j == len) { if (buf[i + len] != 0) return i + len; }',
 'and': 'if (j == len && buf[i + len] != 0) return i + len;',
 'jnest': 'if (j == len) { if (buf[i + j] != 0) return i + j; }',
 'eq0': 'if (j == len) { if (buf[i + len] == 0) continue; return i + len; }',
 'revcont': 'if (j != len) continue; if (buf[i + len] != 0) return i + len;',
 'pjret': 'if (j == len) { p += len; if (*p != 0) return i + len; }',
 'iret': 'if (j == len) { if (buf[i + len] != 0) { i += len; return i; } }',
 'ret': 'if (j == len) { if (buf[i + len] != 0) return i + len; else continue; }',
}
FOR = {'for': None, 'n': 'n'}


def fk(sig, cond, lj, cmp, chk, fr):
    params, pre, call, sz = SIG[sig]
    d = 'unsigned char *p;' if ('p[' in CMP[cmp] or 'p +=' in CHECK[chk]) else ''
    if 'p +=' in CHECK[chk]:
        d = 'unsigned char *p;'
    setp = 'p = &buf[i];' if d else ''
    n = ''
    lim = sz + ' - len'
    if fr == 'n':
        n = 'n = ' + lim + ';'
        lim = 'n'
    nd = 'int n;' if fr == 'n' else ''
    body = LOOPJ[lj] % CMP[cmp]
    c1, c2 = COND[cond]
    glob = pre if pre.startswith('#') else ''
    loc = pre if not pre.startswith('#') else ''
    t = """%s
static int findKey(%s)
{
	int i, j, len;
	%s %s %s
	len = strlen(key);
	%s
	for (i = 0; i < %s; i++) {
		%s
			%s
			%s
			%s
		%s
	}
	return -1;
}
%s
""" % (glob, params, d, nd, loc, n, lim, c1, setp, body, CHECK[chk], c2, '#undef buf' if glob else '')
    return HEAD + t + TAIL.replace('#define FIND findKey(xb.iniBuf, key)', '#define FIND ' + call)


if __name__ == '__main__':
    V = {}
    sel = sys.argv[1:]
    for k in itertools.product(SIG, COND, LOOPJ, CMP, CHECK, FOR):
        V['_'.join(k)] = fk(*k)
    print(len(V))
    rs = L.sweep(V, prefix='fk2', show=25)
    import collections
    print(collections.Counter(r[1][0] for r in rs).most_common(12))
    with open(L.BD + '/fk2.txt', 'w', newline='\n') as f:
        for n, (sc, st, fd, sd) in rs:
            f.write('%s %s %s %s\n' % (sc, n, fd, sd))
