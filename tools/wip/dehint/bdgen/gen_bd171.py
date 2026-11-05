"""patchBlsBlmod without no-early-inlining: small always-inlined helpers (an align16, a file-by-type lookup returning the entry), to see whether
another early-inlined call moves the third findFile's i off the low names."""
import itertools

NEI = '__attribute__((optimize("no-early-inlining")))\nvoid patchBlsBlmod'
HEAD = 'void patchBlsBlmod(const void *blmod, int size)\n{'
AL = '''static uint32_t align16(uint32_t v)
{
	return (v + 15) & ~15;
}

'''
S = {
    'a': ('xb.files[cbb].size = (addr + len + 15) & ~15;', 'xb.files[cbb].size = align16(addr + len);'),
    'b': ('xb.files[cd].size = (addr + len + 15) & ~15;', 'xb.files[cd].size = align16(addr + len);'),
    'c': ('		end = (off + size + 15) & ~15;\n		if (end > max)', '		end = align16(off + size);\n		if (end > max)'),
    'd': ('		end = (off + size + 15) & ~15;\n		i = end', '		end = align16(off + size);\n		i = end'),
}


def PRE(t):
    return t.replace(NEI, 'void patchBlsBlmod')


def CASES(base):
    out = []
    for k in range(1, 5):
        for c in itertools.combinations('abcd', k):
            def f(t, c=c):
                i = t.index(HEAD)
                pre, t = t[:i], t[i:]
                for n in c:
                    if S[n][0] not in t:
                        raise ValueError(S[n][0])
                    t = t.replace(S[n][0], S[n][1], 1)
                return pre + AL + t
            out.append((''.join(c), f))
    return out


FOCUS = ['_patchBlsBlmod']
