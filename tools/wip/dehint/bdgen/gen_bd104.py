"""loadConsoleBlFiles, plain for: forms of case 24 that raise the r = 1 block over the return's 20."""
OLD = '''				if (!xb.glitch2mfg)
					break;
				if (loadBaseFile(e->name, e))
					r = defaultBl60(e);
				else if (e->size != 0x60)
					r = defaultBl60(e);
				break;
'''
F = {
 'keep': OLD,
 'nest': '''				if (xb.glitch2mfg) {
					if (loadBaseFile(e->name, e))
						r = defaultBl60(e);
					else if (e->size != 0x60)
						r = defaultBl60(e);
				}
				break;
''',
 'rev': '''				if (!xb.glitch2mfg)
					break;
				if (!loadBaseFile(e->name, e)) {
					if (e->size == 0x60)
						break;
					r = defaultBl60(e);
				} else
					r = defaultBl60(e);
				break;
''',
 'rev2': '''				if (!xb.glitch2mfg)
					break;
				if (!loadBaseFile(e->name, e) && e->size == 0x60)
					break;
				r = defaultBl60(e);
				break;
''',
 'or': '''				if (!xb.glitch2mfg)
					break;
				if (loadBaseFile(e->name, e) || e->size != 0x60)
					r = defaultBl60(e);
				break;
''',
 'gl': '''				if (xb.glitch2mfg && (loadBaseFile(e->name, e) || e->size != 0x60))
					r = defaultBl60(e);
				break;
''',
 'cont': '''				if (xb.glitch2mfg) {
					if (loadBaseFile(e->name, e)) {
						r = defaultBl60(e);
						break;
					}
					if (e->size != 0x60)
						r = defaultBl60(e);
				}
				break;
''',
}
PLAIN = ('''	/* the cold label gives the shrink-wrapped return 0 frequency 0, so
	   bb-reorder lays it out last */
	if ((uint32_t)xb.nFiles <= 1)
		goto none;
''', '''none: __attribute__((cold));
	return 0;
''')
D60 = '''	e->data = malloc(0x60);
	if (!e->data)
		return 1;
	e->size = 0x60;
	memcpy(e->data, defBl60, 0x60);
	return 0;
'''
def CASES(base):
    base = base.replace(PLAIN[0], '').replace(PLAIN[1], '')
    out = []
    for k, v in F.items():
        out.append((k, base.replace(OLD, v)))
    return out
