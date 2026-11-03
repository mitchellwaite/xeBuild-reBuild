# attempt 4: writeFsTable's compare: ivopts pops incr and end out of one run of names, the else arm of the FS loop in the inlined big copy
# (names released in sequence when next != 0xffff kills it).  A boundary between incr and end needs another length of that run: forms of the arm's index and value.
import os
BASE = os.environ.get('IWB', 'tools/wip/dehint/drafts/image_write_near3.c')
OLD = '''			if (next != 0 && next != 0xffff) {
				fsTable[start + i - xb.fsStart] = SWAP16_IMAGE_WRITE(next);
			} else {
				fsTable[start + i - xb.fsStart] = SWAP16_IMAGE_WRITE(start + i - xb.fsStart + 1);
			}
'''
if 'near3a' in BASE or 'image_write.c' in BASE:
    OLD = OLD.replace('start + i - xb.fsStart', 'start - xb.fsStart + i')
IDX = ['start + i - xb.fsStart', 'start - xb.fsStart + i', 'i + start - xb.fsStart', 'i - xb.fsStart + start']
VAL = ['start + i - xb.fsStart + 1', 'start - xb.fsStart + i + 1', 'start + i + 1 - xb.fsStart', 'i + 1 + start - xb.fsStart',
       'start + (i + 1) - xb.fsStart', '(start + i - xb.fsStart) + 1', '1 + start + i - xb.fsStart', 'i + start - xb.fsStart + 1']
F = []
for a, ia in enumerate(IDX):
    for c, ib in enumerate(IDX):
        for b, v in enumerate(VAL):
            F.append((f'i{a}{c}v{b}', f'			if (next != 0 && next != 0xffff) {{\n				fsTable[{ia}] = SWAP16_IMAGE_WRITE(next);\n			}} else {{\n				fsTable[{ib}] = SWAP16_IMAGE_WRITE({v});\n			}}\n'))
J = {'j0': 'start + i - xb.fsStart', 'j1': 'start - xb.fsStart + i', 'j2': 'i + start - xb.fsStart'}
for k, e in J.items():
    F.append((k + 'A', f'			uint32_t j = {e};\n			if (next != 0 && next != 0xffff) {{\n				fsTable[j] = SWAP16_IMAGE_WRITE(next);\n			}} else {{\n				fsTable[j] = SWAP16_IMAGE_WRITE(j + 1);\n			}}\n'))
    F.append((k + 'B', f'			if (next != 0 && next != 0xffff) {{\n				fsTable[{e}] = SWAP16_IMAGE_WRITE(next);\n			}} else {{\n				uint32_t j = {e} + 1;\n				fsTable[j - 1] = SWAP16_IMAGE_WRITE(j);\n			}}\n'))
    F.append((k + 'C', f'			if (next != 0 && next != 0xffff) {{\n				fsTable[{e}] = SWAP16_IMAGE_WRITE(next);\n			}} else {{\n				uint32_t j = {e};\n				fsTable[j] = SWAP16_IMAGE_WRITE(j + 1);\n			}}\n'))
    F.append((k + 'D', f'			if (next != 0 && next != 0xffff) {{\n				fsTable[{e}] = SWAP16_IMAGE_WRITE(next);\n			}} else {{\n				uint16_t j = {e} + 1;\n				fsTable[{e}] = SWAP16_IMAGE_WRITE(j);\n			}}\n'))
    F.append((k + 'E', f'			if (next != 0 && next != 0xffff) {{\n				fsTable[{e}] = SWAP16_IMAGE_WRITE(next);\n			}} else {{\n				uint32_t j = {e} + 1;\n				fsTable[{e}] = SWAP16_IMAGE_WRITE(j);\n			}}\n'))
AXES = [[(n, [(OLD, f)]) for n, f in F]]
