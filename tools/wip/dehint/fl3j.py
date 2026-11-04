"""fl3j.py: no pin, findKey forms: where the buf test sits, its arm, more than one, and the getter's val forms.
Frequencies are what's left to change LRA's register usage levelling for iniBoolInvalid's `len + 1`."""
import itertools
import fllib as L

L.FLAGS[:] = ['-O3']
B = L.base()
a = B.index('static int findKey(')
b = B.index('#define FIND')
PIN = '\t__asm__("" :: "b"(val));\n'
T = 'if (buf == NULL)\n\t\t\t\t\treturn -1;\n\t\t\t\t'


def fk(pos, arm, cond='buf == NULL'):
    t = {i: '' for i in range(6)}
    t[pos] = 'if (%s)\n\t\t%s\n\t\t' % (cond, arm)
    return '''static int findKey(unsigned char *buf, const char *key)
{
	int i, j, len;
	unsigned char *p;
	%slen = strlen(key);
	%sfor (i = 0; i < xb.iniSize - len; i++) {
		%sif (key[0] == buf[i]) {
			%sp = &buf[i];
			for (j = 0; j < len; j++)
				if (p[j] != key[j])
					j = len + 1;
			%sif (j == len) {
				unsigned char *q = &buf[i + len];

				%sif (*q != 0)
					return i + len;
			}
		}
	}
	return -1;
}
''' % tuple(t[i] for i in range(6))


V = {}
for pos, arm, cond, pin in itertools.product(range(6), ['return -1;', 'break;', 'continue;', 'len = 0;', 'i = 0;', 'j = 0;'], ['buf == NULL', 'xb.iniBuf == NULL', 'buf != xb.iniBuf'], [0, 1]):
    s = B[:a] + fk(pos, arm, cond) + B[b:]
    if not pin:
        s = L.sub(s, PIN, '')
    V['%d|%s|%s|%d' % (pos, arm, cond, pin)] = s
print(len(V))
rs = L.sweep(V, prefix='j3', show=40, workers=2)
with open(L.BD + '/a3/j3.txt', 'w', newline='\n') as f:
    for n, r in rs:
        f.write('%s\t%s\t%s\n' % (r[0], n, r[2]))
