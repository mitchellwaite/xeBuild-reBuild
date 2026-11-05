"""exp_devgl (attempt 8): fuse's type and the way glitch2mfg becomes a flag, with no expect.  Tree-sink moves the setne into
the non-dev path unless that path has >= 75% of the frequency; a different type changes what the statement is."""
import itertools, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
import bdhints

DECL = '	int fuse, blocks, r, cf, cg, region, i;\n'
BODY = '''	fuse = 1;
	if (xb.type != BUILD_JTAG) {
		fuse = xb.glitch2mfg != 0;
		if (xb.type == BUILD_DEVGL || xb.type == BUILD_DEVGL16)
			fuse = 1;
	}
'''
TYPES = ['int', 'unsigned', 'BOOL', '_Bool', 'uint8_t', 'char', 'uint32_t']
SETS = {
    'ne': 'fuse = xb.glitch2mfg != 0;',
    'nn': 'fuse = !!xb.glitch2mfg;',
    'tern': 'fuse = xb.glitch2mfg ? 1 : 0;',
    'raw': 'fuse = xb.glitch2mfg;',
}
TAILS = {
    'if': '		if (xb.type == BUILD_DEVGL || xb.type == BUILD_DEVGL16)\n			fuse = 1;\n',
    'ifne': '		if (xb.type == BUILD_DEVGL || xb.type == BUILD_DEVGL16)\n			fuse = TRUE;\n',
}


def CASES(base):
    t0 = bdhints.off(base, 'exp_devgl')
    if BODY not in t0:
        raise ValueError('body')
    out = []
    for ty, s in itertools.product(TYPES, SETS):
        if s == 'raw' and ty not in ('_Bool', 'BOOL', 'int'):
            continue
        body = BODY.replace('fuse = xb.glitch2mfg != 0;', SETS[s])
        t = t0.replace(BODY, body)
        if ty == 'int':
            pass
        else:
            t = t.replace(DECL, '	int blocks, r, cf, cg, region, i;\n	%s fuse;\n' % ty)
        out.append(('%s %s' % (ty, s), t))
    return out


FOCUS = ['_buildFlash']
