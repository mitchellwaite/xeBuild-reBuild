# imgAdd's two dead tests with empty asm bodies: plain C bodies, with and without pin_end, opt, and the shapes
BASE = 'tools/wip/dehint/drafts/image_write.c'
D2 = '''		if (x > first + 0x4000)
			__asm__("");
'''
D4 = '''		if ((len & 0x3fff) > 0x3fff)
			__asm__("");
'''
BODIES = {'': None, 'bl': 'blocks++;', 'bl2': 'blocks += 2;', 'st': 'start++;', 'fi': 'first++;', 'rm': ''}
def body(old, cond, name):
    v = BODIES[name]
    if v is None:
        return []
    if v == '':
        return [(old, '')]
    return [(old, f'		if ({cond})\n			{v}\n')]
PE = [('''	__asm__("" :: "g"(end));
''', '')]
NEXT = ('''			if (next != 0 && next != 0xffff) {
				fsTable[start - xb.fsStart + i] = SWAP16_IMAGE_WRITE(next);
			} else {
				fsTable[start - xb.fsStart + i] = SWAP16_IMAGE_WRITE(start - xb.fsStart + i + 1);
			}
''', '''			if (next != 0 && next != 0xffff) {
				fsTable[start + i - xb.fsStart] = SWAP16_IMAGE_WRITE(next);
			} else {
				fsTable[start + i - xb.fsStart] = SWAP16_IMAGE_WRITE(start + i - xb.fsStart + 1);
			}
''')
T = ("		t = type - '1';\n		partial = type != 0 && type != '0' && len < 0x4000;\n",
     "		partial = type != 0 && type != '0' && len < 0x4000;\n		t = type - '1';\n")
PG = ('''			pages = len / 512;
			if (len % 512)
				pages++;
''', '''			pages = len % 512 ? len / 512 + 1 : len / 512;
''')
AXES = [
    [('d2' + k, body(D2, 'x > first + 0x4000', k)) for k in BODIES],
    [('d4' + k, body(D4, '(len & 0x3fff) > 0x3fff', k)) for k in BODIES],
    [('', []), ('pe', PE)],
    [('', []), ('next', [NEXT])],
    [('', []), ('t', [T])],
    [('', []), ('pg', [PG])],
]
