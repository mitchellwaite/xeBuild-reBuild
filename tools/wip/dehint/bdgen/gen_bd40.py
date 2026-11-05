# loadBl's case 27 without the "+a" pin on d: spellings of the last test and call.
FOCUS = ['_loadBlFiles']
OLD = '''		{
			uint8_t *d = xb.files[xb.nFlashFiles].data;

			__asm__("" : "+a"(d));
			if (d)
				*pr = extractSmcConfig(e, d, xb.files[xb.nFlashFiles].size);
		}
'''
AXES = [[
    ('plain', [(OLD, '''		if (xb.files[xb.nFlashFiles].data)
			*pr = extractSmcConfig(e, xb.files[xb.nFlashFiles].data, xb.files[xb.nFlashFiles].size);
''')]),
    ('f', [(OLD, '''		{
			struct fileent *f = &xb.files[xb.nFlashFiles];

			if (f->data)
				*pr = extractSmcConfig(e, f->data, f->size);
		}
''')]),
    ('fd', [(OLD, '''		{
			struct fileent *f = &xb.files[xb.nFlashFiles];
			uint8_t *d = f->data;

			if (d)
				*pr = extractSmcConfig(e, d, f->size);
		}
''')]),
    ('fds', [(OLD, '''		{
			struct fileent *f = &xb.files[xb.nFlashFiles];
			uint8_t *d = f->data;
			uint32_t n = f->size;

			if (d)
				*pr = extractSmcConfig(e, d, n);
		}
''')]),
    ('ds', [(OLD, '''		{
			uint8_t *d = xb.files[xb.nFlashFiles].data;

			if (d) {
				int n = xb.files[xb.nFlashFiles].size;

				*pr = extractSmcConfig(e, d, n);
			}
		}
''')]),
    ('fp', [(OLD, '''		{
			struct fileent *f = xb.files + xb.nFlashFiles;

			if (f->data)
				*pr = extractSmcConfig(e, f->data, f->size);
		}
''')]),
    ('nd', [(OLD, '''		{
			int n = xb.nFlashFiles;

			if (xb.files[n].data)
				*pr = extractSmcConfig(e, xb.files[n].data, xb.files[n].size);
		}
''')]),
    ('ni', [(OLD, '''		{
			uint32_t n = xb.nFlashFiles;
			uint8_t *d = xb.files[n].data;

			if (d)
				*pr = extractSmcConfig(e, d, xb.files[n].size);
		}
''')]),
]]
