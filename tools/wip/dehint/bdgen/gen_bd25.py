# One small helper for the default copy (defaultBl60), the load tests written where they're used.
# Base: gen_bd23's "helper".
BASE = 'build/bd/gen_bd23_best.c'
HELPERS_OLD_START = '/* the 0x60-byte bootloader (type 24) from the base dir, else the default */\n'
OLDH = HELPERS_OLD_START + '''static int loadBl60(struct fileent *e)
{
	if (loadBaseFile(e->name, e) || e->size != 0x60) {
		e->data = malloc(0x60);
		if (!e->data)
			return 1;
		e->size = 0x60;
		memcpy(e->data, defBl60, 0x60);
	}
	return 0;
}

static int loadBl60b(struct fileent *e)
{
	if (loadBaseFile(e->name, e)) {
		e->data = malloc(0x60);
		if (!e->data)
			return 1;
		e->size = 0x60;
		memcpy(e->data, defBl60, 0x60);
	} else if (e->size != 0x60) {
		e->data = malloc(0x60);
		if (!e->data)
			return 1;
		e->size = 0x60;
		memcpy(e->data, defBl60, 0x60);
	}
	return 0;
}
'''
NEWH = '''/* the default 0x60-byte bootloader (type 24) */
static int defaultBl60(struct fileent *e)
{
	e->data = malloc(0x60);
	if (!e->data)
		return 1;
	e->size = 0x60;
	memcpy(e->data, defBl60, 0x60);
	return 0;
}
'''
A1O = '''		if (xb.type == BUILD_JTAG || xb.glitch2mfg)
			*pr = loadBl60b(e);
'''
A2O = '''		if (xb.type == BUILD_DEVGL || xb.type == BUILD_DEVGL16)
			*pr = loadBl60(e);
'''
A1 = [
    ('e', [(A1O, '''		if (xb.type == BUILD_JTAG || xb.glitch2mfg) {
			if (loadBaseFile(e->name, e))
				*pr = defaultBl60(e);
			else if (e->size != 0x60)
				*pr = defaultBl60(e);
		}
''')]),
    ('n', [(A1O, '''		if (xb.type == BUILD_JTAG || xb.glitch2mfg) {
			if (!loadBaseFile(e->name, e)) {
				if (e->size != 0x60)
					*pr = defaultBl60(e);
			} else
				*pr = defaultBl60(e);
		}
''')]),
]
A2 = [
    ('o', [(A2O, '''		if (xb.type == BUILD_DEVGL || xb.type == BUILD_DEVGL16) {
			if (loadBaseFile(e->name, e) || e->size != 0x60)
				*pr = defaultBl60(e);
		}
''')]),
    ('oz', [(A2O, '''		if (xb.type == BUILD_DEVGL || xb.type == BUILD_DEVGL16) {
			*pr = 0;
			if (loadBaseFile(e->name, e) || e->size != 0x60)
				*pr = defaultBl60(e);
		}
''')]),
    ('e', [(A2O, '''		if (xb.type == BUILD_DEVGL || xb.type == BUILD_DEVGL16) {
			if (loadBaseFile(e->name, e))
				*pr = defaultBl60(e);
			else if (e->size != 0x60)
				*pr = defaultBl60(e);
		}
''')]),
]
AXES = [[('', [(OLDH, NEWH)])], A1, A2]
