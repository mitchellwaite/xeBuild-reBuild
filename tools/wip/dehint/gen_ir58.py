"""parseDump rj: one entry fewer above _100 on the free list is enough.  dce2's dead PHIs include p_117 = PHI <0, 0> at the zero-block's join: set p before that test."""
FOCUS = ['_parseDump']
BASE = 'build/ir/a3/rj.c'
Z = '		if (blk == 0) {\n			if (!notZeropair()) {'
FOR = '		for (p = 0; p < ppb; p++) {'
TOP = '		blk = n;\n'
AXES = [
    [('', []),
     ('z', [(Z, '		p = 0;\n' + Z), (FOR, '		for (; p < ppb; p++) {')]),
     ('t', [(TOP, TOP + '		p = 0;\n'), (FOR, '		for (; p < ppb; p++) {')]),
     ('w', [(FOR, '		p = 0;\n		while (p < ppb) {'), ('raw + (blk * ppb + p) * 528 + 512, 16);\n', 'raw + (blk * ppb + p) * 528 + 512, 16);\n			p++;\n')]),
     ('d', [(FOR, '		for (int q = 0; q < ppb; q++) {'), ('			memcpy(xb.dump + (dst * ppb + p) * 512, raw + (blk * ppb + p) * 528, 512);\n			memcpy(xb.dumpSpare + (dst * ppb + p) * 16, raw + (blk * ppb + p) * 528 + 512, 16);\n',
                                                                 '			memcpy(xb.dump + (dst * ppb + q) * 512, raw + (blk * ppb + q) * 528, 512);\n			memcpy(xb.dumpSpare + (dst * ppb + q) * 16, raw + (blk * ppb + q) * 528 + 512, 16);\n'), ('	int blk, dst, p, b2;\n', '	int blk, dst, b2;\n')]),
     ],
]
