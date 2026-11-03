# attempt 2, on drafts/image_write.c: hot label lnp2 gone; opcode predictors on the partial test (PRED_TREE_OPCODE_POSITIVE...)
BASE = 'tools/wip/dehint/drafts/image_write.c'
LNP = '''		if (!partial)
			npages = 32;
		else {
			/* imgAddFile's clone: keeps DOM2's threading from zeroing the npages guard edge */
			lnp2: __attribute__((hot));
		}
'''
def v(c):
    return [(LNP, '		if (%s)\n			npages = 32;\n' % c)]
P = "		partial = type != 0 && type != '0' && len < 0x4000;\n"
AXES = [[
 ('le', v('partial <= 0')), ('lt', v('partial < 1')), ('ne1', v('partial != 1')), ('eq0', v('partial == 0')),
 ('gt', [(LNP, '		if (partial > 0) {\n		} else\n			npages = 32;\n')]),
 ('ge', [(LNP, '		if (partial >= 1) {\n		} else\n			npages = 32;\n')]),
 ('eq1', [(LNP, '		if (partial == 1) {\n		} else\n			npages = 32;\n')]),
 ('lenp', [(LNP, '		if (!partial || len >= 0x4000)\n			npages = 32;\n')]),
 ('lenp2', [(LNP, '		if (len >= 0x4000 || !partial)\n			npages = 32;\n')]),
 ('inl', [(LNP, "		if (type == 0 || type == '0' || len >= 0x4000)\n			npages = 32;\n"), (P, '')]),
 ('inl2', [(LNP, "		if (len >= 0x4000 || type == 0 || type == '0')\n			npages = 32;\n"), (P, '')]),
], [('', []),
 ('i', [('	int partial;\n', '	unsigned partial;\n')]),
]]
