# attempt 6: c2: wide forms of partial (each changes how many names the copies burn where type is constant)
import os
PART = "		partial = (len < 0x4000) & (type != 0) & (type != '0');\n"
F = [
 "partial = (type != 0) & (type != '0') && len < 0x4000;",
 "partial = (type != 0 && type != '0') & (len < 0x4000);",
 "partial = type != 0 && type != '0' ? len < 0x4000 : 0;",
 "partial = (type != 0) & (type != '0');\n		partial = partial && len < 0x4000;",
 "partial = type != 0 && type != '0';\n		partial &= len < 0x4000;",
 "partial = (type != 0) & (type != '0');\n		partial &= len < 0x4000;",
 "partial = type != 0 && type != '0';\n		if (len >= 0x4000)\n			partial = 0;",
 "partial = (type != 0) & (type != '0');\n		if (len >= 0x4000)\n			partial = 0;",
 "partial = len < 0x4000;\n		if (type == 0 || type == '0')\n			partial = 0;",
 "partial = len < 0x4000;\n		partial &= type != 0 && type != '0';",
 "partial = len < 0x4000;\n		partial &= (type != 0) & (type != '0');",
 "partial = len < 0x4000;\n		partial &= type != 0;\n		partial &= type != '0';",
 "partial = 0;\n		if (type != 0 && type != '0')\n			partial = len < 0x4000;",
 "partial = 0;\n		if ((type != 0) & (type != '0'))\n			partial = len < 0x4000;",
 "partial = 0;\n		if (len < 0x4000)\n			partial = type != 0 && type != '0';",
 "partial = 0;\n		if (len < 0x4000)\n			partial = (type != 0) & (type != '0');",
 "partial = 0;\n		if ((len < 0x4000) & (type != 0) & (type != '0'))\n			partial = 1;",
 "partial = (type != 0 && type != '0') && (len < 0x4000);",
 "partial = !!type & (type != '0') & (len < 0x4000);",
 "partial = (len < 0x4000) & (type != 0 && type != '0');",
 "partial = (len >> 14 == 0) & (type != 0) & (type != '0');",
 "partial = (len <= 0x3fff) & (type > 0) & (type != '0');",
 "partial = (len < 0x4000) & (type > 0) & (type != '0');",
 "partial = (len < 0x4000) & (type != '0') & (type != 0);",
 "partial = (type != '0') & (type != 0) & (len < 0x4000);",
 "partial = (type != '0') & (len < 0x4000) & (type != 0);",
]
AXES = [[('', [])] + [('f%d' % i, [(PART, '		%s\n' % f)]) for i, f in enumerate(F)]]
BASE = os.environ.get('IWB', 'build/iw/a6/c2.c')
FLAGS = []
