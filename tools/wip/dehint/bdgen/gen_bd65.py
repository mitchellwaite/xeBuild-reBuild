"""checkBl: bad = default's share of the switch + the arms'.  The switch splits its frequency evenly over its distinct targets, so
cases written out separately (duplicates tail-merge later) lower default's share.  Crc expects off."""
REMOVE = ['crc5', 'crc7', 'crc8', 'crc9', 'crc10', 'crc12', 'crc13']
FOCUS = ['_checkBl']
G = [
    ([5, 6, 11, 17], '''		if (bl[1] != 'B')
			goto magic;
		memset(bl + 0x10, 0, 0x30);
		c = crc32(bl, blsize);
		if (crc != c)
			goto bad;
		break;
'''),
    ([7, 18], '''		if (bl[1] != 'D')
			goto magic;
		memset(bl + 0x10, 0, 0x10);
		c = crc32(bl, blsize);
		if (crc != c)
			goto bad;
		break;
'''),
    ([8, 19], '''		if (bl[1] != 'E')
			goto magic;
		memset(bl + 0x10, 0, 0x10);
		c = crc32(bl, blsize);
		if (crc != c)
			goto bad;
		raiseKernel(getBeU16(bl), getBeU16(bl + 2), getBeU16(bl + 4));
		break;
'''),
    ([9, 15, 20], '''		if (bl[1] != 'F')
			goto magic;
		memset(bl + 0x20, 0, 0x210);
		c = crc32(bl, blsize);
		if (crc != c)
			goto bad;
		raiseKernel(getBeU16(bl), getBeU16(bl + 20), getBeU16(bl + 22));
		break;
'''),
    ([10, 16, 21], '''		if (bl[1] != 'G')
			goto magic;
		memset(bl + 0x10, 0, 0x10);
		c = crc32(bl, blsize);
		if (crc != c)
			goto bad;
		break;
'''),
]


def labels(ls):
    return ''.join('\tcase %d:\n' % x for x in ls)


AXES = []
for ls, body in G:
    old = labels(ls) + body
    ax = [('', [])]
    new = ''.join(labels([x]) + body for x in ls)
    ax.append(('s%d' % ls[0], [(old, new)]))
    if len(ls) > 2:
        new = labels(ls[:1]) + body + labels(ls[1:]) + body
        ax.append(('h%d' % ls[0], [(old, new)]))
    AXES.append(ax)
AXES.append([('hot', []), ('plain', [('toobig: __attribute__((hot));\n', 'toobig:\n')])])
