# attempt 10: pin_hdr gone, forms of pageErased's two loops.  r192 = r267's copy in the threaded not-erased entry must reach REG_FREQ 32 (block >= 320):
# iw10a.py shows the flip needs no change to P(ECC).  So raise P(not erased): the per-iteration mismatch edge is PRED_LOOP_EXIT 9% / n_exits = 4.5%.
# A test whose fall-through edge goes straight to the loop header has no PRED_LOOP_EXIT (header_found), so index-in-the-test forms change it.
import os
PIN = '			__asm__("" :: "a"(xb.hdr));\n'
PE = '''	int i;

	for (i = 0; i < 512; i++)
		if (data[i] != 0xff)
			return 0;
	for (i = 0; i < 16; i++)
		if (spare[i] != 0xff)
			return 0;
	return 1;
'''
DATA = {
 '': '''	for (i = 0; i < 512; i++)
		if (data[i] != 0xff)
			return 0;
''',
 'd1': '''	for (i = 0; i < 512;)
		if (data[i++] != 0xff)
			return 0;
''',
 'd2': '''	i = 512;
	while (i--)
		if (*data++ != 0xff)
			return 0;
''',
 'd3': '''	for (i = 512; i > 0; i--)
		if (*data++ != 0xff)
			return 0;
''',
 'd4': '''	i = 0;
	do {
		if (data[i] != 0xff)
			return 0;
	} while (++i < 512);
''',
 'd5': '''	for (i = 0; i < 512; i++) {
		if (data[i] == 0xff)
			continue;
		return 0;
	}
''',
 'd6': '''	i = 0;
	while (i < 512)
		if (data[i++] != 0xff)
			return 0;
''',
}
SPARE = {
 '': '''	for (i = 0; i < 16; i++)
		if (spare[i] != 0xff)
			return 0;
''',
 's1': '''	for (i = 0; i < 16;)
		if (spare[i++] != 0xff)
			return 0;
''',
 's2': '''	i = 16;
	while (i--)
		if (*spare++ != 0xff)
			return 0;
''',
 's3': '''	for (i = 16; i > 0; i--)
		if (*spare++ != 0xff)
			return 0;
''',
 's4': '''	i = 0;
	do {
		if (spare[i] != 0xff)
			return 0;
	} while (++i < 16);
''',
 's5': '''	for (i = 0; i < 16; i++) {
		if (spare[i] == 0xff)
			continue;
		return 0;
	}
''',
 's6': '''	i = 0;
	while (i < 16)
		if (spare[i++] != 0xff)
			return 0;
''',
}
AXES = [
 [('nopin', [(PIN, '')])],
 [(d + ('+' if d or s else '') + s, [(PE, '	int i;\n\n' + DATA[d] + SPARE[s] + '	return 1;\n')]) for d in DATA for s in SPARE],
]
BASE = os.environ.get('IWB', 'src/image_write.c')
FLAGS = []
FOCUS = ['_finalizeImage']
