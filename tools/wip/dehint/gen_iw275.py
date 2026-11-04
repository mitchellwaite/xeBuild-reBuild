# attempt 21: the whole npages computation (small, partial, arm) in a static helper big enough to stay out of early inlining, so its returns' predictors survive into its own profile and IPA inlining brings them in.
# `python tools/wip/dehint/iw21pe.py tools/wip/dehint/gen_iw275.py build/iw/a21/nopt.c pageCount`
H_ = '''		small = type != 0 && type != '0';
		partial = small && len < 0x4000;
		if (partial > 0) {
			if (len % 512)
				npages = (len + 512) / 512;
			else
				npages = len / 512;
		} else
			npages = 32;
'''
DEF = 'int imgAdd(uint32_t off, const void *src, uint32_t len, uint8_t type, uint16_t next, int pad)\n{'
TOP = '''static uint32_t pageCount(uint32_t len, uint8_t type)
{
	_Bool small = type != 0 && type != '0';
	int partial = small && len < 0x4000;
'''
F = {
 'arm1': TOP + '''	if (partial > 0) {
		if (len % 512)
			len += 512;
		return len / 512;
	}
	return 32;
}
''',
 'arm1b': TOP + '''	if (partial > 0)
		return len % 512 ? (len + 512) / 512 : len / 512;
	return 32;
}
''',
 'arm2': TOP + '''	if (partial > 0) {
		if (len % 512)
			return (len + 512) / 512;
		return len / 512;
	}
	return 32;
}
''',
 'else1': TOP + '''	if (partial <= 0)
		return 32;
	if (len % 512)
		return (len + 512) / 512;
	return len / 512;
}
''',
 'elsenot': TOP + '''	if (!partial)
		return 32;
	if (len % 512)
		return (len + 512) / 512;
	return len / 512;
}
''',
 'elsevar': TOP + '''	uint32_t n;
	if (partial <= 0)
		return 32;
	if (len % 512)
		n = (len + 512) / 512;
	else
		n = len / 512;
	return n;
}
''',
 'single': TOP + '''	uint32_t n = 32;
	if (partial > 0) {
		if (len % 512)
			n = (len + 512) / 512;
		else
			n = len / 512;
	}
	return n;
}
''',
 'ifarm': TOP + '''	uint32_t n;
	if (partial > 0) {
		if (len % 512)
			n = (len + 512) / 512;
		else
			n = len / 512;
		return n;
	}
	return 32;
}
''',
}
STATES = [(k, [(DEF, v + '\n' + DEF), (H_, '\t\tnpages = pageCount(len, type);\n')]) for k, v in F.items()]
