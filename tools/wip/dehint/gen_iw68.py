# attempt 5: imgAddFile fully natural (no expect, no dead tests) on the landed imgAdd: forms of the fits test x declaration x stores
HEAD = '''	/* imgFits by hand, its limit before the dead len++: VRP1's threading
	   of the two dead tests copies the block after len++ (which gives the
	   original's head registers), so names defined there are renumbered
	   high.  lim (one use, expanded at the test) keeps a low number:
	   `lim < end` then comes out in the original's operand order.  end lives
	   to DOM2 through `end < off` (the dead test's first half), which then
	   replaces off + len by it: `end > rawSize` in the original's order too */
	uint32_t lim = (xb.fsEnd - 1) * 0x4000;
	uint32_t end = off + len;

	if (end < off && (len & 0x3fff) > 0x3fff)
		len++;
	if (__builtin_expect(lim >= off + len, 1)) {
		/* dead; the noreturn call predicts it not taken, so the threading
		   that removes it doesn't leave the error edge at 75% (the error
		   block is then laid out after the big-block path) */
		if ((end & 0x3fff) > 0x3fff)
			abort();
'''
ELSE = '''	} else {
		log_printf(0, "\\n******* ERROR: adding %s will exceed available flash space! Skipped!\\n\\n", name);
	}
}

void imgAddFileAs'''
ERR = '''		log_printf(0, "\\n******* ERROR: adding %s will exceed available flash space! Skipped!\\n\\n", name);
'''
F = {
 'fits': '\n	if (imgFits(off, len)) {\n',
 'lim': '	uint32_t lim = (xb.fsEnd - 1) * 0x4000;\n\n	if (lim >= off + len) {\n',
 'limend': '	uint32_t lim = (xb.fsEnd - 1) * 0x4000;\n	uint32_t end = off + len;\n\n	if (lim >= end) {\n',
 'endlim': '	uint32_t end = off + len;\n	uint32_t lim = (xb.fsEnd - 1) * 0x4000;\n\n	if (end <= lim) {\n',
 'endlim2': '	uint32_t end = off + len;\n	uint32_t lim = (xb.fsEnd - 1) * 0x4000;\n\n	if (lim >= end) {\n',
 'end': '	uint32_t end = off + len;\n\n	if ((xb.fsEnd - 1) * 0x4000 >= end) {\n',
 'end2': '	uint32_t end = off + len;\n\n	if (end <= (xb.fsEnd - 1) * 0x4000) {\n',
 'expr': '\n	if ((xb.fsEnd - 1) * 0x4000 >= off + len) {\n',
 'exprr': '\n	if (off + len <= (xb.fsEnd - 1) * 0x4000) {\n',
}
AXES = [[(k, [(HEAD, v)]) for k, v in F.items()]]
