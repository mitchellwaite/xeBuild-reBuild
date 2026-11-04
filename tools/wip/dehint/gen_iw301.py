# attempt 24: the arm-store route, the zeroing memset on the else path only: dse3 can then remove it in imgAdd too (a memset before the test feeds both the arm's store and the join's PHI and survives dse3 there, seen in the dumps of gen_iw299 s1).
# `python tools/wip/dehint/iw23sw.py tools/wip/dehint/gen_iw301.py build/iw/a24/nt.c 4 60`
L0 = '						left = (off & 0x1ffff) ? 256 - (off & 0x1ffff) / 512 : 256;\n'
RO = '						if (pages & 3)\n							pages = (pages + 4) & ~3;\n'
S9 = '						left -= pages;\n						s[9] = left >> 2;\n'
OLD = L0 + RO + S9
I = '						'
M = '(off & 0x1ffff)'
def b(*l):
    return ''.join(I + x + '\n' for x in l)
ST = 'struct { uint32_t before, file; } used;'
AR = 'uint32_t used[2];'
def body(decl, A, Z, F, sub, extra=()):
    return b('{', '	' + decl, *extra, '', '	if ' + M, '		' + A + ' = ' + M + ' / 512;', '	else', '		' + Z, *sub, '	s[9] = left >> 2;', '}')
FO = [('', [])]
ZA = 'memset(used, 0, sizeof(used));'
ZS = 'memset(&used, 0, sizeof(used));'
R = ['	if (pages & 3)', '		pages = (pages + 4) & ~3;']
SUBS = {
 'j': R + ['	used[1] = pages;', '	left = 256 - used[0] - used[1];'],
 'k': ['	left = 256 - used[0];'] + R + ['	used[1] = pages;', '	left -= used[1];'],
 'l': ['	left = 256 - used[0];'] + R + ['	left -= pages;'],
 'm': R + ['	left = 256 - used[0] - pages;'],
}
for sl, sub in SUBS.items():
    FO.append(('a' + sl, [(OLD, body(AR, 'used[0]', ZA, None, sub))]))
    FO.append(('s' + sl, [(OLD, body(ST, 'used.before', ZS, None, [x.replace('used[0]', 'used.before').replace('used[1]', 'used.file') for x in sub]))]))
AXES = [FO]
