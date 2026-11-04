"""loadFlashFile: types change the inline summary (likely-eliminated statements)."""
BASE = 'tools/wip/dehint/drafts/image_read_attempt1.c'
P = 'int loadFlashFile(int i, uint32_t block) __attribute__((noinline));'
D = 'int loadFlashFile(int i, uint32_t block)\n{'
L = '''	uint32_t off = fsOffset + (block << 14);
	uint32_t left = xb.flashSize[i];
	uint32_t done = 0;

	xb.flashBuf[i] = calloc(left, 1);
'''
def sig(ret, a, b):
    return [(P, f'{ret} loadFlashFile({a} i, {b} block);'), (D, f'{ret} loadFlashFile({a} i, {b} block)\n{{')]
AX0 = []
for ret in ('int', 'uint32_t', 'void'):
    for a in ('int', 'uint32_t'):
        for b in ('uint32_t', 'int', 'long'):
            e = sig(ret, a, b)
            if ret == 'void':
                e = e + [('	return verifyFlashFile(i);\n}\n\nint fsFindFile', '	verifyFlashFile(i);\n}\n\nint fsFindFile')]
            AX0.append((f'{ret}.{a}.{b}', e))
AX1 = [('', []),
       ('doneint', [(L, L.replace('uint32_t done', 'int done'))]),
       ('offint', [(L, L.replace('uint32_t off', 'int off'))]),
       ('leftint', [(L, L.replace('uint32_t left', 'int left'))]),
       ('ptr', [(L, L.replace('	uint32_t done = 0;\n', '	uint8_t *done;\n').replace('xb.flashBuf[i] = calloc(left, 1);', 'xb.flashBuf[i] = calloc(left, 1);\n	done = xb.flashBuf[i];'))]),
       ]
AXES = [AX0, AX1[:4]]
