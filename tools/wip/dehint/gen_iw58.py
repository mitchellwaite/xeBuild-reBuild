# attempt 4: imgAddFile on lp1 (4 lines, the rawSize tests aren't ifcombined when `end` is computed before the dead len++): where end is computed, with or without the dead test
import os
BASE = os.environ.get('IWB', 'build/iw/a4/lp1.c')
HEAD = '''	uint32_t lim = (xb.fsEnd - 1) * 0x4000;
	uint32_t end = off + len;

	if ((len & 0x3fff) > 0x3fff)
		len++;
	if (__builtin_expect(lim >= end, 1)) {
'''
F = {
 'a': '''	uint32_t lim = (xb.fsEnd - 1) * 0x4000;
	uint32_t end;

	if ((len & 0x3fff) > 0x3fff)
		len++;
	end = off + len;
	if (__builtin_expect(lim >= end, 1)) {
''',
 'b': '''	uint32_t lim = (xb.fsEnd - 1) * 0x4000;
	uint32_t end = off + len;

	if (__builtin_expect(lim >= end, 1)) {
''',
 'c': '''	uint32_t lim = (xb.fsEnd - 1) * 0x4000;

	if (__builtin_expect(lim >= off + len, 1)) {
''',
 'd': '''	uint32_t lim = (xb.fsEnd - 1) * 0x4000;

	if ((len & 0x3fff) > 0x3fff)
		len++;
	if (__builtin_expect(lim >= off + len, 1)) {
''',
 'e': '''	uint32_t lim = (xb.fsEnd - 1) * 0x4000;
	uint32_t end = off + len;

	if (end < off)
		len++;
	if (__builtin_expect(lim >= off + len, 1)) {
''',
 'f': '''	uint32_t end = off + len;
	uint32_t lim = (xb.fsEnd - 1) * 0x4000;

	if (__builtin_expect(lim >= end, 1)) {
''',
 'g': '''	uint32_t end = off + len, lim;

	lim = (xb.fsEnd - 1) * 0x4000;
	if (__builtin_expect(lim >= end, 1)) {
''',
 'h': '''	uint32_t lim;

	if ((len & 0x3fff) > 0x3fff)
		len++;
	lim = (xb.fsEnd - 1) * 0x4000;
	if (__builtin_expect(lim >= off + len, 1)) {
''',
 'i': '''	if (__builtin_expect((xb.fsEnd - 1) * 0x4000 >= off + len, 1)) {
''',
 'j': '''	if ((len & 0x3fff) > 0x3fff)
		len++;
	if (__builtin_expect((xb.fsEnd - 1) * 0x4000 >= off + len, 1)) {
''',
}
AB = '		if ((len & 0x3fff) > 0x3fff)\n			abort();\n'
LPG = '		if (x > first + 0x4000)\n			blocks++;\n		if (x > first + 0x4000)\n			blocks += 2;\n'
AXES = [
 [(k, [(HEAD, v)]) for k, v in F.items()],
 [('', []), ('A0', [(AB, '')])],
 [('', []), ('m', [(LPG, '		if (x > first + 0x4000)\n			blocks += 2;\n')])],
]
