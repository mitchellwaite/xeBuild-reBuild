"""fl3f.py: with findKey's `if (buf == NULL) return -1;`: simpler tails, then natural tests in place of
iniBoolInvalid's pin (in the getter, after val is set; also at other points)."""
import itertools, sys
import fllib as L

L.FLAGS[:] = ['-O3']
B = L.base()
UNR = '''				unsigned char *q = &buf[i + len];

				if (q == 0)
					__builtin_unreachable();
				if (*q != 0)
					return i + len;
'''
GOOD = '''				unsigned char *q = &buf[i + len];

				if (buf == NULL)
					return -1;
				if (*q != 0)
					return i + len;
'''
TAILS = {
 'good': GOOD,
 'noq': '\t\t\t\tif (buf == NULL)\n\t\t\t\t\treturn -1;\n\t\t\t\tif (buf[i + len] != 0)\n\t\t\t\t\treturn i + len;\n',
 'noq2': '\t\t\t\tif (buf != NULL) {\n\t\t\t\t\tif (buf[i + len] != 0)\n\t\t\t\t\t\treturn i + len;\n\t\t\t\t} else\n\t\t\t\t\treturn -1;\n',
 'p': '\t\t\t\tif (p == NULL)\n\t\t\t\t\treturn -1;\n\t\t\t\tif (buf[i + len] != 0)\n\t\t\t\t\treturn i + len;\n',
 'brk': '\t\t\t\tif (buf == NULL)\n\t\t\t\t\tbreak;\n\t\t\t\tif (buf[i + len] != 0)\n\t\t\t\t\treturn i + len;\n',
}
PIN = '\t__asm__("" :: "b"(val));\n'
S0 = {k: L.sub(B, UNR, v) for k, v in TAILS.items()}

if sys.argv[1] == 'tail':
    V = {}
    for k, s in S0.items():
        V[k] = s
        V[k + '_nopin'] = L.sub(s, PIN, '')
    L.sweep(V, prefix='f3')
else:
    base = S0[sys.argv[2]] if len(sys.argv) > 2 else S0['good']
    CONDS = ['val == NULL', 'off < 0', 'off == -1', 'off < -1', 'xb.iniBuf == NULL', 'xb.iniSize == 0', 'xb.iniSize < 0', 'xb.iniSize <= off', 'off >= xb.iniSize', 'off > xb.iniSize',
             'key == NULL', 'val[0] == 0', '*val == 0', '!val[0]', 'val < (char *)xb.iniBuf', 'val != (char *)&xb.iniBuf[off]', 'xb.iniBuf != (unsigned char *)val - off']
    ARMS = {'null': 'return NULL;', 'off': 'off = 0;', 'val': 'val = NULL;', 'sz': 'xb.iniSize = 0;', 'key': 'return (char *)key;', 'v': 'return val;'}
    V = {}
    for c, (an, arm) in itertools.product(CONDS, ARMS.items()):
        V['%s|%s' % (c, an)] = L.sub(base, PIN, '\tif (%s)\n\t\t%s\n' % (c, arm))
    # after the "true" test, before the "false" test
    T = '\tif (strnicmp(val, "true", 4) == 0)\n\t\treturn NULL;\n\tif (strnicmp(val, "false", 5) != 0)\n\t\treturn val;\n\treturn NULL;\n'
    s1 = L.sub(base, PIN, '')
    for c, (an, arm) in itertools.product(CONDS, ARMS.items()):
        V['%s|%s|mid' % (c, an)] = L.sub(s1, T, '\tif (strnicmp(val, "true", 4) == 0)\n\t\treturn NULL;\n\tif (%s)\n\t\t%s\n\tif (strnicmp(val, "false", 5) != 0)\n\t\treturn val;\n\treturn NULL;\n' % (c, arm))
        V['%s|%s|ret' % (c, an)] = L.sub(s1, T, '\tif (strnicmp(val, "true", 4) == 0)\n\t\treturn NULL;\n\tif (strnicmp(val, "false", 5) != 0) {\n\t\tif (%s)\n\t\t\t%s\n\t\treturn val;\n\t}\n\treturn NULL;\n' % (c, arm))
    print(len(V))
    rs = L.sweep(V, prefix='f3p', show=30)
    with open(L.BD + '/a3/f3p.txt', 'w', newline='\n') as f:
        for n, r in rs:
            f.write('%s\t%s\t%s\n' % (r[0], n, r[2]))
