"""findSmcConfig (attempt 12): the scan loops as the Linux build suggests, with no expects and no pin.
tmp/xeBuild64's loops re-test the loop condition after a hit (`cmp eax,1; je <bound test>` with i not advanced), so its
source tests `found != 1` in the loop condition and only advances i on a miss; gcc 6 threads that re-test away, which is
the Windows build's fallthrough into the found block.  Axes: loop statement, condition order, how the advance is
written."""
import itertools, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
import bdhints, bdrun

LOOPS = {
    'wh': '''	while (i + N <= size && found != 1) {
		found = smcConfigOk(buf + i);
		if (found != 1)
			i += N;
	}
''',
    'whf': '''	while (found != 1 && i + N <= size) {
		found = smcConfigOk(buf + i);
		if (found != 1)
			i += N;
	}
''',
    'wh2': '''	while (i + N <= size && found != 1)
		if ((found = smcConfigOk(buf + i)) != 1)
			i += N;
''',
    'for': '''	for (; i + N <= size && found != 1; ) {
		found = smcConfigOk(buf + i);
		if (found != 1)
			i += N;
	}
''',
    'whe': '''	while (i + N <= size && found != 1) {
		found = smcConfigOk(buf + i);
		if (found == 1)
			continue;
		i += N;
	}
''',
}
HEADS = {
    'reset': True,   # i = 0 before each loop
}


def CASES(base):
    t0 = bdhints.off(base, 'exp_200', 'exp_210', 'pin_i')
    i, j = bdrun.fnspan(t0, 'static int findSmcConfig(')
    out = []
    for k1, k2 in itertools.product(LOOPS, ['same', 'plain']):
        l1 = LOOPS[k1].replace('N', '0x200')
        l2 = (LOOPS[k1] if k2 == 'same' else LOOPS['wh']).replace('N', '0x210')
        l2 = ''.join('\t' + l if l.strip() else l for l in l2.splitlines(True))
        fn = ('static int findSmcConfig(uint8_t *buf, int size, uint32_t *pos)\n{\n\tuint32_t i = 0;\n\tint found = 0;\n\n' + l1 +
              '\tif (!found) {\n\t\ti = 0;\n' + l2 + '\t}\n\t*pos = i;\n\treturn found;\n}\n')
        out.append(('%s %s' % (k1, k2), t0[:i] + fn + t0[j:]))
    return out


FOCUS = ['_extractSmcConfig']
