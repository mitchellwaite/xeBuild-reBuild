"""fl10l.py [ff|loop|ff,loop] [n]: parseIni's declaration order at a Part 2 state.  into-SSA numbers PHIs by DECL_UID order, so noCrc declared before len gives
flash's noCrc PHI the lower old version; dom3 takes rows by ascending old version.  Tie C needs noCrc's partition root below len's."""
import itertools, random, sys
import fllib as L, fl10lib as F, fl10h as H

DECL = """	FILE *f;
	unsigned char *buf, *p;
	int size, off, end, pos, len, nul, comma, n, i, nbl;
	uint32_t noCrc;
	char *s;
	uint32_t crc;
"""


def decl(s, order, noCrcPos, crcFirst=False):
    """order: the ints; noCrc goes before them (0), or between position k"""
    ints = 'int ' + ', '.join(order) + ';\n'
    d = "\tFILE *f;\n\tunsigned char *buf, *p;\n"
    if noCrcPos == 0:
        d += "\tuint32_t noCrc;\n\tint " + ', '.join(order) + ";\n"
    elif noCrcPos >= len(order):
        d += "\tint " + ', '.join(order) + ";\n\tuint32_t noCrc;\n"
    else:
        d += "\tint " + ', '.join(order[:noCrcPos]) + ";\n\tuint32_t noCrc;\n\tint " + ', '.join(order[noCrcPos:]) + ";\n"
    d += "\tchar *s;\n\tuint32_t crc;\n"
    return L.sub(s, DECL, d)


if __name__ == '__main__':
    lab = sys.argv[1] if len(sys.argv) > 1 else 'ff'
    B = H.state(lab)
    O = 'size off end pos len nul comma n i nbl'.split()
    V = {}
    for k in range(len(O) + 1):
        V['pos%d' % k] = decl(B, O, k)
    # samples: len after noCrc, others natural groupings
    random.seed(10)
    for t in range(int(sys.argv[2]) if len(sys.argv) > 2 else 0):
        o = O[:]
        random.shuffle(o)
        k = random.randint(0, len(o))
        V['r%s/%d' % (''.join(x[0:2] for x in o), k)] = decl(B, o, k)
    F.run(V, 'l_' + lab.replace(',', '_'), show=20)
