# attempt 13: src without imgWriteHdr (drafts/image_write_nohdr.c): each trick on/off, with or without the bitfield. Any single trick gone with everything right is a reduction.
import os
BASE = os.environ.get('IWB', 'tools/wip/dehint/drafts/image_write_nohdr.c')
DEF = 'struct spare {\n'
S = 's[12] = (s[12] & 0xc0) | (type & 0x3f);'
ATTR = '__attribute__((optimize("no-tree-scev-cprop"))) void writeFsTable'
DEAD = '''	if ((off & 0x3fff) > 0x3fff)
		off += 0x4000;
'''
PIN = '''			__asm__("" :: "g"(t));
'''
LN = '''		else {
			/* imgAddFile's clone: keeps DOM2's threading from zeroing the npages guard edge */
			lnp2: __attribute__((hot));
		}
'''
PN = '''		if ((off & 0x3fff) > 0x3fff)'''
AXES = [
 [('', []), ('bf', [(DEF, 'struct spt { uint8_t b[12]; uint8_t type:6, ecc3:2; };\n' + DEF), (S, '((struct spt *)s)->type = type;')])],
 [('', []), ('noattr', [(ATTR, 'void writeFsTable')])],
 [('', []), ('nodead', [(DEAD, '')])],
 [('', []), ('nopin', [(PIN, '')])],
 [('', []), ('nolnp', [(LN, '')])],
 [('', []),
  ('st', [('	fsTable[blk - xb.fsStart] = SWAP16_IMAGE_WRITE(0x1ffd);\n', '	fsTable[-xb.fsStart + blk] = SWAP16_IMAGE_WRITE(0x1ffd);\n')]),
  ('tl', [('	setBeU16(blk, (uint8_t *)&xb.fsBlock);\n', '	setBeU16(off >> 14, (uint8_t *)&xb.fsBlock);\n')]),
  ('st+tl', [('	fsTable[blk - xb.fsStart] = SWAP16_IMAGE_WRITE(0x1ffd);\n', '	fsTable[-xb.fsStart + blk] = SWAP16_IMAGE_WRITE(0x1ffd);\n'), ('	setBeU16(blk, (uint8_t *)&xb.fsBlock);\n', '	setBeU16(off >> 14, (uint8_t *)&xb.fsBlock);\n')]),
 ],
]
FLAGS = []
