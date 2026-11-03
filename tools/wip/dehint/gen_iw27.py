# attempt 2, on drafts/image_write.c: hot label lnp2 gone, forms of the npages computation (PRED_GOTO, moved into the arm)
BASE = 'tools/wip/dehint/drafts/image_write.c'
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
NP = '''if (len % 512)
				npages = (len + 512) / 512;
			else
				npages = len / 512;
'''
AXES = [[
 ('', []),
 ('A', [(ALL, '		if (partial) {\n			' + NP + '		} else\n			npages = 32;\n')]),
 ('A2', [(ALL, '		if (!partial)\n			npages = 32;\n		else {\n			' + NP + '		}\n')]),
 ('B', [(ALL, '		npages = 32;\n		if (partial) {\n			' + NP + '		}\n')]),
 ('C', [(ALL, '		npages = partial ? (len % 512 ? (len + 512) / 512 : len / 512) : 32;\n')]),
 ('C2', [(ALL, '		npages = !partial ? 32 : len % 512 ? (len + 512) / 512 : len / 512;\n')]),
 ('C3', [(ALL, '		npages = len % 512 ? (len + 512) / 512 : len / 512;\n		if (!partial)\n			npages = 32;\n')]),
 ('C4', [(ALL, '		npages = (len + 511) / 512;\n		if (!partial)\n			npages = 32;\n')]),
 ('C5', [(ALL, '		npages = partial ? (len + 511) / 512 : 32;\n')]),
 ('D', [(ALL, '		if (!partial)\n			npages = 32;\n		else if (len % 512)\n			npages = (len + 512) / 512;\n		else\n			npages = len / 512;\n')]),
 ('F', [(ALL, '		if (!partial) {\n			npages = 32;\n			goto np;\n		}\n		if (len % 512)\n			npages = (len + 512) / 512;\n		else\n			npages = len / 512;\n	np:\n')]),
 ('F2', [(ALL, '		if (partial)\n			goto np;\n		npages = 32;\n		goto nd;\n	np:\n		if (len % 512)\n			npages = (len + 512) / 512;\n		else\n			npages = len / 512;\n	nd:\n')]),
 ('F3', [(ALL, '		if (len % 512)\n			npages = (len + 512) / 512;\n		else\n			npages = len / 512;\n		if (partial)\n			goto np;\n		npages = 32;\n	np:\n')]),
 ('F4', [(ALL, '		if (len % 512)\n			npages = (len + 512) / 512;\n		else\n			npages = len / 512;\n		if (!partial) {\n			npages = 32;\n			goto np;\n		}\n	np:\n')]),
]]
