# attempt 5: partial computed so the len test stays ahead of t (lim's hoist order), x type, on m1
import os
BASE = os.environ.get('IWB', 'build/iw/a5/m1.c')
DECL = '	int partial;\n'
P = "		partial = type != 0 && type != '0' && len < 0x4000;\n"
FORMS = {
 'p0': P,
 'pa': "		partial = 0;\n		if (type != 0 && type != '0' && len < 0x4000)\n			partial = 1;\n",
 'and1': "		partial = (type != 0) & (type != '0') & (len < 0x4000);\n",
 'and2': "		partial = type != 0 && type != '0';\n		partial &= len < 0x4000;\n",
 'and3': "		partial = type != 0 && type != '0';\n		partial = partial && len < 0x4000;\n",
 'and4': "		partial = type != 0 && type != '0';\n		if (partial)\n			partial = len < 0x4000;\n",
 'and5': "		partial = type != 0 && type != '0';\n		if (len >= 0x4000)\n			partial = 0;\n",
 'and6': "		partial = len < 0x4000;\n		if (type == 0 || type == '0')\n			partial = 0;\n",
 'and7': "		partial = type != 0;\n		partial &= type != '0';\n		partial &= len < 0x4000;\n",
 'and8': "		partial = type != 0 && type != '0';\n		partial = partial & (len < 0x4000);\n",
 'and9': "		partial = 0;\n		if (type != 0 && type != '0')\n			partial = len < 0x4000;\n",
 'and10': "		if (type != 0 && type != '0')\n			partial = len < 0x4000;\n		else\n			partial = 0;\n",
 'and11': "		partial = type != 0 && type != '0' ? len < 0x4000 : 0;\n",
 'and12': "		if (type != 0 && type != '0' && len < 0x4000)\n			partial = 1;\n		else\n			partial = 0;\n",
}
AXES = [
 [(k, [(DECL, '	%s partial;\n' % k)] if k != 'int' else []) for k in ('int', 'uint8_t', '_Bool', 'uint32_t', 'short')],
 [(k, [(P, v)]) for k, v in FORMS.items()],
]
FLAGS = []
