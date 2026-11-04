"""fl5f.py single|rand N seed [T]: helpers with out-parameters for the entry heads (loads and stores FRE/SRA only remove after inlining,
so the names freed fall after IPA), and for the crc blocks.  Axes per section; sample with subsets of the four tests."""
import itertools, random, sys
import fllib as L, fl5lib as F

BLH = ("\t\t\tcomma = memFindChar(p, ',', size - pos);\n\t\t\tnul = memFindChar(p, 0, size - pos);\n"
       "\t\t\tlen = comma;\n\t\t\tnoCrc = 0;\n\t\t\tif (comma > nul) {\n\t\t\t\tlen = nul;\n\t\t\t\tnoCrc = 1;\n\t\t\t}\n")
SECH = ("\t\t\tcomma = memFindChar(p, ',', size - pos);\n\t\t\tnul = memFindChar(p, 0, size - pos);\n"
        "\t\t\tif (comma > nul) {\n\t\t\t\tnoCrc = 1;\n\t\t\t\tlen = nul;\n\t\t\t} else {\n\t\t\t\tnoCrc = 0;\n\t\t\t\tlen = comma;\n\t\t\t}\n")
FLH = ("\t\t\tnul = memFindChar(p, 0, size - pos);\n\t\t\tcomma = memFindChar(p, ',', size - pos);\n"
       "\t\t\tnoCrc = 1;\n\t\t\tlen = nul;\n\t\t\tif (comma >= 0 && comma < nul) {\n\t\t\t\tlen = comma;\n\t\t\t\tnoCrc = 0;\n\t\t\t}\n")
RAWH = "\t\t\tnul = memFindChar(p, 0, size - pos);\n\t\t\tcomma = memFindChar(p, ',', size - pos);\n"
HEADS = {'bl': BLH, 'sec': SECH, 'flash': FLH}


def span(s, sec):
    a, b = F.MK[sec]
    return s.index(a), s.index(b)


def secsub(s, sec, old, new):
    i, j = span(s, sec)
    return s[:i] + L.sub(s[i:j], old, new) + s[j:]


def helper(s, name, text):
    if name + '(' in s[:s.index(F.HEAD)]:
        return s
    h = s.index(F.HEAD)
    return s[:h] + text + '\n' + s[h:]


# ----- entry head forms.  form name -> (helper name, helper text, per-section call text)
def body_of(sec):
    """the head as helper body statements, using p, rem"""
    return HEADS[sec].replace('size - pos', 'rem').replace('\t\t\t', '\t').replace('\t\t\t', '\t')


def head_edit(s, sec, form, tag):
    """tag makes a helper shared (same tag) or separate"""
    H = HEADS[sec]
    v = sec if tag is None else tag
    rem = 'size - pos'
    if form == 'cn':  # the two searches, out params
        order = H.split('\n')[:2]
        first = 'comma' if 'comma' in order[0] else 'nul'
        nm = 'findField_' + v
        b = '\t*comma = memFindChar(p, \',\', rem);\n\t*nul = memFindChar(p, 0, rem);\n' if first == 'comma' else '\t*nul = memFindChar(p, 0, rem);\n\t*comma = memFindChar(p, \',\', rem);\n'
        t = 'static void %s(unsigned char *p, int rem, int *comma, int *nul)\n{\n%s}\n' % (nm, b)
        s = helper(s, nm, t)
        rest = '\n'.join(H.split('\n')[2:])
        return secsub(s, sec, H, '\t\t\t%s(p, %s, &comma, &nul);\n%s' % (nm, rem, rest))
    if form == 'cr':  # returns one, the other out
        order = H.split('\n')[:2]
        nm = 'findField_' + v
        if 'comma' in order[0]:
            b = '\tint comma = memFindChar(p, \',\', rem);\n\n\t*nul = memFindChar(p, 0, rem);\n\treturn comma;\n'
            t = 'static int %s(unsigned char *p, int rem, int *nul)\n{\n%s}\n' % (nm, b)
        else:
            b = '\tint comma;\n\n\t*nul = memFindChar(p, 0, rem);\n\tcomma = memFindChar(p, \',\', rem);\n\treturn comma;\n'
            t = 'static int %s(unsigned char *p, int rem, int *nul)\n{\n%s}\n' % (nm, b)
        s = helper(s, nm, t)
        rest = '\n'.join(H.split('\n')[2:])
        return secsub(s, sec, H, '\t\t\tcomma = %s(p, %s, &nul);\n%s' % (nm, rem, rest))
    if form == 'ln':  # returns len, noCrc out
        nm = 'entryLen_' + v
        lines = H.split('\n')
        order = lines[:2]
        d = 'int comma, nul, len;\n'
        b = H.replace('size - pos', 'rem').replace('\t\t\t', '\t')
        b = b.replace('noCrc = ', '*noCrc = ')
        t = 'static int %s(unsigned char *p, int rem, uint32_t *noCrc)\n{\n\t%s\n%s\treturn len;\n}\n' % (nm, d, b)
        s = helper(s, nm, t)
        return secsub(s, sec, H, '\t\t\tlen = %s(p, %s, &noCrc);\n' % (nm, rem))
    if form == 'nl':  # returns noCrc, len out
        nm = 'entrySplit_' + v
        d = 'int comma, nul;\n\tuint32_t noCrc;\n'
        b = H.replace('size - pos', 'rem').replace('\t\t\t', '\t')
        b = b.replace('len = ', '*len = ')
        t = 'static uint32_t %s(unsigned char *p, int rem, int *len)\n{\n\t%s\n%s\treturn noCrc;\n}\n' % (nm, d, b)
        s = helper(s, nm, t)
        return secsub(s, sec, H, '\t\t\tnoCrc = %s(p, %s, &len);\n' % (nm, rem))
    if form == 'lv':  # returns len only, noCrc computed by the caller from comma? (len != comma needs comma): returns len with sign
        nm = 'entryNameLen_' + v
        d = 'int comma, nul;\n\tuint32_t noCrc;\n\tint len;\n'
        b = H.replace('size - pos', 'rem').replace('\t\t\t', '\t')
        t = 'static int %s(unsigned char *p, int rem, uint32_t *pn)\n{\n\t%s\n%s\t*pn = noCrc;\n\treturn len;\n}\n' % (nm, d, b)
        s = helper(s, nm, t)
        return secsub(s, sec, H, '\t\t\tlen = %s(p, %s, &noCrc);\n' % (nm, rem))
    raise ValueError(form)


def raw_edit(s, form):
    nm = 'findField_raw'
    if form == 'cn':
        t = 'static void %s(unsigned char *p, int rem, int *comma, int *nul)\n{\n\t*nul = memFindChar(p, 0, rem);\n\t*comma = memFindChar(p, \',\', rem);\n}\n' % nm
        s = helper(s, nm, t)
        return secsub(s, 'raw', RAWH, '\t\t\t%s(p, size - pos, &comma, &nul);\n' % nm)
    t = 'static int %s(unsigned char *p, int rem, int *nul)\n{\n\t*nul = memFindChar(p, 0, rem);\n\treturn memFindChar(p, \',\', rem);\n}\n' % nm
    s = helper(s, nm, t)
    return secsub(s, 'raw', RAWH, '\t\t\tcomma = %s(p, size - pos, &nul);\n' % nm)


# ----- crc blocks, helper with out params
CRC = {
    'bl': ('''			if (!noCrc) {
				n = memFindChar(&buf[pos], 0, size - pos);
				if (n == 0)
					xb.files[blOrder[i]].crc = 0;
				else if (n != 8) {
					log_printf(0, "\\n******* ERROR: crc data for file '%s' in ini is incorrect size!\\n", xb.files[blOrder[i]].name);
					free(buf);
					return 0;
				} else {
					strncpy(tmp, (char *)&buf[pos], 8);
					tmp[8] = 0;
					xb.files[blOrder[i]].crc = myatox32(tmp, 0);
				}
				pos = pos + n + 1;
			} else
''', 'xb.files[blOrder[i]].crc', 'xb.files[blOrder[i]].name'),
    'sec': ('''				if (!noCrc) {
					n = memFindChar(&buf[pos], 0, size - pos);
					if (n == 0)
						xb.flashCrc[i] = 0;
					else if (n != 8) {
						/* sic: names the [flashfs] file */
						log_printf(0, "\\n******* ERROR: crc data for file '%s' in ini is incorrect size!\\n", xb.firmware[i]);
						free(buf);
						return 0;
					} else {
						strncpy(tmp, (char *)&buf[pos], 8);
						tmp[8] = 0;
						xb.flashCrc[i] = myatox32(tmp, 0);
					}
					pos = pos + n + 1;
				} else
''', 'xb.flashCrc[i]', 'xb.firmware[i]'),
    'flash': ('''				if (!noCrc) {
					n = memFindChar(&buf[pos], 0, size - pos);
					if (n == 0)
						crc = xb.firmwareCrc[i] = 0;
					else if (n != 8) {
						log_printf(0, "\\n******* ERROR: crc data for file '%s' in ini is incorrect size!\\n", xb.firmware[i]);
						free(buf);
						return 0;
					} else {
						strncpy(tmp, (char *)&buf[pos], 8);
						tmp[8] = 0;
						crc = xb.firmwareCrc[i] = myatox32(tmp, 0);
					}
					pos = pos + n + 1;
				} else
''', 'crc = xb.firmwareCrc[i]', 'xb.firmware[i]'),
}


def crc_edit(s, sec, form):
    """p: helper parses into *crc (slot pointer) and returns the field's length, -1 on error; caller frees"""
    old, lv, nm_ = CRC[sec]
    ind = '\t\t\t' if sec == 'bl' else '\t\t\t\t'
    nm = 'readCrc_' + sec
    if form == 'slot':
        slot = lv.replace('crc = ', '')
        t = ('static int %s(unsigned char *p, int rem, char *tmp, uint32_t *crc, const char *name)\n{\n\tint n = memFindChar(p, 0, rem);\n\n\tif (n == 0)\n\t\t*crc = 0;\n'
             '\telse if (n != 8) {\n\t\tlog_printf(0, "\\n******* ERROR: crc data for file \'%%s\' in ini is incorrect size!\\n", name);\n\t\treturn -1;\n\t} else {\n'
             '\t\tstrncpy(tmp, (char *)p, 8);\n\t\ttmp[8] = 0;\n\t\t*crc = myatox32(tmp, 0);\n\t}\n\treturn n;\n}\n') % nm
        s = helper(s, nm, t)
        new = '%sif (!noCrc) {\n%s\tn = %s(&buf[pos], size - pos, tmp, &%s, %s);\n%s\tif (n < 0) {\n%s\t\tfree(buf);\n%s\t\treturn 0;\n%s\t}\n' % (ind, ind, nm, slot, nm_, ind, ind, ind, ind)
        if sec == 'flash':
            new += '%s\tcrc = xb.firmwareCrc[i];\n' % ind
        new += '%s\tpos = pos + n + 1;\n%s} else\n' % (ind, ind)
        return secsub(s, sec, old, new)
    raise ValueError(form)


AX = {}
for sec in ('bl', 'sec', 'flash'):
    AX['h' + sec] = ['cn', 'cr', 'ln', 'nl', 'lv']
    AX['c' + sec] = ['slot']
AX['hraw'] = ['cn', 'cr']
AX['shared'] = ['y']


def gen(c, t):
    s = F.gen(t)
    shared = 'shared' in c
    for sec in ('bl', 'sec', 'flash'):
        k = 'h' + sec
        if k in c:
            tag = 'blsec' if shared and sec in ('bl', 'sec') and c.get('hbl') == c.get('hsec') and c[k] in ('cn', 'cr') else None
            s = head_edit(s, sec, c[k], tag)
        k = 'c' + sec
        if k in c:
            s = crc_edit(s, sec, c[k])
    if 'hraw' in c:
        s = raw_edit(s, c['hraw'])
    return s


def lab(c, t):
    return ','.join('%s=%s' % (a, c[a]) for a in sorted(c)) + '|' + '+'.join(t)


TN = ['raw', 'off3', 'off4', 'x']
if __name__ == '__main__':
    V = {}
    if sys.argv[1] == 'single':
        subs = [c for r in range(0, 5) for c in itertools.combinations(TN, r) if len(c) < 4]
        for t in subs:
            for a in AX:
                if a == 'shared':
                    continue
                for v in AX[a]:
                    V[lab({a: v}, t)] = gen({a: v}, t)
    else:
        N, seed = int(sys.argv[2]), int(sys.argv[3])
        fixed = sys.argv[4].split(',') if len(sys.argv) > 4 else None
        rng = random.Random(seed)
        keys = list(AX)
        while len(V) < N:
            c = {}
            for a in rng.sample(keys, rng.choice((2, 2, 3, 3, 4))):
                c[a] = rng.choice(AX[a])
            t = tuple(fixed) if fixed is not None else tuple(x for x in TN if rng.random() < .4)
            V[lab(c, t)] = gen(c, t)
    print(len(V))
    F.run(V, 'f', show=25)
