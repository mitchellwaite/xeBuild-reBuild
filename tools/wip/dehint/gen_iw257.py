# attempt 18: pin_t probe (not candidates: asm). How much does t's frequency need to gain? t 95, _268 96, r402 98 on src minus the pin (iw18freq.py). Moves the empty asm to places of known frequency.
# `IWB=build/iw/a18/nopt.c python tools/wip/dehint/iw16sweep.py tools/wip/dehint/gen_iw257.py -n 30 -t 1`
import os
BASE = os.environ.get('IWB', 'build/iw/a18/nopt.c')
T = "		t = type - '1';\n		if (t < 15) {\n"
PIN = '__asm__("" :: "g"(t));\n'
E = '	imgEnd = off + len;\n'
N = '	if (next != 0xf1f1) {\n\n'
F = '		for (i = 0; i < blocks; i++) {\n'
P = '			pg = start * 32;\n'
A = [('', []),
 ('exit', [(E, '	' + PIN + E)]),
 ('next', [(N, N + '		' + PIN)]),
 ('fsl', [(F, F + '			' + PIN)]),
 ('head', [("	#undef BLK", "	#undef BLK")]),
 ('page', [(P, '			' + PIN + P)]),
 ('afterT', [("		t = type - '1';\n", "		t = type - '1';\n		" + PIN)]),
 ('elsearm', [('			if (p) p /= 512;\n		}\n', '			if (p) p /= 512;\n		} else\n			' + PIN)]),
]
A = [a for a in A if a[0] != 'head']
AXES = [A]
FLAGS = []
