# attempt 10: pin_hdr gone.  Probes with expect on pageErased's loops (iw10a.py, build/iw/a10/grid.py) show the (A) flip at P(ECC) unchanged, for a per-byte mismatch
# of 5-15% in the spare loop (pageErased and blockEccOk stay right) or 6-8% in the data loop.  PRED_LOOP_EXIT gives a fixed 4.5%, so make the last step a test:
# a test after the loop (flows join in a PHI, no threading before profile_estimate) takes its own probability.  Good: finalizeImage 57 and nothing else.
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
D0 = '''	for (i = 0; i < 512; i++)
		if (data[i] != 0xff)
			return 0;
'''
SL = '''	for (i = 0; i < 16; i++)
		if (spare[i] != 0xff)
			break;
'''
TAILS = {
 '': '''	for (i = 0; i < 16; i++)
		if (spare[i] != 0xff)
			return 0;
	return 1;
''',
 'u1': '	if (!spareUsed(spare))\n		return 1;\n	return 0;\n',
 'u2': '	if (spareUsed(spare))\n		return 0;\n	return 1;\n',
 'u3': '	return !spareUsed(spare);\n',
 'u4': '	return spareUsed(spare) ? 0 : 1;\n',
 'u5': '	return spareUsed(spare) == 0;\n',
 'u6': '	if (spareUsed(spare) == 0)\n		return 1;\n	return 0;\n',
 'u7': '	if (spareUsed(spare) != 1)\n		return 1;\n	return 0;\n',
 'u8': '	if (spareUsed(spare) == 1)\n		return 0;\n	return 1;\n',
 'b1': SL + '	if (i == 16)\n		return 1;\n	return 0;\n',
 'b2': SL + '	if (i < 16)\n		return 0;\n	return 1;\n',
 'b3': SL + '	return i == 16;\n',
 'b4': SL + '	return i >= 16;\n',
 'b5': SL + '	if (i >= 16)\n		return 1;\n	return 0;\n',
 'b6': SL + '	if (i != 16)\n		return 0;\n	return 1;\n',
 'b7': SL + '	return i < 16 ? 0 : 1;\n',
}
DATA = {
 '': D0,
 'D1': '''	for (i = 0; i < 512; i++)
		if (data[i] != 0xff)
			break;
	if (i < 512)
		return 0;
''',
 'D2': '''	for (i = 0; i < 512; i++)
		if (data[i] != 0xff)
			break;
	if (i != 512)
		return 0;
''',
}
AXES = [
 [('nopin', [(PIN, '')])],
 [(d, [(D0, DATA[d])]) for d in DATA],
 [(s, [('	for (i = 0; i < 16; i++)\n		if (spare[i] != 0xff)\n			return 0;\n	return 1;\n}\n\nint blockErased', TAILS[s] + '}\n\nint blockErased')]) for s in TAILS],
]
BASE = os.environ.get('IWB', 'src/image_write.c')
FLAGS = []
