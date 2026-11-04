# attempt 21: a void helper with the page count returned through a pointer: no const-return predictor, so an early return on the arm should give 73 with 39 = 63.35 (900 * P = 570, on imgAdd's grid).
# `python tools/wip/dehint/iw21pe.py tools/wip/dehint/gen_iw280.py build/iw/a21/nopt.c pageRange`
H_ = '''		small = type != 0 && type != '0';
		partial = small && len < 0x4000;
		if (partial > 0) {
			if (len % 512)
				npages = (len + 512) / 512;
			else
				npages = len / 512;
		} else
			npages = 32;
		p = 0;
		t = type - '1';
		if (t < 15) {
			p = xb.bigBlock ? off & 0x1ffff : off & 0x3fff;
			if (p) p /= 512;
		}
		for (end = p + npages; p < end; p++) {
'''
DEF = 'int imgAdd(uint32_t off, const void *src, uint32_t len, uint8_t type, uint16_t next, int pad)\n{'
TOP = '''static void pageRange(uint32_t off, uint32_t len, uint8_t type, uint32_t *first, uint32_t *count)
{
	_Bool small = type != 0 && type != '0';
	int partial = small && len < 0x4000;
	uint8_t t = type - '1';
	uint32_t p = 0;

	if (t < 15) {
		p = xb.bigBlock ? off & 0x1ffff : off & 0x3fff;
		if (p) p /= 512;
	}
	*first = p;
'''
F = {
 'retarm': TOP + '''	if (partial > 0) {
		if (len % 512)
			*count = (len + 512) / 512;
		else
			*count = len / 512;
		return;
	}
	*count = 32;
}
''',
 'retarm1': TOP + '''	if (partial > 0) {
		*count = (len + (len % 512 ? 512 : 0)) / 512;
		return;
	}
	*count = 32;
}
''',
 'noret': TOP + '''	if (partial > 0) {
		if (len % 512)
			*count = (len + 512) / 512;
		else
			*count = len / 512;
	} else
		*count = 32;
}
''',
}
STATES = [(k, [(DEF, v + '\n' + DEF), (H_, '\t\tpageRange(off, len, type, &p, &npages);\n\t\tfor (end = p + npages; p < end; p++) {\n')]) for k, v in F.items()]
