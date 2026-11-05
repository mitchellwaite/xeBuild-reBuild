"""parseDump rj: spellings that shouldn't change code but shift SSA names and the free list, looking for n's name above site 2's load."""
FOCUS = ['_parseDump']
BASE = 'build/ir/a3/rj.c'


def opt(lab, *e):
    return [('', []), (lab, list(e))]


COPY = '''			memcpy(xb.dump + (dst * ppb + p) * 512, raw + (blk * ppb + p) * 528, 512);
			memcpy(xb.dumpSpare + (dst * ppb + p) * 16, raw + (blk * ppb + p) * 528 + 512, 16);
'''
AXES = [
    opt('ty', ('	int valid = dest', '	uint32_t valid = dest')),
    opt('ok2', ('			if (!addRemapP(blk, blk, blk, -1, blocks))\n				return 0;\n', '			{\n				int ok = addRemapP(blk, blk, blk, -1, blocks);\n\n				if (!ok)\n					return 0;\n			}\n')),
    opt('ok1', ('			if (!addRemapP(b2, blk, 0, dst, blocks))\n				return 0;\n', '			{\n				int ok = addRemapP(b2, blk, 0, dst, blocks);\n\n				if (!ok)\n					return 0;\n			}\n')),
    opt('n3', ('		if (dst != blk && !addRemapP(dst, dst, 0, blk, blocks))\n			return 0;\n', '		if (dst != blk) {\n			if (!addRemapP(dst, dst, 0, blk, blocks))\n				return 0;\n		}\n')),
    opt('cnt', ('			goto next;\n		}\n		if (dst == -3)', '			continue;\n		}\n		if (dst == -3)'), ('next:\n		;\n', '')),
    opt('z', ('		if (blk == 0) {\n', '		if (!blk) {\n')),
    opt('sr', ('		src = raw + blk * 528 * ppb;\n', '		src = raw + n * 528 * ppb;\n')),
    opt('wr', ('				if (blk >= blocks - 32)\n', '				if (n >= blocks - 32)\n')),
    opt('cp', (COPY, '''			memcpy(xb.dump + (dst * ppb + p) * 512, src + p * 528, 512);
			memcpy(xb.dumpSpare + (dst * ppb + p) * 16, src + p * 528 + 512, 16);
''')),
    opt('j', ('	uint8_t *src;\n\n	int rr', '	uint8_t *src;\n	int rr')),
]
