# attempt 4: FS loop: value and index locals computed before the `if` (the arm's run of released names gets shorter; gen_iw52 v5 proves that
# the wanted compare tuple is reachable that way, but that form loses imgAdd)
import os
BASE = os.environ.get('IWB', 'tools/wip/dehint/drafts/image_write_near3.c')
OLD = '''			if (next != 0 && next != 0xffff) {
				fsTable[start + i - xb.fsStart] = SWAP16_IMAGE_WRITE(next);
			} else {
				fsTable[start + i - xb.fsStart] = SWAP16_IMAGE_WRITE(start + i - xb.fsStart + 1);
			}
'''
E = 'start + i - xb.fsStart'
F = {}
for ety, en in (('uint32_t ', 'u'), ('uint16_t ', 's'), ('int ', 'i')):
    F['a' + en] = f'			{ety}v = {E} + 1;\n			if (next != 0 && next != 0xffff)\n				fsTable[{E}] = SWAP16_IMAGE_WRITE(next);\n			else\n				fsTable[{E}] = SWAP16_IMAGE_WRITE(v);\n'
    F['b' + en] = f'			uint32_t j = {E};\n			{ety}v = j + 1;\n			if (next != 0 && next != 0xffff)\n				fsTable[j] = SWAP16_IMAGE_WRITE(next);\n			else\n				fsTable[j] = SWAP16_IMAGE_WRITE(v);\n'
    F['c' + en] = f'			{ety}v = {E};\n			if (next != 0 && next != 0xffff)\n				fsTable[{E}] = SWAP16_IMAGE_WRITE(next);\n			else\n				fsTable[{E}] = SWAP16_IMAGE_WRITE(v + 1);\n'
    F['d' + en] = f'			{ety}v = {E} + 1;\n			if (next != 0 && next != 0xffff)\n				fsTable[v - 1] = SWAP16_IMAGE_WRITE(next);\n			else\n				fsTable[v - 1] = SWAP16_IMAGE_WRITE(v);\n'
    F['e' + en] = f'			{ety}v = {E};\n			if (next != 0 && next != 0xffff)\n				fsTable[v] = SWAP16_IMAGE_WRITE(next);\n			else\n				fsTable[v] = SWAP16_IMAGE_WRITE(v + 1);\n'
    F['f' + en] = f'			if (next != 0 && next != 0xffff)\n				fsTable[{E}] = SWAP16_IMAGE_WRITE(next);\n			else {{\n				{ety}v = {E} + 1;\n				fsTable[{E}] = SWAP16_IMAGE_WRITE(v);\n			}}\n'
    F['g' + en] = f'			if (next != 0 && next != 0xffff)\n				fsTable[{E}] = SWAP16_IMAGE_WRITE(next);\n			else {{\n				{ety}v = {E};\n				fsTable[v] = SWAP16_IMAGE_WRITE(v + 1);\n			}}\n'
F['h'] = f'			uint32_t lo = ({E} + 1) >> 8, hi = ({E} + 1) << 8;\n			if (next != 0 && next != 0xffff)\n				fsTable[{E}] = SWAP16_IMAGE_WRITE(next);\n			else\n				fsTable[{E}] = (hi & 0xff00) + (lo & 0xff);\n'
AXES = [[(n, [(OLD, f)]) for n, f in F.items()]]
