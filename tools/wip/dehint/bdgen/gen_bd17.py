"""XB_FILES_BOUND: address spelling instead of a smaller array bound"""
REMOVE = ['bound']
FOCUS = ['_verifyBlSigs', '_addBlsToImage']
EV = ('''	for (i = 1; i < (uint32_t)xb.nFiles; i++) {
		e = &xb.files[i];
		switch (e->type) {''', '''	for (i = 1; i < (uint32_t)xb.nFiles; i++) {
		e = xb.files + i;
		switch (e->type) {''')
EA = ('''	for (i = 1; i < (uint32_t)xb.nFlashFiles; i++) {
		e = &xb.files[i];
		type = e->type;
		if (e->offset != 0xffffffff)
			off = e->offset;
		if (!strnicmp(e->name, "none", 4) && !e->crc)''', '''	for (i = 1; i < (uint32_t)xb.nFlashFiles; i++) {
		e = xb.files + i;
		type = e->type;
		if (e->offset != 0xffffffff)
			off = e->offset;
		if (!strnicmp(e->name, "none", 4) && !e->crc)''')
FF = ('''	for (i = 0; i < xb.nFiles; i++)
		if (xb.files[i].type == type)
			return i;''', '''	for (i = 0; i < xb.nFiles; i++)
		if ((xb.files + i)->type == type)
			return i;''')
FO = ('''		if (xb.files[i].type == type)
			return xb.files[i].offset;''', '''		if ((xb.files + i)->type == type)
			return (xb.files + i)->offset;''')
FS = ('''		if (xb.files[i].type == type)
			return xb.files[i].size;''', '''		if ((xb.files + i)->type == type)
			return (xb.files + i)->size;''')
AXES = [[('', []), ('ev', [EV])], [('', []), ('ea', [EA])], [('', []), ('ff', [FF])], [('', []), ('fo', [FO])], [('', []), ('fs', [FS])],
        [('', []), ('p', [('uint32_t findFileOffset(int type)\n{\n	int i;', 'uint32_t findFileOffset(int type)\n{\n	int i;')])]]
