"""parseDump: gen_ir50's `blk < blocks` guard isn't folded (no signed relation without an unreachable).  The test must reach profile_estimate (not fold in fre1) and fold
later: `!=` against the loop's bound: n < blocks gives n != blocks in VRP and DOM, not in FRE."""
FOCUS = ['_parseDump']
BASE = 'tools/wip/dehint/drafts/image_read_attempt3.c'
ARM = '''		if (dst == -4) {
			if (blk >= blocks)
				__builtin_unreachable();
			log_printf(1, "ECD error at block 0x%x (raw offset 0x%x), block will be remapped\\n", blk, src - raw);
			if (!addRemapP(blk, blk, blk, -1, blocks))
				return 0;
			__asm__("");
			dst = blk;
		} else {
'''
LOG = '''log_printf(1, "ECD error at block 0x%x (raw offset 0x%x), block will be remapped\\n", blk, src - raw);
			'''
CALL = '''if (!addRemapP(blk, blk, blk, -1, blocks))
				return 0;
			'''
BODY = LOG + CALL
COND = ['blk != blocks', 'n != blocks', 'blocks != blk', 'blocks != n', 'n <= (uint32_t)blocks', 'n != (uint32_t)blocks', 'n <= blocks - 1']
AX = [('keep', [])]
for i, c in enumerate(COND):
    for sh, v in (('a', '		if (dst == -4) {\n			if (@C@) {\n				' + BODY + '}\n			__BAR__dst = blk;\n		} else {\n'),
                  ('b', '		if (dst == -4) {\n			if (@C@) {\n				' + BODY + '__BAR__dst = blk;\n			}\n		} else {\n'),
                  ('c', '		if (dst == -4) {\n			if (@C@) {\n				' + LOG + '}\n			' + CALL + '__BAR__dst = blk;\n		} else {\n')):
        v = v.replace('@C@', c)
        AX.append(('c%d%s.b' % (i, sh), [(ARM, v.replace('__BAR__', '__asm__("");\n			'))]))
        AX.append(('c%d%s.nb' % (i, sh), [(ARM, v.replace('__BAR__', ''))]))
CB = '''	__asm__("" : : "ri"(cb), "ri"(cb), "ri"(cb), "ri"(cb));
'''
AXES = [AX, [('ck', []), ('c0', [(CB, '')])]]
