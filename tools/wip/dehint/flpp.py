"""flpp.py: iniPreParse without the dead tests / expect / no-tree-loop-vectorize: subsets and
scope shapes.  Each candidate is scored on iniPreParse and the whole object."""
import itertools, sys
import fllib as L

s = L.base()
EXP = "__builtin_expect(buf[i] == ';', 0)"
DA = "	if (i < 0)\n		buf[0] = 1;\n"
DB = "		for (j = 0; j < 44; j++)\n			if (i < 0)\n				buf[j] = 1;\n"
FO = {'keep': L.ALLFLAGS,
      'noexp': ['-O3', '-fno-tree-loop-vectorize', '--param', 'lra-inheritance-ebb-probability-cutoff=60'],
      'nofiv': [f for f in L.ALLFLAGS if f != '-fno-tree-loop-vectorize'],
      'neither': ['-O3', '--param', 'lra-inheritance-ebb-probability-cutoff=60']}
A = s.index('int iniPreParse(unsigned char *buf, int size)\n{')
B = s.index('int memFindStr(unsigned char *buf, int size, const char *key, int label);')
PP = s[A:B]


def varies():
    # the validChars loop
    VC = {
     'cur': "for (j = 0; j < (int)sizeof(validChars); j++)\n			if ((char)buf[i] == (char)validChars[j])\n				break;\n		if (j == sizeof(validChars))\n			buf[i] = ' ';\n",
     'nocast': "for (j = 0; j < 74; j++)\n			if (buf[i] == validChars[j])\n				break;\n		if (j == 74)\n			buf[i] = ' ';\n",
     'set': "for (j = 0; j < 74; j++)\n			if ((char)buf[i] == (char)validChars[j])\n				j = 75;\n		if (j == 74)\n			buf[i] = ' ';\n",
     'flag': "valid = 0;\n		for (j = 0; j < 74; j++)\n			if ((char)buf[i] == (char)validChars[j])\n				valid = 1;\n		if (!valid)\n			buf[i] = ' ';\n",
     'cc': "c = buf[i];\n		for (j = 0; j < 74; j++)\n			if (c == (char)validChars[j])\n				break;\n		if (j == 74)\n			buf[i] = ' ';\n",
     'while': "j = 0;\n		while (j < 74 && (char)buf[i] != (char)validChars[j])\n			j++;\n		if (j == 74)\n			buf[i] = ' ';\n",
    }
    return VC


if __name__ == '__main__':
    V = {}
    VC = varies()
    for e, da, db in itertools.product([0, 1], [0, 1], [0, 1]):
        t = s
        if e:
            t = L.sub(t, EXP, "buf[i] == ';'")
        if da:
            t = L.sub(t, DA, '')
        if db:
            t = L.sub(t, DB, '')
        for fln in (['keep', 'nofiv'] if not e else ['noexp', 'neither']):
            for vn, vc in VC.items():
                u = L.sub(t, VC['cur'], vc)
                if vn == 'flag':
                    u = L.sub(u, '	int i, j, n = size;\n', '	int i, j, n = size, valid;\n')
                if vn == 'cc':
                    u = L.sub(u, '	int i, j, n = size;\n', '	int i, j, n = size;\n	char c;\n')
                V['e%d_a%d_b%d_%s_%s' % (e, da, db, fln, vn)] = (u, FO[fln])
    print(len(V))
    rs = L.sweep(V, prefix='pp', show=30)
    with open(L.BD + '/pp.txt', 'w', newline='\n') as f:
        for n, (sc, st, fd, sd) in rs:
            f.write('%s %s %s %s\n' % (sc, n, fd, sd))
