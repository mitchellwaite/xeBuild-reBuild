"""flg1.py: small spelling grid at the natural tail, all parseIni dead tests removed."""
import itertools, sys
import fllib as L, flpi as P

B0 = P.gen('else', 'after', 'nest', 'nest', 'else', dead=P.ALLDEAD)
BLIF = '''			len = comma;
			noCrc = 0;
			if (comma > nul) {
				len = nul;
				noCrc = 1;
			}
'''
SECIF = '''		if (comma > nul) {
			noCrc = 1;
			len = nul;
		} else {
			noCrc = 0;
			len = comma;
		}
'''
FLIF = '''		noCrc = 1;
		len = nul;
		if (comma >= 0 && comma < nul) {
			len = comma;
			noCrc = 0;
		}
'''
BL = {
 'cur': BLIF,
 'rev': BLIF.replace('comma > nul', 'nul < comma'),
 'ord': BLIF.replace('len = comma;\n			noCrc = 0;', 'noCrc = 0;\n			len = comma;'),
 'ord2': BLIF.replace('len = nul;\n				noCrc = 1;', 'noCrc = 1;\n				len = nul;'),
 'else': SECIF.replace('\n\t\t', '\n\t\t\t').replace('\t\tif', '\t\t\tif', 1),
 'else2': '			if (comma < nul) {\n				len = comma;\n				noCrc = 0;\n			} else {\n				len = nul;\n				noCrc = 1;\n			}\n',
 'else3': '			if (comma <= nul) {\n				len = comma;\n				noCrc = 0;\n			} else {\n				len = nul;\n				noCrc = 1;\n			}\n',
 'dflt': '			noCrc = 1;\n			len = nul;\n			if (comma <= nul) {\n				len = comma;\n				noCrc = 0;\n			}\n',
}
SEC = {
 'cur': SECIF,
 'rev': SECIF.replace('comma > nul', 'nul < comma'),
 'ord': SECIF.replace('noCrc = 1;\n			len = nul;', 'len = nul;\n			noCrc = 1;'),
 'ord2': SECIF.replace('noCrc = 0;\n			len = comma;', 'len = comma;\n			noCrc = 0;'),
 'ord3': SECIF.replace('noCrc = 1;\n			len = nul;', 'len = nul;\n			noCrc = 1;').replace('noCrc = 0;\n			len = comma;', 'len = comma;\n			noCrc = 0;'),
 'dflt': '		len = comma;\n		noCrc = 0;\n		if (comma > nul) {\n			len = nul;\n			noCrc = 1;\n		}\n',
 'le': '		if (comma <= nul) {\n			noCrc = 0;\n			len = comma;\n		} else {\n			noCrc = 1;\n			len = nul;\n		}\n',
}
FL = {
 'cur': FLIF,
 'ord': FLIF.replace('noCrc = 1;\n		len = nul;', 'len = nul;\n		noCrc = 1;'),
 'ord2': FLIF.replace('len = comma;\n			noCrc = 0;', 'noCrc = 0;\n			len = comma;'),
 'ord3': FLIF.replace('noCrc = 1;\n		len = nul;', 'len = nul;\n		noCrc = 1;').replace('len = comma;\n			noCrc = 0;', 'noCrc = 0;\n			len = comma;'),
 'nest': '		noCrc = 1;\n		len = nul;\n		if (comma >= 0) {\n			if (comma < nul) {\n				len = comma;\n				noCrc = 0;\n			}\n		}\n',
 'else': '		if (comma >= 0 && comma < nul) {\n			len = comma;\n			noCrc = 0;\n		} else {\n			noCrc = 1;\n			len = nul;\n		}\n',
 'rev': FLIF.replace('comma < nul', 'nul > comma'),
}
POSN = '				pos = pos + n + 1;\n				xb.rawPatch'
RAW = {
 'cur': POSN,
 'pluseq': '				pos += n + 1;\n				xb.rawPatch',
 'n1': '				pos = n + pos + 1;\n				xb.rawPatch',
 'n2': '				pos = pos + 1 + n;\n				xb.rawPatch',
}


def apply(bl='cur', sec='cur', fl='cur', raw='cur', base=B0):
    s = L.sub(base, BLIF, BL[bl])
    s = L.sub(s, SECIF, SEC[sec])
    s = L.sub(s, FLIF, FL[fl])
    s = L.sub(s, POSN, RAW[raw])
    return s


if __name__ == '__main__':
    V = {}
    for k in itertools.product(BL, SEC, FL, RAW):
        V['_'.join(k)] = apply(*k)
    print(len(V))
    rs = L.sweep(V, prefix='g1', show=30)
    with open(L.BD + '/g1.txt', 'w', newline='\n') as f:
        for n, (sc, st, fd, sd) in rs:
            f.write('%s %s %s %s\n' % (sc, n, fd, sd))
