"""fl5h.py single BASE | rand N seed BASE: everything else, around a base state given as an fl5f label (`hsec=cn|off4`): fl5f's axes, fl5c's axes,
and raw-section forms.  Labels: `<fl5f axes>;<fl5c axes>;<extra>|tests`."""
import random, sys
import fllib as L, fl5lib as F, fl5f as X
import fl5c as C

RAWIF = '\t\t\tif (comma == -1 || comma >= nul) {\n'
EXTRA = {
    # raw's bad-entry test
    'rawnl': (RAWIF, '\t\t\tif (comma == -1 || nul <= comma) {\n'),
    'rawlt': (RAWIF, '\t\t\tif (comma < 0 || comma >= nul) {\n'),
    'rawsplit': (RAWIF + '''				log_printf(0, "\\n******* ERROR: an entry in [rawpatch] is missing offset info!\\n");
				free(buf);
				return 0;
			}
''', '''			if (comma == -1) {
				log_printf(0, "\\n******* ERROR: an entry in [rawpatch] is missing offset info!\\n");
				free(buf);
				return 0;
			}
			if (comma >= nul) {
				log_printf(0, "\\n******* ERROR: an entry in [rawpatch] is missing offset info!\\n");
				free(buf);
				return 0;
			}
'''),
    'rawgood': ('''			if (comma == -1 || comma >= nul) {
				log_printf(0, "\\n******* ERROR: an entry in [rawpatch] is missing offset info!\\n");
				free(buf);
				return 0;
			}
			if (comma <= 1023) {
''', '''			if (comma != -1 && comma < nul) {
				if (comma > 1023) {
					log_printf(0, "\\n******* ERROR: file name in [rawpatch] is too long!\\n");
					free(buf);
					return 0;
				}
			} else {
				log_printf(0, "\\n******* ERROR: an entry in [rawpatch] is missing offset info!\\n");
				free(buf);
				return 0;
			}
			{
'''),
    'raword': ("\t\t\tnul = memFindChar(p, 0, size - pos);\n\t\t\tcomma = memFindChar(p, ',', size - pos);\n\t\t\tif (comma == -1",
               "\t\t\tcomma = memFindChar(p, ',', size - pos);\n\t\t\tnul = memFindChar(p, 0, size - pos);\n\t\t\tif (comma == -1"),
    'rawp': ('\t\t\tp = &buf[pos];\n\t\t\tnul = memFindChar(p, 0, size - pos);\n\t\t\tcomma = memFindChar(p, \',\', size - pos);\n\t\t\tif (comma == -1',
             '\t\t\tnul = memFindChar(&buf[pos], 0, size - pos);\n\t\t\tcomma = memFindChar(&buf[pos], \',\', size - pos);\n\t\t\tp = &buf[pos];\n\t\t\tif (comma == -1'),
}


def parse(lb):
    a, _, t = lb.partition('|')
    f, _, rest = a.partition(';')
    cc, _, ex = rest.partition(';')
    return (dict(x.split('=') for x in f.split(',') if x), dict(x.split('=') for x in cc.split(',') if x),
            [x for x in ex.split(',') if x], tuple(x for x in t.split('+') if x))


def gen(fc, cc, ex, t):
    s = X.gen(fc, t)
    for a in C.ORDER:
        if a in cc:
            if a == 'base' and 'tool' in cc:
                continue
            s = C.AX[a][cc[a]](s)
    for e in ex:
        s = L.sub(s, *EXTRA[e])
    return s


def lab(fc, cc, ex, t):
    return '%s;%s;%s|%s' % (','.join('%s=%s' % kv for kv in sorted(fc.items())), ','.join('%s=%s' % kv for kv in sorted(cc.items())), ','.join(ex), '+'.join(t))


if __name__ == '__main__':
    V = {}
    mode = sys.argv[1]
    if mode == 'single':
        fc0, cc0, ex0, t0 = parse(sys.argv[2])
        V[lab(fc0, cc0, ex0, t0)] = gen(fc0, cc0, ex0, t0)
        for a in X.AX:
            for v in X.AX[a]:
                fc = dict(fc0)
                fc[a] = v
                V[lab(fc, cc0, ex0, t0)] = gen(fc, cc0, ex0, t0)
        for a in C.ORDER:
            for v in C.AX[a]:
                cc = dict(cc0)
                cc[a] = v
                try:
                    V[lab(fc0, cc, ex0, t0)] = gen(fc0, cc, ex0, t0)
                except (ValueError, AttributeError, AssertionError) as x:
                    pass
        for e in EXTRA:
            try:
                V[lab(fc0, cc0, ex0 + [e], t0)] = gen(fc0, cc0, ex0 + [e], t0)
            except ValueError as x:
                sys.stderr.write('skip %s %s\n' % (e, str(x)[:70]))
    print(len(V))
    F.run(V, 'h', show=int(sys.argv[3]) if len(sys.argv) > 3 else 25)
