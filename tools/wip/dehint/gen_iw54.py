# attempt 4: FS loop: index local before the `if`, the macro argument still the full expression (keeps the short-arithmetic narrowing of SWAP16's
# first half, so generic imgAdd may stay equal) x spelling
import os
BASE = os.environ.get('IWB', 'tools/wip/dehint/drafts/image_write_near3.c')
OLD = '''			if (next != 0 && next != 0xffff) {
				fsTable[start + i - xb.fsStart] = SWAP16_IMAGE_WRITE(next);
			} else {
				fsTable[start + i - xb.fsStart] = SWAP16_IMAGE_WRITE(start + i - xb.fsStart + 1);
			}
'''
IDX = ['start + i - xb.fsStart', 'start - xb.fsStart + i', 'i + start - xb.fsStart']
VAL = ['start + i - xb.fsStart + 1', 'start - xb.fsStart + i + 1', 'start + i + 1 - xb.fsStart', 'i + 1 + start - xb.fsStart', 'j + 1', 'b + 1', 'b + i + 1', 'b + i + 1 - xb.fsStart']
F = {}
for a, e in enumerate(IDX):
    for c, v in enumerate(VAL):
        if 'b +' in v:
            continue
        F[f'A{a}{c}'] = f'			uint32_t j = {e};\n			if (next != 0 && next != 0xffff)\n				fsTable[j] = SWAP16_IMAGE_WRITE(next);\n			else\n				fsTable[j] = SWAP16_IMAGE_WRITE({v});\n'
        F[f'B{a}{c}'] = f'			if (next != 0 && next != 0xffff) {{\n				uint32_t j = {e};\n				fsTable[j] = SWAP16_IMAGE_WRITE(next);\n			}} else {{\n				uint32_t j = {e};\n				fsTable[j] = SWAP16_IMAGE_WRITE({v});\n			}}\n'
        F[f'C{a}{c}'] = f'			uint16_t *e = &fsTable[{e}];\n			uint32_t j = {e};\n			if (next != 0 && next != 0xffff)\n				*e = SWAP16_IMAGE_WRITE(next);\n			else\n				*e = SWAP16_IMAGE_WRITE({v});\n'
        F[f'D{a}{c}'] = f'			uint16_t *e = fsTable + {e};\n			uint32_t j = {e};\n			if (next == 0 || next == 0xffff)\n				*e = SWAP16_IMAGE_WRITE({v});\n			else\n				*e = SWAP16_IMAGE_WRITE(next);\n'
AXES = [[(n, [(OLD, f)]) for n, f in F.items()]]
