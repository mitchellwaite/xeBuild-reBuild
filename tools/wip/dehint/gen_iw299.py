# attempt 24: a store in the arm rather than a clobber. An outer local that SRA can't take (memset keeps it addressable, or an index still variable at late SRA) holds the offset's pages; FRE can't see past the PHI of vdefs, PRE forwards the load, so the arm's store is dead only from PRE on, lim2 can't move a store, and dce4 removes it after lim2's cleanup has already taken the else edge's forwarder.
# `python tools/wip/dehint/iw23sw.py tools/wip/dehint/gen_iw299.py build/iw/a24/nt.c 4 40`
L0 = '						left = (off & 0x1ffff) ? 256 - (off & 0x1ffff) / 512 : 256;\n'
RO = '						if (pages & 3)\n							pages = (pages + 4) & ~3;\n'
S9 = '						left -= pages;\n						s[9] = left >> 2;\n'
OLD = L0 + RO + S9
I = '						'
M = '(off & 0x1ffff)'
def b(*l):
    return ''.join(I + x + '\n' for x in l)
ST = 'struct { uint32_t before, file; } used;'
FO = [('', []),
 # array, memset, both entries real
 ('m1', [(OLD, b('{', '	uint32_t used[2];', '', '	memset(used, 0, sizeof(used));', '	if ' + M, '		used[0] = ' + M + ' / 512;', '	if (pages & 3)', '		pages = (pages + 4) & ~3;', '	used[1] = pages;', '	left = 256 - used[0] - used[1];', '	s[9] = left >> 2;', '}'))]),
 ('m2', [(OLD, b('{', '	uint32_t used[2];', '	int k;', '', '	memset(used, 0, sizeof(used));', '	if ' + M, '		used[0] = ' + M + ' / 512;', '	if (pages & 3)', '		pages = (pages + 4) & ~3;', '	used[1] = pages;', '	left = 256;', '	for (k = 0; k < 2; k++)', '		left -= used[k];', '	s[9] = left >> 2;', '}'))]),
 ('m3', [(OLD, b('{', '	uint32_t used[2];', '', '	memset(used, 0, sizeof(used));', '	if ' + M, '		used[0] = ' + M + ' / 512;', '	left = 256 - used[0];', '	if (pages & 3)', '		pages = (pages + 4) & ~3;', '	used[1] = pages;', '	left -= used[1];', '	s[9] = left >> 2;', '}'))]),
 # struct
 ('s1', [(OLD, b('{', '	' + ST, '', '	memset(&used, 0, sizeof(used));', '	if ' + M, '		used.before = ' + M + ' / 512;', '	if (pages & 3)', '		pages = (pages + 4) & ~3;', '	used.file = pages;', '	left = 256 - used.before - used.file;', '	s[9] = left >> 2;', '}'))]),
 ('s2', [(OLD, b('{', '	' + ST, '', '	memset(&used, 0, sizeof(used));', '	if ' + M, '		used.before = ' + M + ' / 512;', '	left = 256 - used.before;', '	if (pages & 3)', '		pages = (pages + 4) & ~3;', '	used.file = pages;', '	left -= used.file;', '	s[9] = left >> 2;', '}'))]),
 # no memset: the entries assigned, the index variable until cunrolli (late SRA may still take it)
 ('n1', [(OLD, b('{', '	uint32_t used[2] = { 0, 0 };', '	int k;', '', '	if ' + M, '		used[0] = ' + M + ' / 512;', '	if (pages & 3)', '		pages = (pages + 4) & ~3;', '	used[1] = pages;', '	left = 256;', '	for (k = 0; k < 2; k++)', '		left -= used[k];', '	s[9] = left >> 2;', '}'))]),
 # scalar
 ('v1', [(OLD, b('{', '	uint32_t used;', '', '	memset(&used, 0, sizeof(used));', '	if ' + M, '		used = ' + M + ' / 512;', '	left = 256 - used;', '	if (pages & 3)', '		pages = (pages + 4) & ~3;', '	left -= pages;', '	s[9] = left >> 2;', '}'))]),
]
AXES = [FO]
