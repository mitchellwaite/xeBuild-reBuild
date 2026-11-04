# attempt 21: a helper big enough to stay out of early inlining: the block's page range (npages and the first page), or the whole per-block body. Its own profile_estimate then sets P(partial), and IPA inlining scales it.
# `python tools/wip/dehint/iw21pe.py tools/wip/dehint/gen_iw276.py build/iw/a21/nopt.c pageRange`
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
TOP = '''static uint32_t pageRange(uint32_t off, uint32_t len, uint8_t type, uint32_t *first)
{
	_Bool small = type != 0 && type != '0';
	int partial = small && len < 0x4000;
	uint8_t t = type - '1';
	uint32_t p = 0, npages;
'''
PP = '''	if (t < 15) {
		p = xb.bigBlock ? off & 0x1ffff : off & 0x3fff;
		if (p) p /= 512;
	}
	*first = p;
'''
F = {
 'plain': TOP + '''	if (partial > 0) {
		if (len % 512)
			npages = (len + 512) / 512;
		else
			npages = len / 512;
	} else
		npages = 32;
''' + PP + '''	return p + npages;
}
''',
 'retarm': TOP + PP + '''	if (partial > 0) {
		if (len % 512)
			npages = (len + 512) / 512;
		else
			npages = len / 512;
		return p + npages;
	}
	return p + 32;
}
''',
 'retelse': TOP + PP + '''	if (partial <= 0)
		return p + 32;
	if (len % 512)
		npages = (len + 512) / 512;
	else
		npages = len / 512;
	return p + npages;
}
''',
 'retconst': TOP + PP + '''	if (partial > 0) {
		if (len % 512)
			npages = (len + 512) / 512;
		else
			npages = len / 512;
		return npages;
	}
	return 32;
}
''',
}
STATES = [(k, [(DEF, v + '\n' + DEF), (H_, '\t\tend = pageRange(off, len, type, &p);\n\t\tfor (; p < end; p++) {\n')]) for k, v in F.items()]
STATES[-1] = ('retconst', [(DEF, F['retconst'] + '\n' + DEF), (H_, '\t\tnpages = pageRange(off, len, type, &p);\n\t\tfor (end = p + npages; p < end; p++) {\n')])
