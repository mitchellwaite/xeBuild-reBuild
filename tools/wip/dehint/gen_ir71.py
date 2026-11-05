"""base2: forms of the end of parseDump, watching entry and tail frequency (need tail >= entry*100/1000)."""
BASE = 'tools/wip/dehint/drafts/image_read_attempt4_base2.c'
FOCUS = ['_parseDump']
OLD_HEAD = '''	if ((int)xb.bootFlags & 0x40000000) {
		if (xb.numBad) {
			log_printf(1, "Discarding remap data as NOREMAP was specified!\\n");
			xb.numBad = 0;
		}
	} else if (xb.numBad) {
'''
A = [('', []),
     ('ret', [(OLD_HEAD, '''	if ((int)xb.bootFlags & 0x40000000) {
		if (xb.numBad) {
			log_printf(1, "Discarding remap data as NOREMAP was specified!\\n");
			xb.numBad = 0;
		}
		return 1;
	}
	if (xb.numBad) {
''')]),
     ('elsret', [(OLD_HEAD, '''	if (!((int)xb.bootFlags & 0x40000000)) {
		if (xb.numBad) {
''')]) if False else ('', []),
     ('ret2', [(OLD_HEAD, '''	if ((int)xb.bootFlags & 0x40000000) {
		if (!xb.numBad)
			return 1;
		log_printf(1, "Discarding remap data as NOREMAP was specified!\\n");
		xb.numBad = 0;
	} else if (xb.numBad) {
''')]),
     ('ret3', [(OLD_HEAD, '''	if ((int)xb.bootFlags & 0x40000000) {
		if (!xb.numBad)
			return 1;
		log_printf(1, "Discarding remap data as NOREMAP was specified!\\n");
		xb.numBad = 0;
		return 1;
	}
	if (xb.numBad) {
''')]),
     ('e0', [(OLD_HEAD, '''	if ((int)xb.bootFlags & 0x40000000) {
		if (xb.numBad != 0) {
			log_printf(1, "Discarding remap data as NOREMAP was specified!\\n");
			xb.numBad = 0;
		}
	} else if (xb.numBad != 0) {
''')]),
     ]
B = [('', []),
     ('nr0', [('''			log_printf(1, "Discarding remap data as NOREMAP was specified!\\n");
			xb.numBad = 0;
''', '''			xb.numBad = 0;
			log_printf(1, "Discarding remap data as NOREMAP was specified!\\n");
''')]) if False else ('', [])]
AXES = [A]
