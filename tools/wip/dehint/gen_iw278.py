# attempt 21: blocks written so vrp1 can prove blocks != 0 in writeFsTable: the FS loop's guard goes before sccp, so its exit has one predecessor and (expected) sccp doesn't split it.
# `IWB=build/iw/a21/na.c python tools/wip/dehint/iw16sweep.py tools/wip/dehint/gen_iw278.py -n 30 -t 4`
O = '''		rem = len - first;
		tail = rem;
		if (rem >= 0x4000)
			tail = rem % 0x4000;
		blocks = rem / 0x4000;
		if (tail) {
			blocks++;
		}
		if (x) {
			blocks++;
		}
'''
A = [
 ('', []),
 ('b1', [(O, '''		rem = len - first;
		if (rem >= 0x4000) {
			tail = rem % 0x4000;
			blocks = rem / 0x4000;
			if (tail)
				blocks++;
		} else {
			tail = rem;
			blocks = 1;
		}
		if (x) {
			blocks++;
		}
''')]),
 ('b2', [(O, '''		rem = len - first;
		if (rem >= 0x4000) {
			tail = rem % 0x4000;
			blocks = rem / 0x4000;
			if (tail)
				blocks++;
		} else {
			tail = rem;
			blocks = 0;
			if (tail)
				blocks++;
		}
		if (x) {
			blocks++;
		}
''')]),
 ('b3', [(O, '''		rem = len - first;
		tail = rem;
		blocks = 0;
		if (rem >= 0x4000) {
			tail = rem % 0x4000;
			blocks = rem / 0x4000;
		}
		if (tail) {
			blocks++;
		}
		if (x) {
			blocks++;
		}
''')]),
 ('b4', [(O, '''		rem = len - first;
		tail = rem;
		blocks = 1;
		if (rem >= 0x4000) {
			tail = rem % 0x4000;
			blocks = rem / 0x4000;
			if (tail)
				blocks++;
		}
		if (x) {
			blocks++;
		}
''')]),
 ('b5', [(O, '''		rem = len - first;
		tail = rem & 0x3fff;
		blocks = (rem + 0x3fff) / 0x4000;
		if (x) {
			blocks++;
		}
''')]),
 ('b6', [(O, '''		rem = len - first;
		tail = rem;
		if (rem >= 0x4000)
			tail = rem % 0x4000;
		blocks = rem / 0x4000;
		if (tail) {
			blocks++;
		}
		if (x) {
			blocks++;
		}
		if (!blocks) blocks = 1;
''')]),
]
AXES = [A]
