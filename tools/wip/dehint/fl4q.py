"""fl4q.py single | rand N seed: natural source forms of flashfs, rawpatch and bl at fl4f's base, each alone or in combination."""
import random, sys
import fllib as L, fl4lib as F, fl4f as B

FL_IF = '''			noCrc = 1;
			len = nul;
			if (comma >= 0 && comma < nul) {
				len = comma;
				noCrc = 0;
			}
'''
FL = {
    'nest': '''			noCrc = 1;
			len = nul;
			if (comma >= 0) {
				if (comma < nul) {
					len = comma;
					noCrc = 0;
				}
			}
''',
    'else': '''			if (comma >= 0 && comma < nul) {
				len = comma;
				noCrc = 0;
			} else {
				len = nul;
				noCrc = 1;
			}
''',
    'elsen': '''			if (comma < 0 || comma >= nul) {
				len = nul;
				noCrc = 1;
			} else {
				len = comma;
				noCrc = 0;
			}
''',
    'neg1': '''			noCrc = 1;
			len = nul;
			if (comma != -1 && comma < nul) {
				len = comma;
				noCrc = 0;
			}
''',
    'order': '''			len = nul;
			noCrc = 1;
			if (comma >= 0 && comma < nul) {
				noCrc = 0;
				len = comma;
			}
''',
    'order2': '''			noCrc = 1;
			len = nul;
			if (comma >= 0 && comma < nul) {
				noCrc = 0;
				len = comma;
			}
''',
    'lt': '''			noCrc = 1;
			len = nul;
			if (nul > comma && comma >= 0) {
				len = comma;
				noCrc = 0;
			}
''',
    'init0': '''			noCrc = 0;
			len = comma;
			if (comma < 0 || comma >= nul) {
				len = nul;
				noCrc = 1;
			}
''',
    'tern': '''			noCrc = comma < 0 || comma >= nul;
			len = noCrc ? nul : comma;
''',
    'nocrcif': '''			noCrc = comma < 0 || comma >= nul;
			if (noCrc)
				len = nul;
			else
				len = comma;
''',
    'lenfirst': '''			len = nul;
			if (comma >= 0 && comma < nul)
				len = comma;
			noCrc = len != comma;
''',
}
FLORD = ('''			nul = memFindChar(p, 0, size - pos);
@@nul@@			comma = memFindChar(p, ',', size - pos);
''', '''			comma = memFindChar(p, ',', size - pos);
			nul = memFindChar(p, 0, size - pos);
''')
EDITS = {
    'loopbreak': ('''			if (pos >= size)
				i = 256;
''', '''			if (pos >= size)
				break;
'''),
    'crcvar': ('''					if (n == 0)
						crc = xb.firmwareCrc[i] = 0;
''', '''					if (n == 0) {
						crc = 0;
						xb.firmwareCrc[i] = 0;
					}
'''),
    'crcelse': ('''				} else
					crc = xb.firmwareCrc[i] = 0;
''', '''				} else {
					crc = 0;
					xb.firmwareCrc[i] = 0;
				}
'''),
    'lenbad': ('''			if (len <= 1023) {
				strncpy(xb.firmware[i], (char *)p, len);
''', '''			if (len < 1024) {
				strncpy(xb.firmware[i], (char *)p, len);
'''),
    'strlen': ('''					if (strlen(s) > 21) {
						log_printf(0, "\\n******* ERROR: file in [flashfs]''', '''					if ((int)strlen(s) > 21) {
						log_printf(0, "\\n******* ERROR: file in [flashfs]'''),
    'sifelse': ('''					if (s == NULL)
						s = strrchr(xb.firmware[i], '\\\\');
					s = s ? s + 1 : xb.firmware[i];
''', '''					if (s == NULL)
						s = strrchr(xb.firmware[i], '\\\\');
					if (s == NULL)
						s = xb.firmware[i];
					else
						s++;
'''),
    'digit': ('''				if (xb.firmware[i][len - 1] == '1' || xb.firmware[i][len - 1] == '2')
					xb.firmware[i][len - 1] = 0;
''', '''				if (xb.firmware[i][len - 1] == '1')
					xb.firmware[i][len - 1] = 0;
				else if (xb.firmware[i][len - 1] == '2')
					xb.firmware[i][len - 1] = 0;
'''),
    'nfw': ('''		xb.nFirmware = 0;
		log_printf(1, "\\nini: label [flashfs] found\\n");
		pos = off;
''', '''		log_printf(1, "\\nini: label [flashfs] found\\n");
		xb.nFirmware = 0;
		pos = off;
'''),
    'rawif': ('''			if (comma == -1 || comma >= nul) {
''', '''			if (comma < 0 || comma >= nul) {
'''),
    'rawpos': ('''				pos = pos + comma + 1;
				n = memFindChar''', '''				pos += comma + 1;
				n = memFindChar'''),
    'rawend': ('''			if (pos >= end)
				i = 16;
''', '''			if (pos >= end)
				break;
'''),
    'rawlog': ('''			if (off != -1) {
		end''', '''			if (off >= 0) {
		end'''),
    'blge': ('''	if (off >= 0) {
		log_printf(1, "\\nini: label %s found\\n", label);''', '''	if (off != -1) {
		log_printf(1, "\\nini: label %s found\\n", label);'''),
    'bllen': ('''			len = comma;
			noCrc = 0;
			if (comma > nul) {
				len = nul;
				noCrc = 1;
			}
''', '''			if (comma > nul) {
				len = nul;
				noCrc = 1;
			} else {
				len = comma;
				noCrc = 0;
			}
'''),
    'blinc': ('''			i++;
			if (pos > end) {
				log_printf(0, "\\n******* ERROR: ini problem, can't find enough data for %s section!\\n", label);
				free(buf);
				return 0;
			}
		}
''', '''			if (pos > end) {
				log_printf(0, "\\n******* ERROR: ini problem, can't find enough data for %s section!\\n", label);
				free(buf);
				return 0;
			}
			i++;
		}
'''),
    'blfor': ('''		for (i = 0; i < nbl; ) {
''', '''		i = 0;
		while (i < nbl) {
'''),
}


def gen(c):
    s = B.BASE
    if 'fl' in c:
        s = L.sub(s, FL_IF, FL[c['fl']])
    if 'ord' in c:
        k = s.rindex(FLORD[0].replace('@@nul@@', ''))
        s = s[:k] + FLORD[1] + s[k + len(FLORD[0].replace('@@nul@@', '')):]
    for e in c.get('ed', ()):
        s = L.sub(s, *EDITS[e])
    return s


def lab(c):
    return ','.join([c.get('fl', '')] + (['ord'] if 'ord' in c else []) + sorted(c.get('ed', ())))


if __name__ == '__main__':
    V = {}
    if sys.argv[1] == 'single':
        for f in FL:
            V['fl=' + f] = gen({'fl': f})
        V['ord'] = gen({'ord': 1})
        for e in EDITS:
            try:
                V[e] = gen({'ed': [e]})
            except ValueError as x:
                print('skip', e, x)
    else:
        N, seed = int(sys.argv[2]), int(sys.argv[3])
        rng = random.Random(seed)
        while len(V) < N:
            c = {'ed': [e for e in EDITS if e != 'rawlog' and rng.random() < 0.2]}
            if rng.random() < 0.5:
                c['fl'] = rng.choice(list(FL))
            V[lab(c)] = gen(c)
    print(len(V))
    F.run(V, 'q', show=32)
