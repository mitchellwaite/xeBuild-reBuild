# attempt 4: imgAddFile with no dead len++ at all: VRP1 then threads head -> fits -> abort test and renumbers the head high (3 compares flip).  Move the abort test / other conditions.
import os
BASE = os.environ.get('IWB', 'build/iw/a4/a6.c')
HEAD = '''	uint32_t lim = (xb.fsEnd - 1) * 0x4000;
	uint32_t end = off + len;

	if (end < off && (len & 0x3fff) > 0x3fff)
		len++;
	if (__builtin_expect(lim >= off + len, 1)) {
'''
AB = '		if ((len & 0x3fff) > 0x3fff)\n			abort();\n'
BLOCK = '		fsFiles[nFsFiles].block = SWAP16_IMAGE_WRITE((uint16_t)(off >> 14) - xb.fsStart);\n'
SIZE = '		fsFiles[nFsFiles].size = SWAP32_IMAGE_WRITE(len);\n'
CPY = '		strcpy(fsFiles[nFsFiles].name, name);\n'
TIME = '		fsFiles[nFsFiles].time = *time;\n'
ADDB = '		if (!xb.bigBlock)\n			imgAdd(off, data, len, 0, 0xffff, 1);\n'
NF = '		nFsFiles++;\n'
LIM = '	uint32_t lim = (xb.fsEnd - 1) * 0x4000;\n'
H = {
 'F0': LIM + '	uint32_t end = off + len;\n\n	if (__builtin_expect(lim >= off + len, 1)) {\n',
 'F1': LIM + '	uint32_t end = off + len;\n\n	if (__builtin_expect(lim >= end, 1)) {\n',
 'G0': LIM + '\n	if (__builtin_expect(lim >= off + len, 1)) {\n',
 'G1': '\n	if (__builtin_expect((xb.fsEnd - 1) * 0x4000 >= off + len, 1)) {\n',
}
CONDS = {'l': '(len & 0x3fff) > 0x3fff', 'o': '(off & 0x3fff) > 0x3fff', 'u': '(off & 0x3fff) != 0'}
POS = {'b': BLOCK, 's': SIZE, 'c': CPY, 't': TIME, 'a': ADDB, 'n': NF}
ax = []
for hn, h in H.items():
    for cn, c in CONDS.items():
        if cn == 'u' and False:
            continue
        for pn, p in POS.items():
            ed = [(HEAD, h), (AB, '')]
            ed.append((p, f'		if ({c})\n			abort();\n' + p))
            ax.append((f'{hn}{cn}{pn}', ed))
            if 'end' in h:
                ax.append((f'{hn}e{cn}{pn}', [(HEAD, h), (AB, ''), (p, f'		if ((end & 0x3fff) > 0x3fff)\n			abort();\n' + p)]))
AXES = [ax]
