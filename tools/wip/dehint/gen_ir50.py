"""parseDump, on attempt 3's draft (`valid`, no u2).  u1 raises the ECD block's freq 25 -> 58 at profile_estimate: PRED_CALL looks only at the first block of the
guarded arm, and with a test there it doesn't see the log call.  A plain guard does the same: site 2's `if (blk < blocks)` in place of the unreachable, barrier
and pin_cb on or off.  Also `dst < 0` forms of the arm's test."""
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
V = {
    'keep': ARM,
    'g1': '		if (dst == -4) {\n			if (blk < blocks) {\n				' + BODY + '}\n			__BAR__dst = blk;\n		} else {\n',
    'g2': '		if (dst == -4) {\n			if (blk < blocks) {\n				' + BODY + '__BAR__dst = blk;\n			}\n		} else {\n',
    'g3': '		if (dst == -4) {\n			if (blk < blocks - 0) {\n				' + LOG + '}\n			' + CALL + '__BAR__dst = blk;\n		} else {\n',
    'g4': '		if (dst == -4) {\n			if (blk >= blocks)\n				return 0;\n			' + BODY + '__BAR__dst = blk;\n		} else {\n',
    'g5': '		if (dst == -4) {\n			if (blk >= blocks)\n				goto next;\n			' + BODY + '__BAR__dst = blk;\n		} else {\n',
    'g6': '		if (dst == -4) {\n			if (blk >= blocks)\n				continue;\n			' + BODY + '__BAR__dst = blk;\n		} else {\n',
}
AX = []
for k, v in V.items():
    if k == 'keep':
        AX.append((k, []))
        continue
    AX.append((k + '.b', [(ARM, v.replace('__BAR__', '__asm__("");\n			'))]))
    AX.append((k + '.nb', [(ARM, v.replace('__BAR__', ''))]))
CB = '''	__asm__("" : : "ri"(cb), "ri"(cb), "ri"(cb), "ri"(cb));
'''
AXES = [AX, [('ck', []), ('c0', [(CB, '')])]]
