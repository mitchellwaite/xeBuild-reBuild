"""Attempt 59: defaultBl60's copy as memmove, lab_none (precheck + cold label) off; crossed with hint sets.
python tools/wip/dehint/bdgen/a58lib.py tools/wip/dehint/bdgen/a59_mm.py -o "-;exp_pr;vol_fail;lab_devgl;exp_devgl" """
NONE = [('\tif ((uint32_t)xb.nFiles <= 1)\n\t\tgoto none;\n', ''), ('none: __attribute__((cold));\n\treturn 0;\n', '')]
MM = [('\tmemcpy(e->data, defBl60, 0x60);\n', '\tmemmove(e->data, defBl60, 0x60);\n')]
NL = [('	/* the cold label gives the shrink-wrapped return 0 frequency 0, so\n	   bb-reorder lays it out last */\n', '')]
B1 = [('''	if (loadBaseFile(e->name, e))
		return defaultBl60(e);
	if (e->size != 0x60)
		return defaultBl60(e);
	return 0;
}''', '''	if (loadBaseFile(e->name, e) || e->size != 0x60)
		return defaultBl60(e);
	return 0;
}''')]
A2 = [('''					r = 0;
					if (loadBaseFile(e->name, e))
						r = defaultBl60(e);
					else if (e->size != 0x60)
						r = defaultBl60(e);
''', '''					r = loadBl24(e);
''')]
V = {
    'mm_N': ({}, MM + NONE + NL),
    'mm_N_one': ({}, MM + NONE + NL + B1),
    'mm_N_a2': ({}, MM + NONE + NL + A2),
    'mm_N_one_a2': ({}, MM + NONE + NL + B1 + A2),
}
MM3 = [('\t\t\t\tmemcpy(e->data, defPayload, 0x200);\n', '\t\t\t\tmemmove(e->data, defPayload, 0x200);\n'),
       ('\t\t\t\tmemcpy(e->data, defCore, 0xd40);\n', '\t\t\t\tmemmove(e->data, defCore, 0xd40);\n')]
V['mm_N_all'] = ({}, MM + NONE + NL + MM3)
V['mm_keepN'] = ({}, MM)
