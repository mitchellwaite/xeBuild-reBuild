# attempt 11: on build/iw/a11/g1.c.  imgAddFile's slots want the fits arm hotter than the head (P about 60%): an early return on the error arm gives 61% (PRED_TREE_EARLY_RETURN), but through the if-shaped imgFits
# the threaded head edge stays 50/50 and bbro's better_edge_p then prefers the lower-frequency error arm (gen_iw182 e3, 85 lines, error block moved).  With the comparison spelled so that the 61% stays on the head edge, the fits arm should fall through.
import os
BASE = os.environ.get('IWB', 'build/iw/a11/g1.c')
HEAD = '	uint32_t off = imgSizeAligned();\n\n	if (imgFits(off, len)) {\n		fsFiles'
TAIL = '		nFsFiles++;\n	} else {\n		log_printf(0, "\\n******* ERROR: adding %s will exceed available flash space! Skipped!\\n\\n", name);\n	}\n'
ERR = '		log_printf(0, "\\n******* ERROR: adding %s will exceed available flash space! Skipped!\\n\\n", name);\n		return;\n	}\n	{\n		fsFiles'
def f(test, decl=''):
    return [(HEAD, '	uint32_t off = imgSizeAligned();\n' + decl + '\n	if (' + test + ') {\n' + ERR), (TAIL, '		nFsFiles++;\n	}\n')]
FITS = 'int imgFits(uint32_t off, uint32_t len)\n{\n	if ((xb.fsEnd - 1) * 0x4000 >= off + len)\n		return 1;\n	return 0;\n}\n'
AXES = [
 [('e0', f('!imgFits(off, len)')),
  ('e1', f('(xb.fsEnd - 1) * 0x4000 < off + len')),
  ('e2', f('off + len > (xb.fsEnd - 1) * 0x4000')),
  ('e3', f('!((xb.fsEnd - 1) * 0x4000 >= off + len)')),
  ('e4', f('end > lim', '	uint32_t end = off + len, lim = (xb.fsEnd - 1) * 0x4000;\n')),
  ('e5', f('lim < off + len', '	uint32_t lim = (xb.fsEnd - 1) * 0x4000;\n')),
  ('e6', f('off + len > xb.fsEnd * 0x4000 - 0x4000')),
 ],
]
FLAGS = []
