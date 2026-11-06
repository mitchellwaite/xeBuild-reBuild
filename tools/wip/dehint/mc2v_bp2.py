# clientBinPatch without the edi/count hints: natural options alone and in pairs
import itertools, os, runpy
V0 = runpy.run_path(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'mc2v_bp.py'))['V']
B = V0['none']
SW = '''					switch (cinfo->nandSize) {
					default:
						patchNand(nand, rem, data, len);
						break;
					case 0x3000000:
						memcpy(nand + rem, data, len);
					}
'''
OPTS = {
    'sw_swap': [(SW, '''					switch (cinfo->nandSize) {
					case 0x3000000:
						memcpy(nand + rem, data, len);
						break;
					default:
						patchNand(nand, rem, data, len);
					}
''')],
    'sw_if': [(SW, '''					if (cinfo->nandSize == 0x3000000)
						memcpy(nand + rem, data, len);
					else
						patchNand(nand, rem, data, len);
''')],
    'sw_ifn': [(SW, '''					if (cinfo->nandSize != 0x3000000)
						patchNand(nand, rem, data, len);
					else
						memcpy(nand + rem, data, len);
''')],
    'sw_brk': [(SW, SW.replace('len);\n\t\t\t\t\t}', 'len);\n\t\t\t\t\t\tbreak;\n\t\t\t\t\t}'))],
    'decl_split': [('	uint32_t off, rem, start, count;\n', '	uint32_t off, rem;\n	uint32_t start, count;\n')],
    'decl_int': [('	uint32_t off, rem, start, count;\n', '	uint32_t off, rem;\n	int start, count;\n')],
    'rlen_u': [('	int rlen;\n', '	uint32_t rlen;\n')],
    'data_nc': [('	const uint8_t *data;\n', '	uint8_t *data;\n')],
    'nand_c': [('	if (nand && rlen) {', '	if (nand != NULL && rlen != 0) {')],
    'len_int': [('patchNand(nand, rem, data, len);', 'patchNand(nand, rem, data, (int)len);')],
    'rem_int': [('patchNand(nand, rem, data, len);', 'patchNand(nand, (int)rem, data, (int)len);')],
    'cnt_order': [('''				start = rem / bs;
				count = (len + rem) / bs;''', '''				count = (len + rem) / bs;
				start = rem / bs;''')],
    'cnt_inc': [('''				if ((len + rem) % bs)
					count++;''', '''				if ((len + rem) % bs != 0)
					count += 1;''')],
}
V = {}
keys = list(OPTS)
for n in (1, 2):
    for c in itertools.combinations(keys, n):
        if sum(k.startswith('sw_') for k in c) > 1 or ('decl_split' in c and 'decl_int' in c) or ('len_int' in c and 'rem_int' in c):
            continue
        V['+'.join(c)] = B + sum((OPTS[k] for k in c), [])
