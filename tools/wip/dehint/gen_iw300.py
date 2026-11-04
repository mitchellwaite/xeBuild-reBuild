# attempt 24: the arm-store route without memset: the outer array read through a pointer, so (from memory) it stays addressable past late SRA, the load survives to PRE, and the arm's store is dead only from PRE on. Every entry is real: the pages before off in the 128K block and the file's own.
# `python tools/wip/dehint/iw23sw.py tools/wip/dehint/gen_iw300.py build/iw/a24/nt.c 4 60`
L0 = '						left = (off & 0x1ffff) ? 256 - (off & 0x1ffff) / 512 : 256;\n'
RO = '						if (pages & 3)\n							pages = (pages + 4) & ~3;\n'
S9 = '						left -= pages;\n						s[9] = left >> 2;\n'
OLD = L0 + RO + S9
I = '						'
M = '(off & 0x1ffff)'
def b(*l):
    return ''.join(I + x + '\n' for x in l)
INIT = {
 'i0': ('uint32_t used[2] = { 0, 0 };', None),
 'i1': ('uint32_t used[2];', 'used[0] = 0;'),
 'i2': ('uint32_t used[2] = { 0 };', None),
}
LOOPS = {
 'p1': ('uint32_t *u;', ('left = 256;', 'for (u = used; u != used + 2; u++)', '	left -= *u;')),
 'p2': ('uint32_t *u;', ('left = 256;', 'for (u = used; u < used + 2; u++)', '	left -= *u;')),
 'p3': ('uint32_t *u = used;', ('left = 256 - *u;', 'left -= *++u;')),
 'p4': ('uint32_t *u = used;', ('left = 256 - u[0] - u[1];',)),
 'p5': ('const uint32_t *u = used;', ('left = 256 - *u++;', 'left -= *u;')),
 'p6': ('uint32_t *u, *e = used + 2;', ('left = 256;', 'for (u = used; u != e; u++)', '	left -= *u;')),
 'p7': ('int k;', ('left = 256;', 'for (k = 0; k < 2; k++)', '	left -= *(used + k);')),
}
FO = [('', [])]
for il, (d, st) in INIT.items():
    for ll, (ld, lp) in LOOPS.items():
        body = ['{', '	' + d, '	' + ld, '']
        if st:
            body.append('	' + st)
        body += ['	if ' + M, '		used[0] = ' + M + ' / 512;', '	if (pages & 3)', '		pages = (pages + 4) & ~3;', '	used[1] = pages;']
        body += ['	' + x for x in lp]
        body += ['	s[9] = left >> 2;', '}']
        FO.append((il + ll, [(OLD, b(*body))]))
AXES = [FO]
