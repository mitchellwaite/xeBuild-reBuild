"""buildFlash (attempt 12): forms of the fuse computation with no expect.  The reference loads glitch2mfg and does setne on
every non-JTAG path, then cmovbe 1 for the dev types; without the expect tree-sink puts the setne on the non-dev path only.
Forms here write the dev types as the case that skips the glitch2mfg read, so RTL if-conversion could speculate it."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
import bdhints, bdrun

OLD = '''	fuse = 1;
	if (xb.type != BUILD_JTAG) {
		fuse = xb.glitch2mfg != 0;
		if (xb.type == BUILD_DEVGL || xb.type == BUILD_DEVGL16)
			fuse = 1;
	}
'''
FORMS = {
    'and3': '''	fuse = 1;
	if (xb.type != BUILD_JTAG && xb.type != BUILD_DEVGL && xb.type != BUILD_DEVGL16)
		fuse = xb.glitch2mfg != 0;
''',
    'nest': '''	fuse = 1;
	if (xb.type != BUILD_JTAG) {
		if (xb.type != BUILD_DEVGL && xb.type != BUILD_DEVGL16)
			fuse = xb.glitch2mfg != 0;
	}
''',
    'else': '''	if (xb.type == BUILD_JTAG || xb.type == BUILD_DEVGL || xb.type == BUILD_DEVGL16)
		fuse = 1;
	else
		fuse = xb.glitch2mfg != 0;
''',
    'tern': '''	fuse = xb.type == BUILD_JTAG || xb.type == BUILD_DEVGL || xb.type == BUILD_DEVGL16 ? 1 : xb.glitch2mfg != 0;
''',
    'or': '''	fuse = xb.type == BUILD_JTAG || xb.type == BUILD_DEVGL || xb.type == BUILD_DEVGL16 || xb.glitch2mfg;
''',
    'or2': '''	fuse = 1;
	if (xb.type != BUILD_JTAG)
		fuse = xb.type == BUILD_DEVGL || xb.type == BUILD_DEVGL16 || xb.glitch2mfg;
''',
    'sw': '''	switch (xb.type) {
	case BUILD_JTAG:
	case BUILD_DEVGL:
	case BUILD_DEVGL16:
		fuse = 1;
		break;
	default:
		fuse = xb.glitch2mfg != 0;
	}
''',
    'sw2': '''	fuse = 1;
	if (xb.type != BUILD_JTAG) {
		switch (xb.type) {
		case BUILD_DEVGL:
		case BUILD_DEVGL16:
			break;
		default:
			fuse = xb.glitch2mfg != 0;
		}
	}
''',
    'neg': '''	fuse = 1;
	if (xb.type != BUILD_JTAG) {
		fuse = xb.glitch2mfg != 0;
		if (!(xb.type != BUILD_DEVGL && xb.type != BUILD_DEVGL16))
			fuse = 1;
	}
''',
    'bor': '''	fuse = 1;
	if (xb.type != BUILD_JTAG)
		fuse = (xb.glitch2mfg != 0) | (xb.type == BUILD_DEVGL || xb.type == BUILD_DEVGL16);
''',
}


def CASES(base):
    t0 = bdhints.off(base, 'exp_devgl')
    return [(k, bdrun.sub(t0, OLD, f)) for k, f in FORMS.items()]


FOCUS = ['_buildFlash']
