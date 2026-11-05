"""parseDump: gen_ir47's `dest == -1 || (uint32_t)dest < numBlocks` folds u2's test through n, 6 loose lines, but ifcombine leaves `_148 = dest == -1` in T, so T
isn't an empty forwarder when the test folds in fre3, and the log block merged with it has T's freq 760, not 220: blk gets a register in the site 3 loop
(IRA: mem cost 2 uses * 4 * freq/10 vs border 464, limit freq 580).  Forms that leave T empty: the test computed before the loop, `?:`."""
FOCUS = ['_parseDump']
T = 'xb.badRemap[i] == -1 && dest < numBlocks) {\n		log_printf(1, "block 0x%x was remapped to block 0x%x at remap instance %d\\n", block, dest, i);\n		xb.badRemap[i] = dest;\n		found = 1;\n	}\n	i++;'
H = '	int found = 0;\n\n	i = 0;\n	goto test;\n'


def t(new):
    return [(T, T.replace('dest < numBlocks', new))]


def v(decl):
    return [(T, T.replace('dest < numBlocks', 'valid')), (H, '	int found = 0;\n	' + decl + '\n\n	i = 0;\n	goto test;\n')]


AXT = [
    ('q1', t('(dest != -1 ? (uint32_t)dest < numBlocks : 1)')),
    ('q2', t('(dest == -1 ? 1 : (uint32_t)dest < numBlocks)')),
    ('v1', v('int valid = dest == -1 || (uint32_t)dest < numBlocks;')),
    ('v2', v('int valid = (uint32_t)dest < numBlocks || dest == -1;')),
    ('v3', v('int valid = dest < 0 || (uint32_t)dest < numBlocks;')),
    ('v4', v('int valid = dest != -1 ? (uint32_t)dest < numBlocks : 1;')),
    ('v5', v('int valid = dest < numBlocks;')),
]
U1 = '''			if (blk >= blocks)
				__builtin_unreachable();
			log_printf(1, "ECD'''
U2 = '''		if (blk >= blocks)
			__builtin_unreachable();
		if (dst != blk &&'''
BAR = '''			__asm__("");
			dst = blk;
'''


def opt(name, a, b):
    return [(name + 'k', []), (name + '0', [(a, b)])]


AXES = [AXT,
        opt('u1', U1, '			log_printf(1, "ECD'),
        opt('u2', U2, '		if (dst != blk &&'),
        opt('b', BAR, '			dst = blk;\n'),
        ]
