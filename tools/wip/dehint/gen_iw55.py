# attempt 4: on near3 (one compare off): every subset of the remaining dead tests and opt, to see who moves the compare tuple
import os
BASE = os.environ.get('IWB', 'tools/wip/dehint/drafts/image_write_near3.c')
OPT = '__attribute__((optimize("no-tree-scev-cprop"))) void writeFsTable'
AXES = [
 [('', []), ('A2', [('		if (x > first + 0x4000)\n			blocks += 2;\n', '')])],
 [('', []), ('C4', [('		if ((len & 0x3fff) > 0x3fff)\n			blocks++;\n', '')])],
 [('', []), ('A5', [('			if (x > first + 0x4000)\n				blocks++;\n', '')])],
 [('', []), ('A6', [('		if (x + 0x4000 < first)\n			blocks++;\n', '')])],
 [('', []), ('LEN', [('	if (end < off && (len & 0x3fff) > 0x3fff)\n		len++;\n', '')]),
  ('LEN0', [('	if (end < off && (len & 0x3fff) > 0x3fff)\n		len++;\n', '	if ((len & 0x3fff) > 0x3fff)\n		len++;\n')])],
 [('', []), ('AB', [('		if ((len & 0x3fff) > 0x3fff)\n			abort();\n', '')])],
 [('', []), ('noopt', [(OPT, 'void writeFsTable')])],
]
