# attempt 4: imgAddFile without its expect: with no dead test first in the fits arm its first block holds a call (strcpy), so PRED_CALL fires on both arms and cancels to 50%
import os
BASE = os.environ.get('IWB', 'tools/wip/dehint/drafts/image_write_a4.c')
FIT = '	if (__builtin_expect(lim >= off + len, 1)) {\n'
AB = '		if ((end & 0x3fff) > 0x3fff)\n			abort();\n'
LEN = '	if (end < off && (len & 0x3fff) > 0x3fff)\n		len++;\n'
BLOCK = '		fsFiles[nFsFiles].block = SWAP16_IMAGE_WRITE((uint16_t)(off >> 14) - xb.fsStart);\n'
CPY = '		strcpy(fsFiles[nFsFiles].name, name);\n'
AXES = [
 [('xp', []), ('noxp', [(FIT, '	if (lim >= off + len) {\n')]), ('noxpn', [(FIT, '	if (off + len <= lim) {\n')])],
 [('', []), ('A0', [(AB, '')]), ('Al', [(AB, '		if ((len & 0x3fff) > 0x3fff)\n			abort();\n')]),
  ('Acpy', [(AB, ''), (CPY, CPY + '		if ((end & 0x3fff) > 0x3fff)\n			abort();\n')]),
  ('Ab', [(AB, ''), (BLOCK, CPY + BLOCK), (CPY + BLOCK, BLOCK), ])],
 [('', []), ('L1', [(LEN, '	if ((len & 0x3fff) > 0x3fff)\n		len++;\n')]), ('L0', [(LEN, '')])],
 [('', []), ('cpyfirst', [(CPY, ''), (BLOCK, CPY + BLOCK)])],
]
