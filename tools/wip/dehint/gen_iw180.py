# attempt 11: pin_hdr with the public testers: pageErased and/or finalizeImage's test written with isErased() and spareUsed(), which exist in the file anyway.
# isErased's loop has no known trip count at profile_estimate, so its exits get other probabilities; a new source for the flows, no helper.
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
}

int blockErased'''
END = '}\n\nint blockErased'
H = 'xb.hdr + (b * 32 + p) * 512'
S = 'xb.spare + (b * 32 + p) * 16'
TEST = '			if (!pageErased(%s, %s))\n' % (H, S)
PF = [
 ('', []),
 ('p1', [(PE, '	return isErased(data, 512) && !spareUsed(spare);\n' + END)]),
 ('p2', [(PE, '	if (!isErased(data, 512))\n		return 0;\n	if (spareUsed(spare))\n		return 0;\n	return 1;\n' + END)]),
 ('p3', [(PE, '	if (isErased(data, 512) && !spareUsed(spare))\n		return 1;\n	return 0;\n' + END)]),
 ('p4', [(PE, '	return isErased(data, 512) && isErased(spare, 16);\n' + END)]),
 ('p5', [(PE, '	if (!isErased(data, 512))\n		return 0;\n	return isErased(spare, 16);\n' + END)]),
 ('p6', [(PE, '	if (isErased(data, 512) && isErased(spare, 16))\n		return 1;\n	return 0;\n' + END)]),
 ('p7', [(PE, '	int i;\n\n	for (i = 0; i < 512; i++)\n		if (data[i] != 0xff)\n			return 0;\n	return !spareUsed(spare);\n' + END)]),
 ('p8', [(PE, '	int i;\n\n	for (i = 0; i < 512; i++)\n		if (data[i] != 0xff)\n			return 0;\n	return isErased(spare, 16);\n' + END)]),
 ('p9', [(PE, '	if (!isErased(data, 512))\n		return 0;\n	for (int_i = 0; int_i < 16; int_i++)\n		if (spare[int_i] != 0xff)\n			return 0;\n	return 1;\n'.replace('int_i', 'i').replace('	if (!isErased', '	int i;\n\n	if (!isErased') + END)]),
]
TF = [
 ('', []),
 ('t1', [(TEST, '			if (!isErased(%s, 512) || spareUsed(%s))\n' % (H, S))]),
 ('t2', [(TEST, '			if (!isErased(%s, 512) || !isErased(%s, 16))\n' % (H, S))]),
 ('t3', [(TEST, '			if (spareUsed(%s) || !isErased(%s, 512))\n' % (S, H))]),
]
AXES = [[('nopin', [(PIN, '')])], PF, TF]
BASE = os.environ.get('IWB', 'src/image_write.c')
FLAGS = []
