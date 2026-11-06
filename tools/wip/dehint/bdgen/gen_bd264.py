"""Attempt 15, exp_devgl: the dev-type override as its own statement after the JTAG one, not inside it.  Then
`fuse = xb.glitch2mfg != 0` reaches its PHI on a non-critical edge (its block's only successor), so sink has nowhere
to move it before vrp1 threads the JTAG path past the dev test.  Same behaviour: JTAG isn't a dev type.  Axes: how the
first part is written.  Runs on src/build.c after the lab_badsize landing."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import bdrun

OLD = '''	fuse = 1;
	if (xb.type != BUILD_JTAG) {
		fuse = xb.glitch2mfg != 0;
		if (__builtin_expect(xb.type == BUILD_DEVGL || xb.type == BUILD_DEVGL16, 0))
			fuse = 1;
	}
'''
DEV = '''	if (xb.type == BUILD_DEVGL || xb.type == BUILD_DEVGL16)
		fuse = 1;
'''
FIRST = {
    'if': '''	fuse = 1;
	if (xb.type != BUILD_JTAG)
		fuse = xb.glitch2mfg != 0;
''',
    'ifelse': '''	if (xb.type == BUILD_JTAG)
		fuse = 1;
	else
		fuse = xb.glitch2mfg != 0;
''',
    'tern': '''	fuse = xb.type == BUILD_JTAG ? 1 : xb.glitch2mfg != 0;
''',
    'or': '''	fuse = xb.type == BUILD_JTAG || xb.glitch2mfg;
''',
    'blk': '''	fuse = 1;
	if (xb.type != BUILD_JTAG) {
		fuse = xb.glitch2mfg != 0;
	}
''',
}


def CASES(base):
    out = []
    for k, f in FIRST.items():
        out.append((k, lambda b, f=f: bdrun.sub(b, OLD, f + DEV, 1)))
        out.append((k + ' dev1st', lambda b, f=f: bdrun.sub(b, OLD, DEV.replace('fuse = 1;', 'fuse = 1;') + f, 1)))
    return out


FOCUS = ['_buildFlash']
