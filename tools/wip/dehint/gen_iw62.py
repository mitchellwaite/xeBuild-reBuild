# attempt 4: imgAddFile: the dead test before the fits test with one condition and a body that doesn't touch len (end++ / lim--), so FRE3 still merges off + len and ifcombine fires
import os
BASE = os.environ.get('IWB', 'build/iw/a4/a6.c')
HEAD = '''	uint32_t lim = (xb.fsEnd - 1) * 0x4000;
	uint32_t end = off + len;

	if (end < off && (len & 0x3fff) > 0x3fff)
		len++;
	if (__builtin_expect(lim >= off + len, 1)) {
'''
AB = '		if ((end & 0x3fff) > 0x3fff)\n			abort();\n'
LIM = '	uint32_t lim = (xb.fsEnd - 1) * 0x4000;\n'
ax = []
for cn, c in (('L', '(len & 0x3fff) > 0x3fff'), ('E', '(end & 0x3fff) > 0x3fff'), ('O', '(off & 0x3fff) > 0x3fff'), ('T', 'len > ~0u - 0') ):
    if cn == 'T':
        continue
    for bn, b in (('e', 'end++;'), ('E', 'end--;'), ('l', 'lim++;'), ('L', 'lim--;'), ('o', 'off++;'), ('n', 'len++;')):
        for tn, t in (('t', 'lim >= end'), ('T', 'lim >= off + len'), ('u', 'end <= lim')):
            ax.append((f'{cn}{bn}{tn}', [(HEAD, LIM + f'	uint32_t end = off + len;\n\n	if ({c})\n		{b}\n	if (__builtin_expect({t}, 1)) {{\n')]))
AXES = [
 ax,
 [('', []),
  ('A', [(AB, '		if ((len & 0x3fff) > 0x3fff)\n			abort();\n')]),
  ('B', [(AB, '		if ((off & 0x3fff) > 0x3fff)\n			abort();\n')])],
]
