"""Attempt 32: exp_devgl by forms where the glitch2mfg test is the *else* arm of the dev test (so there is no def
above the dev test for tree-sink to move, and RTL if-conversion has to speculate it, as the reference's
setne-then-cmovbe does).  Attempt 15/16 swept the src order (def, then override) and its spellings; these put
the override first.  Also memset/fuse order.  Runs on src as of ccf9746b."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bdrun

FOCUS = ['_buildFlash']
OLD = '''	memset(salt, 0, sizeof(salt));
	fuse = 1;
	if (xb.type != BUILD_JTAG) {
		fuse = xb.glitch2mfg != 0;
		if (__builtin_expect(xb.type == BUILD_DEVGL || xb.type == BUILD_DEVGL16, 0))
			fuse = 1;
	}
'''
DEV = '(xb.type == BUILD_DEVGL || xb.type == BUILD_DEVGL16)'
NDEV = '(xb.type != BUILD_DEVGL && xb.type != BUILD_DEVGL16)'
G = 'xb.glitch2mfg != 0'

BODIES = {
    'f2': '''	if (xb.type == BUILD_JTAG)
		fuse = 1;
	else if DEV
		fuse = 1;
	else
		fuse = G;
''',
    'f2b': '''	if (xb.type == BUILD_JTAG || DEV)
		fuse = 1;
	else
		fuse = G;
''',
    'f3': '''	if (xb.type != BUILD_JTAG) {
		if DEV
			fuse = 1;
		else
			fuse = G;
	} else
		fuse = 1;
''',
    'f3b': '''	fuse = 1;
	if (xb.type != BUILD_JTAG) {
		if DEV
			fuse = 1;
		else
			fuse = G;
	}
''',
    'f4': '''	fuse = 1;
	if (xb.type != BUILD_JTAG) {
		if NDEV
			fuse = G;
	}
''',
    'f4b': '''	fuse = 1;
	if (xb.type != BUILD_JTAG && NDEV)
		fuse = G;
''',
    'f5': '''	fuse = 1;
	if (xb.type != BUILD_JTAG && !DEV)
		fuse = G;
''',
    'f6': '''	if (xb.type != BUILD_JTAG && !DEV)
		fuse = G;
	else
		fuse = 1;
''',
    'f7': '''	fuse = 1;
	if (xb.type != BUILD_JTAG && !xb.glitch2mfg && !DEV)
		fuse = 0;
''',
    'f8': '''	fuse = 1;
	if (xb.type != BUILD_JTAG && !DEV && !xb.glitch2mfg)
		fuse = 0;
''',
    'f9': '''	fuse = 1;
	if (xb.type != BUILD_JTAG) {
		if (!xb.glitch2mfg)
			fuse = 0;
		if DEV
			fuse = 1;
	}
''',
    'f10': '''	fuse = 1;
	if (xb.type != BUILD_JTAG) {
		if (!DEV)
			fuse = G;
	}
''',
    'f11': '''	fuse = 1;
	if (xb.type != BUILD_JTAG) {
		if (!xb.glitch2mfg && !DEV)
			fuse = 0;
	}
''',
    'f12': '''	fuse = 1;
	if (xb.type != BUILD_JTAG) {
		if (!xb.glitch2mfg) {
			if (!DEV)
				fuse = 0;
		}
	}
''',
}


def CASES(base):
    out = []
    for k, v in BODIES.items():
        b = v.replace('NDEV', NDEV).replace('if DEV', 'if ' + DEV).replace('!DEV', '!' + DEV).replace('|| DEV', '|| ' + DEV)
        b = b.replace('= G;', '= ' + G + ';')
        for ms in ('first', 'after'):
            body = '\tmemset(salt, 0, sizeof(salt));\n' + b if ms == 'first' else b + '\tmemset(salt, 0, sizeof(salt));\n'
            out.append((k + ' ' + ms, bdrun.sub(base, OLD, body, 1)))
    return out
