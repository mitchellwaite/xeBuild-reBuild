"""Attempt 34: pin_d by the smc fallback's share of case 27's flow (gen_bd462's two_pr fixes the join's registers but
moves bbro: the extract block's edge into the if (r) test drops 355 -> 320, under the loadBinFile block's 322).  Window
from the two end points: q (the share of case 27 reaching the smcConfig test) in about (0.07, 0.47); src 0.04, two_pr 0.5.
So the `*pr` re-test only on the first load's failure flow (q about 0.145), in several spellings.  pin_d off."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bdhints, bdrun

FOCUS = ['_loadBlFiles']
F = '&xb.files[xb.nFlashFiles]'
OLD = '''		if (loadBaseFile(e->name, &xb.files[xb.nFlashFiles]) &&
		    loadBaseFile("config.bin", &xb.files[xb.nFlashFiles]) &&
		    (*pr = loadBaseFile("config_raw.bin", &xb.files[xb.nFlashFiles]))) {
			if (!xb.smcConfig.data)
				break;
			log_printf(1, "reading %s%s failed, using %s from nand dump\\n", xb.baseDir, e->name, e->name);
			if (xb.files[xb.nFlashFiles].data)
				free(xb.files[xb.nFlashFiles].data);
			xb.files[xb.nFlashFiles].data = xb.smcConfig.data;
			xb.smcConfig.data = NULL;
			xb.files[xb.nFlashFiles].size = xb.smcConfig.size;
			xb.smcConfig.size = 0;
			*pr = 0;
		}
'''
BODY = '''if (!xb.smcConfig.data)
	break;
log_printf(1, "reading %s%s failed, using %s from nand dump\\n", xb.baseDir, e->name, e->name);
if (xb.files[xb.nFlashFiles].data)
	free(xb.files[xb.nFlashFiles].data);
xb.files[xb.nFlashFiles].data = xb.smcConfig.data;
xb.smcConfig.data = NULL;
xb.files[xb.nFlashFiles].size = xb.smcConfig.size;
xb.smcConfig.size = 0;
*pr = 0;'''


def ind(s, n):
    return ''.join('\t' * n + l + '\n' for l in s.split('\n'))


L1 = 'loadBaseFile(e->name, %s)' % F
L2 = 'loadBaseFile("config.bin", %s)' % F
L3 = 'loadBaseFile("config_raw.bin", %s)' % F
FORMS = {
    'c_nested': '\t\tif (%s) {\n\t\t\tif (%s)\n\t\t\t\t*pr = %s;\n\t\t\tif (*pr) {\n%s\t\t\t}\n\t\t}\n' % (L1, L2, L3, ind(BODY, 4)),
    'c_else0': '\t\tif (%s) {\n\t\t\tif (%s)\n\t\t\t\t*pr = %s;\n\t\t\telse\n\t\t\t\t*pr = 0;\n\t\t\tif (*pr) {\n%s\t\t\t}\n\t\t}\n' % (L1, L2, L3, ind(BODY, 4)),
    'c_seq': '\t\tif (%s) {\n\t\t\t*pr = %s;\n\t\t\tif (*pr)\n\t\t\t\t*pr = %s;\n\t\t\tif (*pr) {\n%s\t\t\t}\n\t\t}\n' % (L1, L2, L3, ind(BODY, 4)),
    'c_and': '\t\tif (%s) {\n\t\t\tif (%s && (*pr = %s)) {\n%s\t\t\t}\n\t\t}\n' % (L1, L2, L3, ind(BODY, 4)),
    'c2_nested': '\t\tif (%s && %s) {\n\t\t\t*pr = %s;\n\t\t\tif (*pr) {\n%s\t\t\t}\n\t\t}\n' % (L1, L2, L3, ind(BODY, 4)),
    'two_pr': '\t\tif (%s && %s)\n\t\t\t*pr = %s;\n\t\tif (*pr) {\n%s\t\t}\n' % (L1, L2, L3, ind(BODY, 3)),
}


def PRE(b):
    return bdhints.off(b, 'pin_d')


def CASES(base):
    return [(k, (lambda b, v=v: bdrun.sub(b, OLD, v))) for k, v in FORMS.items()]
