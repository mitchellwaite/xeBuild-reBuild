"""extractSmcConfig (attempt 12): gen_bd233's Linux-style scan loops written in extractSmcConfig itself (findSmcConfig
gone), no expects, no pin.  Axes: loop form, how the not-found case is written, where found and i are set to 0."""
import itertools, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
import bdhints, bdrun

LOOP = '''	while (i + N <= size && found != 1) {
		found = smcConfigOk(buf + i);
		if (found != 1)
			i += N;
	}
'''
LOOP2 = '''	while (i + N <= size && found != 1)
		if ((found = smcConfigOk(buf + i)) != 1)
			i += N;
'''
CALL = '''	found = findSmcConfig(buf, size, &i);
	if (!found)
		goto notfound;
'''
NF = {
    'goto': ('\tif (!found)\n\t\tgoto notfound;\n', None),
    'ret': ('\tif (!found) {\n\t\tlog_printf(0, "******* ERROR: unable to find SMC config data!\\n");\n\t\treturn 2;\n\t}\n', True),
}
INIT = {'stmt': ('\ti = 0;\n\tfound = 0;\n', '\tuint32_t i, j;\n\tint found;\n'),
        'decl': ('', '\tuint32_t i = 0, j;\n\tint found = 0;\n'),
        'late': ('\tfound = 0;\n\ti = 0;\n', '\tuint32_t i, j;\n\tint found;\n')}


def CASES(base):
    t0 = bdhints.off(base, 'exp_200', 'exp_210', 'pin_i')
    i, j = bdrun.fnspan(t0, 'static int findSmcConfig(')
    t0 = t0[:i] + t0[j:]
    out = []
    for (lk, lp), nk, ik in itertools.product({'wh': LOOP, 'wh2': LOOP2}.items(), NF, INIT):
        ini, decl = INIT[ik]
        l1 = lp.replace('N', '0x200')
        l2 = ''.join('\t' + l for l in lp.replace('N', '0x210').splitlines(True))
        body = ini + l1 + '\tif (!found) {\n\t\ti = 0;\n' + l2 + '\t}\n' + NF[nk][0]
        t = bdrun.sub(t0, CALL, body)
        t = bdrun.sub(t, '\tuint32_t i, j;\n\tint found;\n\n\t/* size is an int', decl + '\n\t/* size is an int')
        if NF[nk][1]:
            t = bdrun.sub(t, '''	return 0;
notfound:
	log_printf(0, "******* ERROR: unable to find SMC config data!\\n");
	return 2;
}''', '\treturn 0;\n}')
        out.append(('%s %s %s' % (lk, nk, ik), t))
    return out


FOCUS = ['_extractSmcConfig']
