"""pin_size: patchBlsBlmod's answer was another early-inlined call shifting SSA names.  Each file-size lookup in calcBlAreaSize through a small helper or not (subsets, not all or none),
and align helpers for the two round-ups."""
import itertools, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
import bdhints

HEAD = 'uint32_t calcBlAreaSize(void)\n{'
HELP = '''static uint32_t blFileSize(int type)
{
	return xb.files[findFile(type)].size;
}

'''
JT = [('		x = findFile(5);\n		size = findFileOffset(5) + xb.files[x].size;\n', '		size = findFileOffset(5) + blFileSize(5);\n'),
      ('		x = findFile(7);\n		size += xb.files[x].size;\n', '		size += blFileSize(7);\n'),
      ('			x = findFile(14);\n			size += xb.files[x].size;\n', '			size += blFileSize(14);\n')]
XE = [('		x = findFile(11);\n		size = findFileOffset(11) + xb.files[x].size;\n', '		size = findFileOffset(11) + blFileSize(11);\n'),
      ('		x = findFile(12);\n		size += xb.files[x].size;\n', '		size += blFileSize(12);\n'),
      ('		x = findFile(13);\n		size += xb.files[x].size;\n', '		size += blFileSize(13);\n')]
LAST = ('		x = findFile(14);\n		/* the sum so far in ebx (esi up to the 13 lookup), as in the\n		   original: IRA otherwise keeps it in esi */\n		size += xb.files[x].size;\n', '		size += blFileSize(14);\n')
ALL = JT + XE + [LAST]


def PRE(t):
    return bdhints.off(t, 'pin_size')


def CASES(base):
    out = []
    for m in range(1, 1 << len(ALL)):
        def f(t, m=m):
            i = t.index(HEAD)
            pre, t = t[:i], t[i:]
            for k, (a, b) in enumerate(ALL):
                if m >> k & 1:
                    if a not in t:
                        raise ValueError(a)
                    t = t.replace(a, b, 1)
            return pre + HELP + t
        out.append(('%03x' % m, f))
    return out


FOCUS = ['_calcBlAreaSize']
