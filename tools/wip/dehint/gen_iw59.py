# attempt 4: near3 minus a6 (writeFsTable and imgAdd match, imgAddFile off): imgAddFile's forms
import os
BASE = os.environ.get('IWB', 'build/iw/a4/a6.c')
HEAD = '''	uint32_t lim = (xb.fsEnd - 1) * 0x4000;
	uint32_t end = off + len;

	if (end < off && (len & 0x3fff) > 0x3fff)
		len++;
	if (__builtin_expect(lim >= off + len, 1)) {
'''
LIM = '	uint32_t lim = (xb.fsEnd - 1) * 0x4000;\n'
F = {}
LENT = {
 'n': None,
 'p': '(len & 0x3fff) > 0x3fff',
 'e': 'end < off && (len & 0x3fff) > 0x3fff',
 'E': '(end & 0x3fff) > 0x3fff',
 'l': 'end < off',
 'o': '(off & 0x3fff) > 0x3fff',
 'k': 'end < len',
}
for ln, c in LENT.items():
    t = f'	if ({c})\n		len++;\n' if c else ''
    F[ln + 'F0'] = LIM + '	uint32_t end = off + len;\n\n' + t + '	if (__builtin_expect(lim >= off + len, 1)) {\n'
    F[ln + 'F1'] = LIM + '	uint32_t end = off + len;\n\n' + t + '	if (__builtin_expect(lim >= end, 1)) {\n'
    F[ln + 'F2'] = LIM + '	uint32_t end = off + len;\n\n' + t + '	end = off + len;\n	if (__builtin_expect(lim >= end, 1)) {\n'
    if c and 'end' not in c:
        F[ln + 'G0'] = LIM + '\n' + t + '	if (__builtin_expect(lim >= off + len, 1)) {\n'
        F[ln + 'G1'] = '\n' + t + '	if (__builtin_expect((xb.fsEnd - 1) * 0x4000 >= off + len, 1)) {\n'
    if not c:
        F[ln + 'G0'] = LIM + '\n	if (__builtin_expect(lim >= off + len, 1)) {\n'
        F[ln + 'G1'] = '\n	if (__builtin_expect((xb.fsEnd - 1) * 0x4000 >= off + len, 1)) {\n'
AB = '		if ((len & 0x3fff) > 0x3fff)\n			abort();\n'
AXES = [
 [(k, [(HEAD, v)]) for k, v in F.items()],
 [('', []),
  ('A0', [(AB, '')]),
  ('A1', [(AB, '		if ((end & 0x3fff) > 0x3fff)\n			abort();\n')]),
  ('A2', [(AB, '		if ((off & 0x3fff) > 0x3fff)\n			abort();\n')])],
]
