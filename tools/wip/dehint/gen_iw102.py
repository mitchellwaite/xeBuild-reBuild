# attempt 6: r0 (IWB=): `off + len` as a local in imgAdd's head and memset, imgEnd; x and first forms
import os
HEAD = '	if (xb.rawSize < off || xb.rawSize < off + len) {\n		return -1;\n	}\n	x = off & 0x3fff;\n'
MS = '	if (pad == 1) if (tail)\n		memset(xb.hdr + off + len, 0, ((off + len + 0x3fff) & ~0x3fff) - (off + len));\n'
IE = '	imgEnd = off + len;\n	return 0;\n}\n\n/* an `if`'
MC = '	memcpy(xb.hdr + off, src, len);\n'
AXES = [
 [('', []),
  ('h1', [(HEAD, '	end = off + len;\n	if (xb.rawSize < off || xb.rawSize < end) {\n		return -1;\n	}\n	x = off & 0x3fff;\n')]),
  ('h2', [(HEAD, HEAD.replace('off + len', 'off + len')), (MC, '	end = off + len;\n' + MC)]),
  ('h3', [(HEAD, '	x = off & 0x3fff;\n	if (xb.rawSize < off || xb.rawSize < off + len) {\n		return -1;\n	}\n')]),
 ],
 [('', []),
  ('m1', [(MS, '	if (pad == 1) if (tail)\n		memset(xb.hdr + end, 0, ((end + 0x3fff) & ~0x3fff) - end);\n')]),
  ('m2', [(MS, '	if (pad == 1) if (tail) {\n		uint32_t e = off + len;\n		memset(xb.hdr + e, 0, ((e + 0x3fff) & ~0x3fff) - e);\n	}\n')]),
  ('m3', [(MS, '	if (pad == 1) if (tail) {\n		uint32_t e = (off + len + 0x3fff) & ~0x3fff;\n		memset(xb.hdr + off + len, 0, e - (off + len));\n	}\n')]),
  ('m4', [(MS, '	if (pad == 1) if (tail) {\n		uint8_t *e = xb.hdr + off + len;\n		memset(e, 0, ((off + len + 0x3fff) & ~0x3fff) - (off + len));\n	}\n')]),
 ],
 [('', []),
  ('e1', [(IE, '	imgEnd = end;\n	return 0;\n}\n\n/* an `if`')])],
]
BASE = os.environ.get('IWB', 'build/iw/a6/r0.c')
FLAGS = []
