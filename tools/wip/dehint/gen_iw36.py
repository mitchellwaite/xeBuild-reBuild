# attempt 3: lnp2's hot label gone with a guard probability >= .78: `partial <= 0` (PRED_TREE_OPCODE_POSITIVE) and a goto in the arm (PRED_GOTO).
ALL = '''		if (len % 512)
			npages = (len + 512) / 512;
		else
			npages = len / 512;
		if (!partial)
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
AXES = [[
 ('F', [(ALL, '		if (partial <= 0) {\n			npages = 32;\n			goto np;\n		}\n' + NP + '	np:\n')]),
 ('Fne', [(ALL, '		if (!partial) {\n			npages = 32;\n			goto np;\n		}\n' + NP + '	np:\n')]),
 ('Fg', [(ALL, NP + '		if (partial <= 0) {\n			npages = 32;\n			goto np;\n		}\n	np:\n')]),
 ('Fh', [(ALL, '		npages = 32;\n		if (partial <= 0)\n			goto np;\n' + NP + '	np:\n')]),
 ('Fi', [(ALL, '		npages = 32;\n		if (!partial)\n			goto np;\n' + NP + '	np:\n')]),
 ('Fj', [(ALL, NP + '		if (partial > 0)\n			goto np;\n		npages = 32;\n	np:\n')]),
 ('Fk', [(ALL, '		if (partial > 0)\n			goto np;\n		npages = 32;\n		goto nd;\n	np:\n' + NP + '	nd:\n')]),
]]
