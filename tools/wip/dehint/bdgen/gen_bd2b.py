"""buildFlash's fuse: the expect keeps setne above the test (tree-sink's 75% threshold)"""
Q = '''	fuse = 1;
	if (xb.type != BUILD_JTAG) {
		fuse = xb.glitch2mfg != 0;
		if (__builtin_expect(xb.type == BUILD_DEVGL || xb.type == BUILD_DEVGL16, 0))
			fuse = 1;
	}
'''
FOCUS = ['_buildFlash']


def v(s):
    return [(Q, s)]


D = 'xb.type == BUILD_DEVGL || xb.type == BUILD_DEVGL16'
AXES = [[
    ('goto', v('''	fuse = 1;
	if (xb.type != BUILD_JTAG) {
		fuse = xb.glitch2mfg != 0;
		if (%s)
			goto on;
		goto done;
on:
		fuse = 1;
done:
		;
	}
''' % D)),
    ('goto2', v('''	if (xb.type == BUILD_JTAG) {
on:
		fuse = 1;
	} else {
		fuse = xb.glitch2mfg != 0;
		if (%s)
			goto on;
	}
''' % D)),
    ('goto3', v('''	if (xb.type != BUILD_JTAG) {
		fuse = xb.glitch2mfg != 0;
		if (%s)
			goto on;
	} else {
on:
		fuse = 1;
	}
''' % D)),
    ('goto4', v('''	fuse = 1;
	if (xb.type == BUILD_JTAG)
		goto fused;
	fuse = xb.glitch2mfg != 0;
	if (%s)
		fuse = 1;
fused:
''' % D)),
    ('swap', v('''	fuse = xb.glitch2mfg != 0;
	if (xb.type == BUILD_JTAG || %s)
		fuse = 1;
''' % D)),
    ('else', v('''	if (xb.type != BUILD_JTAG) {
		fuse = xb.glitch2mfg != 0;
		if (%s)
			fuse = 1;
	} else
		fuse = 1;
''' % D)),
    ('char', v('''	fuse = 1;
	if (xb.type != BUILD_JTAG) {
		fuse = !!xb.glitch2mfg;
		if (%s)
			fuse = 1;
	}
''' % D)),
    ('ifelse', v('''	fuse = 1;
	if (xb.type != BUILD_JTAG) {
		if (xb.glitch2mfg)
			fuse = 1;
		else
			fuse = 0;
		if (%s)
			fuse = 1;
	}
''' % D)),
]]
