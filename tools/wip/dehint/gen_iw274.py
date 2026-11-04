# attempt 21: the page-count arm of imgAdd as a static helper, so `partial`'s test can carry an early-return or const-return prediction as well as its opcode heuristic.
# `python tools/wip/dehint/iw21pe.py tools/wip/dehint/gen_iw274.py build/iw/a21/nopt.c`
H_ = '''		if (partial > 0) {
			if (len % 512)
				npages = (len + 512) / 512;
			else
				npages = len / 512;
		} else
			npages = 32;
'''
DEF = 'int imgAdd(uint32_t off, const void *src, uint32_t len, uint8_t type, uint16_t next, int pad)\n{'
F = {
 'arm1ret': '''static uint32_t pageCount(uint32_t len, int partial)
{
	if (partial > 0) {
		if (len % 512)
			len += 512;
		return len / 512;
	}
	return 32;
}
''',
 'arm1ter': '''static uint32_t pageCount(uint32_t len, int partial)
{
	if (partial > 0)
		return len % 512 ? (len + 512) / 512 : len / 512;
	return 32;
}
''',
 'arm2ret': '''static uint32_t pageCount(uint32_t len, int partial)
{
	if (partial > 0) {
		if (len % 512)
			return (len + 512) / 512;
		return len / 512;
	}
	return 32;
}
''',
 'else1ret': '''static uint32_t pageCount(uint32_t len, int partial)
{
	if (partial <= 0)
		return 32;
	if (len % 512)
		return (len + 512) / 512;
	return len / 512;
}
''',
 'else1npos': '''static uint32_t pageCount(uint32_t len, int partial)
{
	if (!partial)
		return 32;
	if (len % 512)
		return (len + 512) / 512;
	return len / 512;
}
''',
 'else1local': '''static uint32_t pageCount(uint32_t len, int partial)
{
	uint32_t n;

	if (partial <= 0)
		return 32;
	if (len % 512)
		n = (len + 512) / 512;
	else
		n = len / 512;
	return n;
}
''',
 'armpos0': '''static uint32_t pageCount(uint32_t len, int partial)
{
	uint32_t n = 32;

	if (partial > 0) {
		if (len % 512)
			n = (len + 512) / 512;
		else
			n = len / 512;
	}
	return n;
}
''',
}
STATES = [(k, [(DEF, v + '\n' + DEF), (H_, '\t\tnpages = pageCount(len, partial);\n')]) for k, v in F.items()]
