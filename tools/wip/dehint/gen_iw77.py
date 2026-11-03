# attempt 5: _Bool partial: the len test's SSA name must be below t's (PRE orders its preheader insertions by value id = SSA version): t forms x partial forms
import os
BASE = os.environ.get('IWB', 'build/iw/a5/m1.c')
DECL = '	int partial;\n'
P = "		partial = type != 0 && type != '0' && len < 0x4000;\n"
T = "		t = type - '1';\n"
TESTS = "type != 0 && type != '0' && len < 0x4000"
PF = {
 'pa': "		partial = 0;\n		if (%s)\n			partial = 1;\n" % TESTS,
 'pb': "		if (%s)\n			partial = 1;\n		else\n			partial = 0;\n" % TESTS,
 'pc': "		partial = 0;\n		if (type != 0 && type != '0')\n			if (len < 0x4000)\n				partial = 1;\n",
 'pd': "		partial = 1;\n		if (type == 0 || type == '0' || len >= 0x4000)\n			partial = 0;\n",
 'pe': "		partial = 0;\n		small = len < 0x4000;\n		if (type != 0 && type != '0' && small)\n			partial = 1;\n",
 'pf': "		small = len < 0x4000;\n		partial = 0;\n		if (small && type != 0 && type != '0')\n			partial = 1;\n",
 'pg': "		partial = 0;\n		if (%s) {\n			partial = 1;\n		}\n" % TESTS,
 'ph': "		partial = type == 0 || type == '0' || len >= 0x4000 ? 0 : 1;\n",
 'pi': "		partial = !(type == 0 || type == '0' || len >= 0x4000);\n",
 'pj': "		partial = %s ? 1 : 0;\n" % TESTS,
}
TF = {
 't0': T,
 't1': "		t = type - 0x31;\n",
 't2': "		t = (uint8_t)(type - '1');\n",
 't3': "		t = type;\n		t -= '1';\n",
 't4': "		t = type + 207;\n",
}
DT = {
 'dt0': [],
 'dt1': [('	uint8_t t;\n', '	uint32_t t;\n')],
}
AXES = [
 [(k, [(DECL, '	%s partial;\n' % k)] if k != 'int' else []) for k in ('_Bool', 'uint8_t', 'int')],
 [(k, [(P, v)]) for k, v in PF.items()],
 [(k, [(T, v)]) for k, v in TF.items()],
 [('', [])],
 [('sm', [('	uint32_t i;\n\n	if (xb.rawSize < off', '	uint32_t i;\n	int small;\n\n	if (xb.rawSize < off')])],
]
FLAGS = []
