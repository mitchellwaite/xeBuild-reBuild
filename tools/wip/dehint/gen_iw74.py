# attempt 5: t's position against the _Bool partial form (m3), with the pin and without
import os
BASE = os.environ.get('IWB', 'build/iw/a5/m3.c')
IF = "		if (type != 0 && type != '0' && len < 0x4000)\n			partial = 1;\n"
OLD = "		partial = 0;\n" + IF + "		t = type - '1';\n"
T = "		t = type - '1';\n"
Z = "		partial = 0;\n"
PIN = '			__asm__("" :: "g"(t));\n'
FORMS = {
 'o': OLD,
 'tz': T + Z + IF,
 'zt': Z + T + IF,
}
IFS = {
 'i0': IF,
 'i1': "		if (type && type != '0' && len < 0x4000)\n			partial = 1;\n",
 'i2': "		if (len < 0x4000 && type != 0 && type != '0')\n			partial = 1;\n",
 'i3': "		if (type != 0 && type != '0')\n			if (len < 0x4000)\n				partial = 1;\n",
 'i4': "		if (type != 0)\n			if (type != '0' && len < 0x4000)\n				partial = 1;\n",
 'i5': "		if (type != 0 && len < 0x4000 && type != '0')\n			partial = 1;\n",
 'i6': "		if (type != '0' && type != 0 && len < 0x4000)\n			partial = 1;\n",
}
D = {
 'd0': [],
 'd1': [('	uint8_t t;\n	uint32_t pg;\n	uint8_t sp9, *s;\n	_Bool partial;\n', '	_Bool partial;\n	uint8_t t;\n	uint32_t pg;\n	uint8_t sp9, *s;\n')],
}
AXES = [
 [(k + i, [(OLD, v.replace(IF, w))]) for k, v in FORMS.items() for i, w in IFS.items()],
 [('', []), ('nopin', [(PIN, '')])],
 [(k, v) for k, v in D.items()],
]
FLAGS = []
