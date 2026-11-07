"""Attempt 23, exp_devgl: fuse's computation written as one expression or as the dev types guarding the glitch2mfg
read (so the setne can't be sunk past a dev-test PHI), against src's `fuse = g != 0; if (dev) fuse = 1;` (sink moves the
setne into the non-dev arm unless that arm is >= 75.06%).  Runs on src as of 604028f1 + attempt 23's isUpdateBl."""
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
DEV = 'xb.type == BUILD_DEVGL || xb.type == BUILD_DEVGL16'
F = {
    'none': OLD.replace('__builtin_expect(%s, 0)' % DEV, DEV),
    'or_g_dev': '\tfuse = 1;\n\tif (xb.type != BUILD_JTAG)\n\t\tfuse = xb.glitch2mfg != 0 || %s;\n' % DEV,
    'or_dev_g': '\tfuse = 1;\n\tif (xb.type != BUILD_JTAG)\n\t\tfuse = %s || xb.glitch2mfg != 0;\n' % DEV,
    'tern': '\tfuse = 1;\n\tif (xb.type != BUILD_JTAG)\n\t\tfuse = (%s) ? 1 : xb.glitch2mfg != 0;\n' % DEV,
    'ifelse': '\tfuse = 1;\n\tif (xb.type != BUILD_JTAG) {\n\t\tif (%s)\n\t\t\tfuse = 1;\n\t\telse\n\t\t\tfuse = xb.glitch2mfg != 0;\n\t}\n' % DEV,
    'ne_chain': '\tfuse = 1;\n\tif (xb.type != BUILD_JTAG && xb.type != BUILD_DEVGL && xb.type != BUILD_DEVGL16)\n\t\tfuse = xb.glitch2mfg != 0;\n',
    'ne_nest': '\tfuse = 1;\n\tif (xb.type != BUILD_JTAG) {\n\t\tif (xb.type != BUILD_DEVGL && xb.type != BUILD_DEVGL16)\n\t\t\tfuse = xb.glitch2mfg != 0;\n\t}\n',
    'g_first': '\tfuse = 1;\n\tif (xb.type != BUILD_JTAG) {\n\t\tint g = xb.glitch2mfg != 0;\n\n\t\tfuse = g;\n\t\tif (%s)\n\t\t\tfuse = 1;\n\t}\n' % DEV,
    'or_g_dev_noj': '\tfuse = xb.type == BUILD_JTAG || xb.glitch2mfg != 0 || %s;\n' % DEV,
    'bor': '\tfuse = 1;\n\tif (xb.type != BUILD_JTAG)\n\t\tfuse = (xb.glitch2mfg != 0) | (%s);\n' % DEV,
}
FOCUS = ['_buildFlash']


def CASES(base):
    return [(k, lambda b, v=v: bdrun.sub(b, OLD, v, 1)) for k, v in F.items()]
