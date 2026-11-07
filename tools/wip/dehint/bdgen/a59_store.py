"""Attempt 59: lab_none's one-call loadBl24 residue (the size store's place) by defaultBl60's types and
copy forms.  python tools/wip/dehint/bdgen/a58lib.py tools/wip/dehint/bdgen/a59_store.py -o "-;lab_none" """
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
D0 = '''	e->data = malloc(0x60);
	if (!e->data)
		return 1;
	e->size = 0x60;
	memcpy(e->data, defBl60, 0x60);
	return 0;
}'''
DV = {
    'src': D0,
    'loc': '''	uint8_t *p = malloc(0x60);

	e->data = p;
	if (!p)
		return 1;
	e->size = 0x60;
	memcpy(p, defBl60, 0x60);
	return 0;
}''',
    'cpy_sz': '''	e->data = malloc(0x60);
	if (!e->data)
		return 1;
	e->size = 0x60;
	memcpy(e->data, defBl60, e->size);
	return 0;
}''',
    'sizeof': '''	e->data = malloc(sizeof(defBl60));
	if (!e->data)
		return 1;
	e->size = sizeof(defBl60);
	memcpy(e->data, defBl60, sizeof(defBl60));
	return 0;
}''',
    'loop': '''	int i;

	e->data = malloc(0x60);
	if (!e->data)
		return 1;
	e->size = 0x60;
	for (i = 0; i < 0x60; i++)
		e->data[i] = defBl60[i];
	return 0;
}''',
    'cast_char': '''	e->data = malloc(0x60);
	if (!e->data)
		return 1;
	e->size = 0x60;
	memcpy((char *)e->data, defBl60, 0x60);
	return 0;
}''',
    'memmove': '''	e->data = malloc(0x60);
	if (!e->data)
		return 1;
	e->size = 0x60;
	memmove(e->data, defBl60, 0x60);
	return 0;
}''',
    'setfd': '''	return setFileData(e, defBl60, 0x60);
}''',
}
V = {}
for bn, body in (('two', B2), ('one', B1)):
    for dn, d in DV.items():
        ed = []
        if body != B2:
            ed.append((B2, body))
        if d != D0:
            ed.append((D0, d))
        V['%s_%s' % (bn, dn)] = ({}, ed)
        V['%s_%s_N' % (bn, dn)] = ({}, ed + NONE)
