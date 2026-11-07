"""Attempt 38: exp_devgl by attempt 34's lever (a re-tested result variable): the dev override only where fuse is
still 0 (`if (!fuse && dev) fuse = 1;` and spellings; the same behaviour, setting 1 over 1 is a no-op).  The re-test
uses the glitch2mfg flag in its own block, so sink can't move it below the dev test, and the `!fuse` edge adds flow
at profile_estimate that phiopt / ifcombine may fold away later.  Expect off.
Run: python tools/wip/dehint/bdrun.py tools/wip/dehint/bdgen/gen_bd503.py"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import bdhints, bdrun

OLD = '''		fuse = xb.glitch2mfg != 0;
		if (xb.type == BUILD_DEVGL || xb.type == BUILD_DEVGL16)
			fuse = 1;
'''
DEV = 'xb.type == BUILD_DEVGL || xb.type == BUILD_DEVGL16'
FORMS = {
    'src': OLD,
    'and': '\t\tfuse = xb.glitch2mfg != 0;\n\t\tif (!fuse && (%s))\n\t\t\tfuse = 1;\n' % DEV,
    'and_eq0': '\t\tfuse = xb.glitch2mfg != 0;\n\t\tif (fuse == 0 && (%s))\n\t\t\tfuse = 1;\n' % DEV,
    'nest': '\t\tfuse = xb.glitch2mfg != 0;\n\t\tif (!fuse) {\n\t\t\tif (%s)\n\t\t\t\tfuse = 1;\n\t\t}\n' % DEV,
    'assign': '\t\tfuse = xb.glitch2mfg != 0;\n\t\tif (!fuse)\n\t\t\tfuse = %s;\n' % DEV,
    'dev_and': '\t\tfuse = xb.glitch2mfg != 0;\n\t\tif ((%s) && !fuse)\n\t\t\tfuse = 1;\n' % DEV,
    'raw_nest': '\t\tfuse = xb.glitch2mfg;\n\t\tif (!fuse) {\n\t\t\tif (%s)\n\t\t\t\tfuse = 1;\n\t\t} else\n\t\t\tfuse = 1;\n' % DEV,
}


def CASES(base):
    return [(k, lambda b, v=v: bdrun.sub(bdhints.off(b, 'exp_devgl'), OLD, v, 1)) for k, v in FORMS.items()]


FOCUS = ['_buildFlash']
