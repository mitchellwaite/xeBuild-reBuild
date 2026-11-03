# attempt 4: on drafts/image_write_a4.c (14 tricks, identical): subsets of what's left
import os
BASE = os.environ.get('IWB', 'tools/wip/dehint/drafts/image_write_a4.c')
OPT = '__attribute__((optimize("no-tree-scev-cprop"))) void writeFsTable'
LEN = '	if (end < off && (len & 0x3fff) > 0x3fff)\n		len++;\n'
LNP = '''		if (!partial)
			npages = 32;
		else {
			/* imgAddFile's clone: keeps DOM2's threading from zeroing the npages guard edge */
			lnp2: __attribute__((hot));
		}
'''
AXES = [
 [('', []), ('C4', [('		if ((len & 0x3fff) > 0x3fff)\n			blocks++;\n', '')])],
 [('', []), ('LEN', [(LEN, '')]), ('LENp', [(LEN, '	if ((len & 0x3fff) > 0x3fff)\n		len++;\n')]), ('LENe', [(LEN, '	if (end < off)\n		len++;\n')]), ('LENE', [(LEN, '	if ((end & 0x3fff) > 0x3fff)\n		len++;\n')])],
 [('', []), ('AB', [('		if ((end & 0x3fff) > 0x3fff)\n			abort();\n', '')])],
 [('', []), ('noopt', [(OPT, 'void writeFsTable')])],
 [('', []), ('nopt', [('			__asm__("" :: "g"(t));\n', '')])],
 [('', []), ('lnp', [(LNP, '		if (partial <= 0)\n			npages = 32;\n')])],
]
