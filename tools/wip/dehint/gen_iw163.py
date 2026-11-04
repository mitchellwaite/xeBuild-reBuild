# attempt 10: pin_hdr gone.  Threading rebuilds the chain's flows from the incoming edges, so a test after the loop (gen_iw162) doesn't count: only the mismatch edge's own
# probability does.  PRED_LOOP_EXIT is 9% / n_exits; forms with one exit test on a flag (predict_extra_loop_exits, 9% on the paths into the PHI) or that bypass it (continue).
# Wanted per byte: 5-15% in the spare loop, 6-8% in the data loop.  Good: finalizeImage 57 and nothing else.
import os
PIN = '			__asm__("" :: "a"(xb.hdr));\n'
PE = '''	int i;

	for (i = 0; i < 512; i++)
		if (data[i] != 0xff)
			return 0;
	for (i = 0; i < 16; i++)
		if (spare[i] != 0xff)
			return 0;
	return 1;
'''
def forms(p, n):
    return {
     'f1': '	ok = 1;\n	for (i = 0; ok && i < %s; i++)\n		ok = %s[i] == 0xff;\n',
     'f2': '	ok = 1;\n	for (i = 0; i < %s && ok; i++)\n		if (%s[i] != 0xff)\n			ok = 0;\n',
     'f3': '	ok = 1;\n	for (i = 0; ok && i < %s; i++)\n		if (%s[i] != 0xff)\n			ok = 0;\n',
     'f4': '	ok = 1;\n	i = 0;\n	do {\n		ok = %s[i] == 0xff;\n	} while (ok && ++i < %s);\n',
     'f5': '	ok = 1;\n	i = 0;\n	while (ok && i < %s)\n		ok = %s[i++] == 0xff;\n',
     'f6': '	for (i = 0;; i++) {\n		ok = i < %s && %s[i] == 0xff;\n		if (!ok)\n			break;\n	}\n	ok = i == N;\n',
     'f7': '	for (i = 0; i < %s; i++) {\n		ok = %s[i] == 0xff;\n		if (!ok)\n			break;\n	}\n',
     'c1': '	ok = 1;\n	for (i = 0; i < %s; i++) {\n		if (%s[i] == 0xff)\n			continue;\n		ok = 0;\n		break;\n	}\n',
     'c2': '	ok = 1;\n	for (i = 0; i < %s; i++) {\n		if (%s[i] != 0xff) {\n			ok = 0;\n			break;\n		}\n	}\n',
     'c3': '	ok = 1;\n	for (i = 0; i < %s; i++) {\n		if (%s[i] != 0xff)\n			goto out;\n		continue;\nout:\n		ok = 0;\n		break;\n	}\n',
    }
def mk(p, n, k):
    t = forms(p, n)[k]
    if k == 'f4':
        return t % (p, n)
    return (t % (n, p)).replace('N;', n + ';')
SP = {k: mk('spare', '16', k) + '	return ok;\n' for k in forms('', '')}
DA = {k: mk('data', '512', k) + '	if (!ok)\n		return 0;\n' for k in forms('', '')}
D0 = '''	for (i = 0; i < 512; i++)
		if (data[i] != 0xff)
			return 0;
'''
S0 = '''	for (i = 0; i < 16; i++)
		if (spare[i] != 0xff)
			return 0;
	return 1;
'''
AXES = [
 [('nopin', [(PIN, ''), (PE, '	int i, ok;\n\n' + D0 + S0)])],
 [('', [])] + [('D' + k, [(D0 + S0, DA[k] + S0)]) for k in DA] + [('S' + k, [(D0 + S0, D0 + SP[k])]) for k in SP],
]
BASE = os.environ.get('IWB', 'src/image_write.c')
FLAGS = []
