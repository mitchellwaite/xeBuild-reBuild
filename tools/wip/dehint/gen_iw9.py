# imgAdd: the t/partial slot order without the "g"(t) pin
BASE = 'tools/wip/dehint/drafts/image_write.c'
FOCUS = ['_imgAdd', '_imgAdd.constprop.1', '_imgAdd.constprop.2', '_imgAdd.constprop.4', '_imgAddFile', '_writeFsTable']
PIN = '''			/* no code: the slot order of t and partial (dead in every clone) */
			__asm__("" :: "g"(t));
'''
T = "		t = type - '1';\n"
P = "		partial = type != 0 && type != '0' && len < 0x4000;\n"
NP = '''		if (len % 512)
			npages = (len + 512) / 512;
		else
			npages = len / 512;
'''
GD = '''		if (t < 15) {
'''
AXES = [[('', [(PIN, '')])], [
    ('', []),
    ('swap', [(T + P, P + T)]),
    ('tlate', [(T + P, P), ('''		p = 0;
		if (t < 15) {''', '''		p = 0;
		t = type - '1';
		if (t < 15) {''')]),
    ('tafterNP', [(T + P, P), ('''		if (!partial)
			npages = 32;''', '''		t = type - '1';
		if (!partial)
			npages = 32;''')]),
    ('notemp', [(T, ''), ("if (t < 15) {", "if ((uint8_t)(type - '1') < 15) {"), ('	uint8_t t;\n', '')]),
    ('locT', [(T, "		uint8_t t = type - '1';\n"), ('	uint8_t t;\n', '')]),
    ('intT', [('	uint8_t t;\n', '	uint32_t t;\n'), (T, "		t = (uint8_t)(type - '1');\n")]),
], [
    ('', []),
    ('dpartial', [('	int partial;\n	uint32_t b;', '	uint32_t b;\n	int partial;')]),
    ('bpart', [('	int partial;\n', '	uint8_t partial;\n')]),
    ('pfirst', [('	uint8_t t;\n', ''), ('	int partial;\n', '	int partial;\n	uint8_t t;\n')]),
]]
