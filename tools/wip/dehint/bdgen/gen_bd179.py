"""exp_devgl: `xb.type == BUILD_DEVGL || xb.type == BUILD_DEVGL16` is written seven times in build.c, so a small helper is natural, and it's early inlined.  At buildFlash's test alone and everywhere,
with the fuse test's forms."""
import itertools, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
import bdhints

HEAD = '/* read baseDir/name into e */\n'
T = 'xb.type == BUILD_DEVGL || xb.type == BUILD_DEVGL16'
HELP = {
    'or': 'static int isDevGl(void)\n{\n	return ' + T + ';\n}\n\n',
    'if': 'static int isDevGl(void)\n{\n	if (' + T + ')\n		return 1;\n	return 0;\n}\n\n',
    'seq': 'static int isDevGl(void)\n{\n	if (xb.type == BUILD_DEVGL)\n		return 1;\n	if (xb.type == BUILD_DEVGL16)\n		return 1;\n	return 0;\n}\n\n',
    'type': 'static int isDevGl(int type)\n{\n	return type == BUILD_DEVGL || type == BUILD_DEVGL16;\n}\n\n',
}
Q = '		fuse = xb.glitch2mfg != 0;\n		if (' + T + ')\n			fuse = 1;\n'
F = {
    'if': '		fuse = xb.glitch2mfg != 0;\n		if (CALL)\n			fuse = 1;\n',
    'or': '		fuse = xb.glitch2mfg != 0 || CALL;\n',
    'or2': '		fuse = CALL || xb.glitch2mfg != 0;\n',
    'if2': '		fuse = 1;\n		if (!CALL)\n			fuse = xb.glitch2mfg != 0;\n',
    'tern': '		fuse = CALL ? 1 : xb.glitch2mfg != 0;\n',
}


def PRE(t):
    return bdhints.off(t, 'exp_devgl')


def CASES(base):
    out = []
    for h, f, w in itertools.product(HELP, F, ('one', 'all')):
        call = 'isDevGl(xb.type)' if h == 'type' else 'isDevGl()'

        def g(t, h=h, f=f, w=w, call=call):
            if Q not in t:
                raise ValueError('q')
            t = t.replace(Q, F[f].replace('CALL', call))
            i = t.index(HEAD)
            pre, t = t[:i] + HELP[h] + HEAD, t[i + len(HEAD):]
            if w == 'all':
                t = t.replace('(' + T + ')', '(' + call + ')').replace('xb.glitch2mfg || ' + T, 'xb.glitch2mfg || ' + call)
            return pre + t
        out.append(('%s %s %s' % (h, f, w), g))
    return out


FOCUS = ['_buildFlash']
