# attempt 4: FS loop forms with a short dying arm (value local, conditional expression): a shorter run of released names (see gen_iw51)
import os
BASE = os.environ.get('IWB', 'tools/wip/dehint/drafts/image_write_near3.c')
OLD = '''			if (next != 0 && next != 0xffff) {
				fsTable[start + i - xb.fsStart] = SWAP16_IMAGE_WRITE(next);
			} else {
				fsTable[start + i - xb.fsStart] = SWAP16_IMAGE_WRITE(start + i - xb.fsStart + 1);
			}
'''
E = 'start + i - xb.fsStart'
F = {
 'v1': f'			{{ uint16_t v; if (next != 0 && next != 0xffff) v = next; else v = {E} + 1;\n			fsTable[{E}] = SWAP16_IMAGE_WRITE(v); }}\n',
 'v2': f'			{{ uint16_t v = next != 0 && next != 0xffff ? next : {E} + 1;\n			fsTable[{E}] = SWAP16_IMAGE_WRITE(v); }}\n',
 'v3': f'			{{ uint32_t v = next != 0 && next != 0xffff ? next : {E} + 1;\n			fsTable[{E}] = SWAP16_IMAGE_WRITE(v); }}\n',
 'v4': f'			{{ uint32_t v; if (next != 0 && next != 0xffff) v = next; else v = {E} + 1;\n			fsTable[{E}] = SWAP16_IMAGE_WRITE(v); }}\n',
 'v5': f'			{{ uint32_t v = {E} + 1; if (next != 0 && next != 0xffff) v = next;\n			fsTable[{E}] = SWAP16_IMAGE_WRITE(v); }}\n',
 'v6': f'			{{ uint32_t v = {E}; if (next != 0 && next != 0xffff) fsTable[v] = SWAP16_IMAGE_WRITE(next); else {{ v++; fsTable[v - 1] = SWAP16_IMAGE_WRITE(v); }} }}\n',
 'v7': f'			if (next == 0 || next == 0xffff) {{\n				fsTable[{E}] = SWAP16_IMAGE_WRITE({E} + 1);\n			}} else {{\n				fsTable[{E}] = SWAP16_IMAGE_WRITE(next);\n			}}\n',
 'v8': f'			if (next != 0 && next != 0xffff)\n				fsTable[{E}] = SWAP16_IMAGE_WRITE(next);\n			else\n				fsTable[{E}] = SWAP16_IMAGE_WRITE({E} + 1);\n',
 'v9': f'			fsTable[{E}] = next != 0 && next != 0xffff ? SWAP16_IMAGE_WRITE(next) : SWAP16_IMAGE_WRITE({E} + 1);\n',
}
AXES = [[(n, [(OLD, f)]) for n, f in F.items()]]
