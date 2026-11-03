# attempt 5: fallback on m1 (imgAddFile natural but for one compare in the big copy): one dead test in imgAddFile to flip it
import os
BASE = os.environ.get('IWB', 'build/iw/a5/m1.c')
F = '	if (imgFits(off, len)) {\n		fsFiles'
AB = '		if ((%s & 0x3fff) > 0x3fff)\n			abort();\n'
AXES = [
 [('', []),
  ('L', [(F, '	if ((len & 0x3fff) > 0x3fff)\n		len++;\n' + F)]),
  ('Lo', [(F, '	if ((off & 0x3fff) > 0x3fff)\n		off++;\n' + F)]),
  ('Ll', [(F, '	if ((off & 0x3fff) > 0x3fff)\n		len++;\n' + F)]),
  ('E', [(F, '	uint32_t end = off + len;\n\n	if (end < off && (len & 0x3fff) > 0x3fff)\n		len++;\n' + F)]),
 ],
 [('', []),
  ('Al', [('		fsFiles[nFsFiles].block =', AB % 'len' + '		fsFiles[nFsFiles].block =')]),
  ('Ao', [('		fsFiles[nFsFiles].block =', AB % 'off' + '		fsFiles[nFsFiles].block =')]),
  ('Bl', [('		nFsFiles++;\n	} else {', '		if ((len & 0x3fff) > 0x3fff)\n			abort();\n		nFsFiles++;\n	} else {')]),
 ],
]
FLAGS = []
