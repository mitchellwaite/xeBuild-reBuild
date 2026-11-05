"""parseDump rj: free list top to bottom at ch2 is dce2's PHIs, then dest.43_98, _100, _135; n takes _100, one more pop before it would give it site 2's _135 (> the load's _127).
Things that change how many names ch2 pops: conversions and statements in copied loop headers, types of the counters."""
FOCUS = ['_parseDump']
BASE = 'build/ir/a3/rj.c'


def opt(lab, *e):
    return [('', []), (lab, list(e))]


AXES = [
    [('', []),
     ('iu', [('static int addRemapP(int block, int ablock, int cb, int dest, int numBlocks)\n{\n	int i;\n', 'static int addRemapP(int block, int ablock, int cb, int dest, int numBlocks)\n{\n	uint32_t i;\n')]),
     ],
    [('', []),
     ('su', [('	uint32_t n;\n	int i;\n	uint8_t *src;\n', '	uint32_t n;\n	uint32_t i;\n	uint8_t *src;\n')]),
     ('sc', [('		for (i = 0; i < xb.numBad; i++) {\n			if (xb.badRemap[i] == -5)', '		for (i = 0; (uint32_t)i < xb.numBad; i++) {\n			if (xb.badRemap[i] == -5)')]),
     ],
    [('', []),
     ('pu', [('		for (p = 0; p < ppb; p++) {', '		for (p = 0; (uint32_t)p < ppb; p++) {')]),
     ('pu2', [('	int blk, dst, p, b2;\n', '	int blk, dst, b2;\n	uint32_t p;\n')]),
     ('pl', [('		for (p = 0; p < ppb; p++) {', '		int lim = ppb;\n		for (p = 0; p < lim; p++) {')]),
     ],
    [('', []),
     ('nl', [('	for (n = 0; n < blocks; n++) {', '	for (n = 0; n < (uint32_t)blocks; n++) {')]),
     ('nl2', [('	for (n = 0; n < blocks; n++) {', '	uint32_t limit = blocks;\n\n	for (n = 0; n < limit; n++) {')]),
     ],
    [('', []),
     ('tb', [('	if (i < xb.numBad)\n		goto body;\n', '	if ((uint32_t)i < xb.numBad)\n		goto body;\n')]),
     ('tn', [('	if (i < xb.numBad)\n		goto body;\n	if (found)', '	if (xb.numBad > i)\n		goto body;\n	if (found)')]),
     ],
]
