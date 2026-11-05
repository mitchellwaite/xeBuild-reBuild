"""pin_size (attempt 8), the helper lever: calcBlAreaSize's two round-ups ((size + 0xffff) & ~0xffff, (size + 0x3fff) & ~0x3fff)
through a general align helper, which einline takes and which changes the freed SSA names PRE reuses."""
import itertools, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
import bdhints

A16 = '''static uint32_t align16(uint32_t v)
{
	return (v + 15) & ~15;
}
'''
HELP = {
    'up': '''
/* v rounded up to a multiple of a (a power of two) */
static uint32_t alignUp(uint32_t v, uint32_t a)
{
	return (v + a - 1) & ~(a - 1);
}
''',
    'mask': '''
/* v rounded up to the next multiple of mask + 1 */
static uint32_t alignUp(uint32_t v, uint32_t mask)
{
	return (v + mask) & ~mask;
}
''',
}
S1 = '		size = (size + 0xffff) & ~0xffff;\n'
S2 = '	if (size & 0x3fff)\n		size = (size + 0x3fff) & ~0x3fff;\n'


def CASES(base):
    if A16 not in base or S1 not in base or S2 not in base:
        raise ValueError('text')
    out = []
    for h, s1, s2, pin in itertools.product(HELP, (0, 1), (0, 1, 2), (1, 0)):
        if not s1 and not s2:
            continue
        a, b = ('0x10000', '0x4000') if h == 'up' else ('0xffff', '0x3fff')
        t = base.replace(A16, A16 + HELP[h])
        if s1:
            t = t.replace(S1, '		size = alignUp(size, %s);\n' % a)
        if s2 == 1:
            t = t.replace(S2, '	if (size & 0x3fff)\n		size = alignUp(size, %s);\n' % b)
        elif s2 == 2:
            t = t.replace(S2, '	size = alignUp(size, %s);\n' % b)
        if not pin:
            t = bdhints.off(t, 'pin_size')
        out.append(('%s s1=%d s2=%d pin%d' % (h, s1, s2, pin), t))
    return out


FOCUS = ['_calcBlAreaSize']
