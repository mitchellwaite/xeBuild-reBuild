# attempt 5: can a low SSA name be released before ifcombine with imgAddFile staying right (no len++)?  extra copies around partial, on m1
import os
BASE = os.environ.get('IWB', 'build/iw/a5/m1.c')
DECL = '	int partial;\n'
P = "		partial = type != 0 && type != '0' && len < 0x4000;\n"
T = "		t = type - '1';\n"
TESTS = "type != 0 && type != '0' && len < 0x4000"
NP = '		if (!partial)\n			npages = 32;\n'
FORMS = {
 'c1': "		small = %s;\n		partial = small;\n" % TESTS,
 'c2': "		partial = 0;\n		if (%s)\n			partial = 1;\n		small = partial;\n" % TESTS,
 'c3': "		small = 0;\n		if (%s)\n			small = 1;\n		partial = small;\n" % TESTS,
 'c4': "		small = len < 0x4000;\n		partial = type != 0 && type != '0' && small;\n",
 'c5': "		partial = (small = %s);\n" % TESTS,
 'c6': "		partial = type != 0 && type != '0';\n		partial = partial && len < 0x4000;\n",
 'c7': "		partial = type != 0 && type != '0';\n		if (partial)\n			partial = len < 0x4000;\n",
 'c8': "		small = type != 0 && type != '0';\n		partial = small && len < 0x4000;\n",
 'c9': "		partial = 0;\n		if (type != 0 && type != '0')\n			partial = len < 0x4000;\n",
 'c10': "		partial = 0;\n		small = type != 0 && type != '0';\n		if (small && len < 0x4000)\n			partial = 1;\n",
}
AXES = [
 [(a + b, [(DECL, '	%s partial;\n	%s small;\n' % (a, b))]) for a in ('int', '_Bool', 'uint8_t') for b in ('int', '_Bool', 'uint8_t')],
 [(k, [(P, v)]) for k, v in FORMS.items()],
 [('', []), ('us', [(NP, '		if (!small)\n			npages = 32;\n')])],
]
AXES[2] = [('', [])]
FLAGS = []
FOCUS = ['_imgAdd', '_imgAddFile', '_writeFsTable', '_imgAdd.constprop.1', '_imgAdd.constprop.2', '_imgAdd.constprop.4']
