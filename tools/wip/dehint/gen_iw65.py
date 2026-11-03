# attempt 4: imgAddFile fully natural (no expect, no dead tests) on a4's imgAdd: forms of the fits test
import os
BASE = os.environ.get('IWB', 'tools/wip/dehint/drafts/image_write_a4.c')
HEAD = '''	uint32_t lim = (xb.fsEnd - 1) * 0x4000;
	uint32_t end = off + len;

	if (end < off && (len & 0x3fff) > 0x3fff)
		len++;
	if (__builtin_expect(lim >= off + len, 1)) {
'''
AB = '		if ((end & 0x3fff) > 0x3fff)\n			abort();\n'
F = {
 'fits': '\n	if (imgFits(off, len)) {\n',
 'nfits': '\n	if (!imgFits(off, len)) {\n		log_printf(0, "\\n******* ERROR: adding %s will exceed available flash space! Skipped!\\n\\n", name);\n		return;\n	}\n	{\n',
 'lim': '	uint32_t lim = (xb.fsEnd - 1) * 0x4000;\n\n	if (lim >= off + len) {\n',
 'limend': '	uint32_t lim = (xb.fsEnd - 1) * 0x4000;\n	uint32_t end = off + len;\n\n	if (lim >= end) {\n',
 'endlim': '	uint32_t end = off + len;\n	uint32_t lim = (xb.fsEnd - 1) * 0x4000;\n\n	if (end <= lim) {\n',
 'end': '	uint32_t end = off + len;\n\n	if ((xb.fsEnd - 1) * 0x4000 >= end) {\n',
 'expr': '\n	if ((xb.fsEnd - 1) * 0x4000 >= off + len) {\n',
 'exprr': '\n	if (off + len <= (xb.fsEnd - 1) * 0x4000) {\n',
 'lt': '\n	if (off + len < (xb.fsEnd - 1) * 0x4000 + 1) {\n',
}
TAIL = '''	} else {
		log_printf(0, "\\n******* ERROR: adding %s will exceed available flash space! Skipped!\\n\\n", name);
	}
}

void imgAddFileAs'''
AXES = [
 [(k, [(AB, ''), (HEAD, v)] + ([(TAIL, '	}\n}\n\nvoid imgAddFileAs')] if k == 'nfits' else [])) for k, v in F.items()],
 [('', []), ('exp', [('(xb.fsEnd - 1) * 0x4000 >= off + len) {', '__builtin_expect((xb.fsEnd - 1) * 0x4000 >= off + len, 1)) {')]) ],
]
AXES = AXES[:1]
