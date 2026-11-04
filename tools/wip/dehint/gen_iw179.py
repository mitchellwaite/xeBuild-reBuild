# attempt 11: on drafts/image_write_near10.c.  blockEccOk stops sharing the byte helper with pageErased: it spells its own erased test,
# through the other public testers or its own loops.  pageErased, finalizeImage keep the helper.
import os
CALL = '''		if (pageErased(blk + i * 528, blk + i * 528 + 512))
			continue;
'''
DECL = '	int i, pages = bigBlock ? 256 : 32;\n\n	for (i = 0; i < pages; i++) {\n		if (pageErased(blk'
D2 = '	int i, j, pages = bigBlock ? 256 : 32;\n\n	for (i = 0; i < pages; i++) {\n		if (pageErased(blk'
PRE = '/* a raw block (data and spare interleaved) */\nint blockEccOk'
OLD = '''static int pageBlank(const uint8_t *data, const uint8_t *spare)
{
	int i;

	for (i = 0; i < 512; i++)
		if (data[i] != 0xff)
			return 0;
	for (i = 0; i < 16; i++)
		if (spare[i] != 0xff)
			return 0;
	return 1;
}

'''
LOOPS = '''		for (j = 0; j < 512; j++)
			if (blk[i * 528 + j] != 0xff)
				goto check;
		for (j = 0; j < 16; j++)
			if (blk[i * 528 + 512 + j] != 0xff)
				goto check;
		continue;
check:
'''
LOOPS2 = '''		{
			const uint8_t *data = blk + i * 528, *spare = data + 512;

			for (j = 0; j < 512; j++)
				if (data[j] != 0xff)
					goto check;
			for (j = 0; j < 16; j++)
				if (spare[j] != 0xff)
					goto check;
			continue;
		}
check:
'''
LOOPS3 = '''		{
			const uint8_t *data = blk + i * 528, *spare = data + 512;

			for (j = 0; j < 512; j++)
				if (data[j] != 0xff)
					break;
			if (j == 512) {
				for (j = 0; j < 16; j++)
					if (spare[j] != 0xff)
						break;
				if (j == 16)
					continue;
			}
		}
'''
F = [
 ('', []),
 ('ie', [(CALL, '		if (isErased(blk + i * 528, 512) && !spareUsed(blk + i * 528 + 512))\n			continue;\n')]),
 ('ie2', [(CALL, '		if (isErased(blk + i * 528, 512) && isErased(blk + i * 528 + 512, 16))\n			continue;\n')]),
 ('ie3', [(CALL, '		if (isErased(blk + i * 528, 528))\n			continue;\n')]),
 ('blank', [(CALL, CALL.replace('pageErased', 'pageBlank')), (PRE, OLD + PRE)]),
 ('l1', [(DECL, D2), (CALL, LOOPS)]),
 ('l2', [(DECL, D2), (CALL, LOOPS2)]),
 ('l3', [(DECL, D2), (CALL, LOOPS3)]),
]
AXES = [F]
BASE = os.environ.get('IWB', 'tools/wip/dehint/drafts/image_write_near10.c')
FLAGS = []
