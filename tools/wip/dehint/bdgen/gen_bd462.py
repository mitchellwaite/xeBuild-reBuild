"""Attempt 34: pin_d by the fallback's flow (gen_bd460's theory: n must outweigh the base in ALLOCNO_FREQ, so more flow
through the fallbacks' reloads of n, or less into the d block).  The third load and the smc take-over joined through a
`*pr` test, the chain as two loads and a separate third, the smc fallback's skip as a goto past the extract.  pin_d off."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bdhints, bdrun

FOCUS = ['_loadBlFiles']
F = '&xb.files[xb.nFlashFiles]'
HEAD = '''		if (loadBaseFile(e->name, &xb.files[xb.nFlashFiles]) &&
		    loadBaseFile("config.bin", &xb.files[xb.nFlashFiles]) &&
		    (*pr = loadBaseFile("config_raw.bin", &xb.files[xb.nFlashFiles]))) {
			if (!xb.smcConfig.data)
				break;
'''
HEADS = {
    'two_pr': ('\t\tif (loadBaseFile(e->name, %s) &&\n\t\t    loadBaseFile("config.bin", %s))\n'
               '\t\t\t*pr = loadBaseFile("config_raw.bin", %s);\n\t\tif (*pr) {\n\t\t\tif (!xb.smcConfig.data)\n\t\t\t\tbreak;\n') % (F, F, F),
    'two_else0': ('\t\tif (loadBaseFile(e->name, %s) &&\n\t\t    loadBaseFile("config.bin", %s))\n'
                  '\t\t\t*pr = loadBaseFile("config_raw.bin", %s);\n\t\telse\n\t\t\t*pr = 0;\n\t\tif (*pr) {\n\t\t\tif (!xb.smcConfig.data)\n\t\t\t\tbreak;\n') % (F, F, F),
    'and_smc': ('\t\tif (loadBaseFile(e->name, %s) &&\n\t\t    loadBaseFile("config.bin", %s) &&\n'
                '\t\t    (*pr = loadBaseFile("config_raw.bin", %s))) {\n\t\t\tif (!xb.smcConfig.data)\n\t\t\t\treturn;\n') % (F, F, F),
    'r_local': ('\t\tif (loadBaseFile(e->name, %s) &&\n\t\t    loadBaseFile("config.bin", %s) &&\n'
                '\t\t    loadBaseFile("config_raw.bin", %s)) {\n\t\t\t*pr = -1;\n\t\t\tif (!xb.smcConfig.data)\n\t\t\t\tbreak;\n') % (F, F, F),
}


def PRE(b):
    return bdhints.off(b, 'pin_d')


def CASES(base):
    return [(k, (lambda b, h=h: bdrun.sub(b, HEAD, h))) for k, h in HEADS.items()] + [('src', lambda b: b)]
