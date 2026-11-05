"""parseDump: u1/u2 exist so `dest < numBlocks` folds at sites 2/3 with an unsigned counter.  Spell the callee's test so that it folds through n itself:
(uint32_t)blk is n (FRE), and the loop test is n < (uint32_t)blocks.  -1 stays allowed by `dest == -1`, which is the no-remap value anyway."""
FOCUS = ['_parseDump']
TEST = 'xb.badRemap[i] == -1 && dest < numBlocks) {\n		log_printf(1, "block 0x%x was remapped to block 0x%x at remap instance %d\\n", block, dest, i);\n		xb.badRemap[i] = dest;\n		found = 1;\n	}\n	i++;'
T = TEST
def t(new):
    return [(T, T.replace('dest < numBlocks', new))]
AXT = [
       ('f1', t('(uint32_t)(dest + 1) <= numBlocks')),
       ('f2', t('dest + 1U <= numBlocks')),
       ('f3', t('(uint32_t)dest + 1 <= (uint32_t)numBlocks')),
       ('f4', t('(uint32_t)(dest + 1) < numBlocks + 1U')),
       ('f5', t('dest + 1 <= numBlocks')),
       ('f6', t('dest <= numBlocks - 1')),
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
CB = '''	__asm__("" : : "ri"(cb), "ri"(cb), "ri"(cb), "ri"(cb));
'''
B2 = '''			__asm__("" : "+r"(b2));
'''
def opt(name, a, b):
    return [(name + 'k', []), (name + '0', [(a, b)])]
AXES = [AXT,
        opt('u1', U1, '			log_printf(1, "ECD'),
        opt('u2', U2, '		if (dst != blk &&'),
        opt('b', BAR, '			dst = blk;\n'),
        opt('c', CB, ''),
        ]
