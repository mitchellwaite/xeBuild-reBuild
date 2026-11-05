"""parseDump rj: (uint32_t)p in the p loop's copied header gives one more pop and the right compare, but an unsigned test.  The same extra statement with the signed test: `long` or short types on ppb, p."""
FOCUS = ['_parseDump']
BASE = 'build/ir/a3/rj.c'
PPB = '	int ppb = xb.dumpBigBlock ? 256 : 32;\n'
AXES = [
    [('', []),
     ('lppb', [(PPB, '	long ppb = xb.dumpBigBlock ? 256 : 32;\n')]),
     ('sppb', [(PPB, '	short ppb = xb.dumpBigBlock ? 256 : 32;\n')]),
     ('uppb', [(PPB, '	uint16_t ppb = xb.dumpBigBlock ? 256 : 32;\n')]),
     ('uuppb', [(PPB, '	uint32_t ppb = xb.dumpBigBlock ? 256 : 32;\n')]),
     ],
    [('', []),
     ('lp', [('	int blk, dst, p, b2;\n', '	int blk, dst, b2;\n	long p;\n')]),
     ('cp', [('		for (p = 0; p < ppb; p++) {', '		for (p = 0; p < (long)ppb; p++) {')]),
     ('cp2', [('		for (p = 0; p < ppb; p++) {', '		for (p = 0; (long)p < ppb; p++) {')]),
     ('ci', [('		for (p = 0; p < ppb; p++) {', '		for (p = 0; p < (int)ppb; p++) {')]),
     ],
    [('', []),
     ('lb', [('	int blocks = xb.dumpPages / ppb;\n', '	long blocks = xb.dumpPages / ppb;\n')]),
     ],
]
