"""align16 as a helper of the whole file: every `(x + 15) & ~15` in build.c, placed before its first user, with no-early-inlining gone from patchBlsBlmod.
x axes: which of the sites outside patchBlsBlmod use it."""
import itertools

NEI = '__attribute__((optimize("no-early-inlining")))\nvoid patchBlsBlmod'
AL = '''/* round up to the 16 bytes bootloaders are padded to */
static uint32_t align16(uint32_t v)
{
	return (v + 15) & ~15;
}

'''
ANCHOR = '/* read baseDir/name into e */\n'
BL = [
    ('xb.files[cbb].size = (addr + len + 15) & ~15;', 'xb.files[cbb].size = align16(addr + len);'),
    ('		end = (off + size + 15) & ~15;\n		if (end > max)', '		end = align16(off + size);\n		if (end > max)'),
    ('		end = (off + size + 15) & ~15;\n		i = end', '		end = align16(off + size);\n		i = end'),
]
HEAD = 'void patchBlsBlmod(const void *blmod, int size)\n{'
BLCD = ('xb.files[cd].size = (addr + len + 15) & ~15;', 'xb.files[cd].size = align16(addr + len);')
OTHER = {
    'L': ('		e->size = (size + 15) & ~15;\n', '		e->size = align16(size);\n'),
    'G': ('name, size, (size + 15) & ~15);', 'name, size, align16(size));'),
}


def PRE(t):
    return t.replace(NEI, 'void patchBlsBlmod')


def CASES(base):
    out = []
    for l, g, r in itertools.product((0, 1), (0, 1), (0, 1)):
        def f(t, l=l, g=g, r=r):
            i = t.index(HEAD)
            pre, t = t[:i], t[i:]
            for a, b in BL + [BLCD]:
                if a not in t:
                    raise ValueError(a)
                t = t.replace(a, b, 1)
            if l:
                pre = pre.replace(*OTHER['L'])
            if g:
                pre = pre.replace(*OTHER['G'])
            if r:
                if BLCD[0] not in pre:
                    raise ValueError('resign')
                pre = pre.replace(*BLCD)
            return pre.replace(ANCHOR, AL + ANCHOR, 1) + t
        out.append(('L%d G%d R%d' % (l, g, r), f))
    return out
