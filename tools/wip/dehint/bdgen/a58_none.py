"""Attempt 58: lab_none (precheck and cold label off) with loadBl24 / defaultBl60 return types, two-call
and one-call (`||`) bodies.  python tools/wip/dehint/bdgen/a58lib.py tools/wip/dehint/bdgen/a58_none.py -o "-;lab_devgl;vol_fail;exp_pr" """
NONE = [('\tif ((uint32_t)xb.nFiles <= 1)\n\t\tgoto none;\n', ''), ('none: __attribute__((cold));\n\treturn 0;\n', '')]
B2 = '''	if (loadBaseFile(e->name, e))
		return defaultBl60(e);
	if (e->size != 0x60)
		return defaultBl60(e);
	return 0;
}'''
B1 = '''	if (loadBaseFile(e->name, e) || e->size != 0x60)
		return defaultBl60(e);
	return 0;
}'''
D = 'static int defaultBl60(struct fileent *e)\n'
L = 'static int loadBl24(struct fileent *e)\n'
V = {}
for body, bn in ((B2, 'two'), (B1, 'one')):
    for dt in ('int', 'uint32_t'):
        for lt in ('int', 'uint32_t'):
            for none in (0, 1):
                ed = [(B2, body)] if body != B2 else []
                if dt != 'int':
                    ed.append((D, 'static %s defaultBl60(struct fileent *e)\n' % dt))
                if lt != 'int':
                    ed.append((L, 'static %s loadBl24(struct fileent *e)\n' % lt))
                if none:
                    ed += NONE
                V['%s_d%s_l%s%s' % (bn, dt[0], lt[0], '_N' if none else '')] = ({}, ed)
