"""checkHeader: ifcombine only merges when the inner block holds nothing but the condition
(cf is FRE'd from the earlier test).  A load the sink pass moves down later does the asm's job."""
FOCUS = ['_checkHeader']
BAR = '''	__asm__("");
	if (SWAP32(hdr.cfOffset) > SWAP32(hdr.sysUpdateAddr)) {'''
USE = '''	if (SWAP16(hdr.sysUpdateCount) != 2)
'''
DECL = '''	long long size;

	size = getFileSize64(fp);
'''
AXES = [[
    ('count', [(BAR, '''	count = SWAP16(hdr.sysUpdateCount);
	if (SWAP32(hdr.cfOffset) > SWAP32(hdr.sysUpdateAddr)) {'''),
               (USE, '''	if (count != 2)
'''), (DECL, '''	long long size;
	uint16_t count;

	size = getFileSize64(fp);
''')]),
    ('countu32', [(BAR, '''	count = SWAP16(hdr.sysUpdateCount);
	if (SWAP32(hdr.cfOffset) > SWAP32(hdr.sysUpdateAddr)) {'''),
               (USE, '''	if (count != 2)
'''), (DECL, '''	long long size;
	uint32_t count;

	size = getFileSize64(fp);
''')]),
    ('countraw', [(BAR, '''	count = hdr.sysUpdateCount;
	if (SWAP32(hdr.cfOffset) > SWAP32(hdr.sysUpdateAddr)) {'''),
               (USE, '''	if (SWAP16(count) != 2)
'''), (DECL, '''	long long size;
	uint16_t count;

	size = getFileSize64(fp);
''')]),
]]
