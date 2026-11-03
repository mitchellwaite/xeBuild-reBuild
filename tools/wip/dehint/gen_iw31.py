# attempt 2, on drafts/image_write.c: hot label lnp2 gone with `partial <= 0` (73%): 12 lines, two slots swap in imgAddFile
# because the guard block's frequency is 900*(2p-1): 414 vs 630.  Forms that raise p or lower the other slot (end).
BASE = 'tools/wip/dehint/drafts/image_write.c'
LNP = '''		if (!partial)
			npages = 32;
		else {
			/* imgAddFile's clone: keeps DOM2's threading from zeroing the npages guard edge */
			lnp2: __attribute__((hot));
		}
'''
NP = '''		if (len % 512)
			npages = (len + 512) / 512;
		else
			npages = len / 512;
'''
PAD = '	if (pad == 1) if (tail)\n'
AXES = [[
 ('le', [(LNP, '		if (partial <= 0)\n			npages = 32;\n')]),
 ('gt', [(LNP, '		if (partial > 0) {\n		} else\n			npages = 32;\n')]),
 ('n2', [(NP + LNP, '		if (partial > 0) {\n			if (len % 512)\n				npages = (len + 512) / 512;\n			else\n				npages = len / 512;\n		}\n		if (partial <= 0)\n			npages = 32;\n')]),
 ('n3', [(NP + LNP, '		if (partial <= 0)\n			npages = 32;\n		if (partial > 0) {\n			if (len % 512)\n				npages = (len + 512) / 512;\n			else\n				npages = len / 512;\n		}\n')]),
 ('n4', [(NP + LNP, '		if (partial > 0) {\n			if (len % 512)\n				npages = (len + 512) / 512;\n			else\n				npages = len / 512;\n		} else\n			npages = 32;\n')]),
 ('n5', [(LNP, '		if (partial <= 0)\n			npages = 32;\n		if (partial > 0)\n			npages = npages;\n')]),
 ('n6', [(LNP, '		if (partial <= 0)\n			npages = 32;\n		else if (partial <= 0)\n			npages = 32;\n')]),
 ('n7', [(LNP, '		if (partial <= 0 || !partial)\n			npages = 32;\n')]),
 ('n8', [(LNP, '		if (partial < 1 || partial <= 0)\n			npages = 32;\n')]),
], [('', []),
 ('p1', [(PAD, '	if (pad == 1 && tail)\n')]),
 ('p2', [(PAD, '	if (tail && pad == 1)\n')]),
 ('p3', [(PAD, '	if (tail > 0) if (pad == 1)\n')]),
 ('p4', [(PAD, '	if (pad > 0) if (tail)\n')]),
 ('p5', [(PAD, '	if (pad == 1) if (tail > 0)\n')]),
]]
