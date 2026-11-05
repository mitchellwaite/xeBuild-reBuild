"""loadBl case 27, pin_d off: where a helper starts and ends; the load fallbacks as a function, the extract as a function; size read first, or a pointer."""
import itertools
OLD = '''		if (loadBaseFile(e->name, &xb.files[xb.nFlashFiles]) &&
		    loadBaseFile("config.bin", &xb.files[xb.nFlashFiles]) &&
		    (*pr = loadBaseFile("config_raw.bin", &xb.files[xb.nFlashFiles]))) {
			if (!xb.smcConfig.data)
				break;
			log_printf(1, "reading %s%s failed, using %s from nand dump\\n", xb.baseDir, e->name, e->name);
			if (xb.files[xb.nFlashFiles].data)
				free(xb.files[xb.nFlashFiles].data);
			xb.files[xb.nFlashFiles].data = xb.smcConfig.data;
			xb.smcConfig.data = NULL;
			xb.files[xb.nFlashFiles].size = xb.smcConfig.size;
			xb.smcConfig.size = 0;
			*pr = 0;
		}
		{
			uint8_t *d = xb.files[xb.nFlashFiles].data;

			__asm__("" : "+a"(d));
			if (d)
				*pr = extractSmcConfig(e, d, xb.files[xb.nFlashFiles].size);
		}
		break;
'''
LOAD = OLD[:OLD.index('		{\n			uint8_t *d')]
EX = {
    'd': '''		{
			uint8_t *d = xb.files[xb.nFlashFiles].data;

			if (d)
				*pr = extractSmcConfig(e, d, xb.files[xb.nFlashFiles].size);
		}
		break;
''',
    'plain': '''		if (xb.files[xb.nFlashFiles].data)
			*pr = extractSmcConfig(e, xb.files[xb.nFlashFiles].data, xb.files[xb.nFlashFiles].size);
		break;
''',
    'ptr': '''		{
			struct fileent *c = &xb.files[xb.nFlashFiles];

			if (c->data)
				*pr = extractSmcConfig(e, c->data, c->size);
		}
		break;
''',
    'ptr2': '''		{
			struct fileent *c = &xb.files[xb.nFlashFiles];
			uint8_t *d = c->data;

			if (d)
				*pr = extractSmcConfig(e, d, c->size);
		}
		break;
''',
    'sz': '''		{
			uint8_t *d = xb.files[xb.nFlashFiles].data;

			if (d) {
				uint32_t n = xb.files[xb.nFlashFiles].size;

				*pr = extractSmcConfig(e, d, n);
			}
		}
		break;
''',
    'i': '''		{
			int n = xb.nFlashFiles;
			uint8_t *d = xb.files[n].data;

			if (d)
				*pr = extractSmcConfig(e, d, xb.files[n].size);
		}
		break;
''',
    'helper': '''		extractLoadedConfig(e, pr);
		break;
''',
    'helper2': '''		if (extractLoadedConfig2(e))
			*pr = extractLoadedConfig3(e);
		break;
''',
}
H = '''static void extractLoadedConfig(struct fileent *e, uint32_t *pr)
{
	struct fileent *c = &xb.files[xb.nFlashFiles];

	if (c->data)
		*pr = extractSmcConfig(e, c->data, c->size);
}

static void extractLoadedConfigB(struct fileent *e, uint32_t *pr)
{
	uint8_t *d = xb.files[xb.nFlashFiles].data;

	if (d)
		*pr = extractSmcConfig(e, d, xb.files[xb.nFlashFiles].size);
}

'''
ANCHOR = '/* load the input file e (xb.files[i]) by its type */\n'
LD = {
    'keep': LOAD,
    'nest': '''		if (loadBaseFile(e->name, &xb.files[xb.nFlashFiles])) {
			if (loadBaseFile("config.bin", &xb.files[xb.nFlashFiles])) {
				*pr = loadBaseFile("config_raw.bin", &xb.files[xb.nFlashFiles]);
				if (*pr) {
					if (!xb.smcConfig.data)
						break;
					log_printf(1, "reading %s%s failed, using %s from nand dump\\n", xb.baseDir, e->name, e->name);
					if (xb.files[xb.nFlashFiles].data)
						free(xb.files[xb.nFlashFiles].data);
					xb.files[xb.nFlashFiles].data = xb.smcConfig.data;
					xb.smcConfig.data = NULL;
					xb.files[xb.nFlashFiles].size = xb.smcConfig.size;
					xb.smcConfig.size = 0;
					*pr = 0;
				}
			}
		}
''',
}


def CASES(base):
    if OLD not in base:
        raise ValueError('old')
    out = []
    for (a, la), (b, ex) in itertools.product(LD.items(), EX.items()):
        if b == 'helper2':
            continue
        t = base.replace(OLD, la + ex)
        if b == 'helper':
            t = t.replace(ANCHOR, H + ANCHOR)
            out.append((a + ' helperB', t.replace('extractLoadedConfig(e, pr);', 'extractLoadedConfigB(e, pr);').replace(H, H[H.index('static void extractLoadedConfigB'):])))
            t = t.replace(H, H[:H.index('static void extractLoadedConfigB')])
        out.append((a + ' ' + b, t))
    return out
