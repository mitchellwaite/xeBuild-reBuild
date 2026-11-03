# attempt 4: near3 minus the a6 test and optionally c4: imgAddFile's forms (its own dead tests, lim, end, the fits test); writeFsTable already matches here
import os
BASE = os.environ.get('IWB', 'build/iw/a4/c4a6.c')
LEN = '	if (end < off && (len & 0x3fff) > 0x3fff)\n		len++;\n'
FIT = '	if (__builtin_expect(lim >= off + len, 1)) {\n'
AB = '		if ((len & 0x3fff) > 0x3fff)\n			abort();\n'
DECL = '	uint32_t lim = (xb.fsEnd - 1) * 0x4000;\n	uint32_t end = off + len;\n'
AXES = [
 [('', []), ('Dswap', [(DECL, '	uint32_t end = off + len;\n	uint32_t lim = (xb.fsEnd - 1) * 0x4000;\n')])],
 [('', []),
  ('L1', [(LEN, '	if ((len & 0x3fff) > 0x3fff)\n		len++;\n')]),
  ('L2', [(LEN, '	if ((end & 0x3fff) > 0x3fff)\n		len++;\n')]),
  ('L3', [(LEN, '	if (end < len && (len & 0x3fff) > 0x3fff)\n		len++;\n')]),
  ('L4', [(LEN, '	if ((len & 0x3fff) > 0x3fff && end < off)\n		len++;\n')]),
  ('L5', [(LEN, '	if (end < off)\n		len++;\n')]),
  ('L6', [(LEN, '	if (end < len)\n		len++;\n')]),
  ('L7', [(LEN, '	if ((off & 0x3fff) > 0x3fff)\n		len++;\n')]),
  ('L8', [(LEN, '	if ((off & 0x3fff) > 0x3fff && end < off)\n		len++;\n')]),
 ],
 [('', []),
  ('F1', [(FIT, '	if (__builtin_expect(lim >= end, 1)) {\n')]),
  ('F2', [(FIT, '	if (__builtin_expect(off + len <= lim, 1)) {\n')]),
  ('F3', [(FIT, '	if (__builtin_expect(end <= lim, 1)) {\n')]),
 ],
 [('', []),
  ('A1', [(AB, '		if ((end & 0x3fff) > 0x3fff)\n			abort();\n')]),
  ('A2', [(AB, '		if ((off & 0x3fff) > 0x3fff)\n			abort();\n')]),
  ('A3', [(AB, '		if (end < off && (len & 0x3fff) > 0x3fff)\n			abort();\n')]),
 ],
]
