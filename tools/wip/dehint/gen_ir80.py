"""getImageSmc, no hint at all, on the current source: forms of the address test (one log or two) crossed with the size test, the last test and the types of addr/size."""
import re, os
FOCUS = ['_getImageSmc']
BASE = 'src/image_read.c'
_src = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..', BASE), newline='').read().replace('\r\n', '\n')
_m = re.search(r'__attribute__\(\(optimize\("no-if-conversion", "no-if-conversion2", "no-tree-tail-merge"\)\)\) void getImageSmc\(void\)\n\{.*?\n\}\n', _src, re.S)
OLD = _m.group(0)
TAIL = '''xb.smc.data = malloc(size);
		if (xb.smc.data) {
			xb.smc.size = size;
			memcpy(xb.smc.data, xb.dump + addr, size);
			log_printf(1, "decrypting SMC at address 0x%x of size 0x%x\\n", addr, size);
			if (unscramble(xb.smc.data, xb.smc.size)) {
				log_printf(1, "SMC decrypted OK, will use if no external smc.bin is provided\\n");
				setSmcKey(xb.smc.data);
			} else {
				log_printf(1, "SMC did not decrypt, discarding it\\n");
				free(xb.smc.data);
				xb.smc.data = 0;
				xb.smc.size = 0;
			}
		} else
			log_printf(1, "Wasn't able to alloc 0x%x bytes memory for SMC bin, not using...\\n", size);
'''
NS = 'log_printf(1, "SMC at 0x%x of size 0x%x is not sane, skipping smc.bin in NAND image\\n", addr, size);\n'
BAD = 'log_printf(1, "smc.bin should not be at 0x%x, trying 0x1000\\n", addr);\n		addr = 0x1000;\n'
A = {
    'seq': f'if (!addr) {{\n{BAD}}}\nif (addr != 0x800 && addr != 0x1000) {{\n{BAD}}}\n',
    'elif': f'if (!addr) {{\n{BAD}}} else if (addr != 0x800 && addr != 0x1000) {{\n{BAD}}}\n',
    'one': f'if (!addr || (addr != 0x800 && addr != 0x1000)) {{\n{BAD}}}\n',
    'one2': f'if (addr != 0x800 && addr != 0x1000 || !addr) {{\n{BAD}}}\n',
    'and': f'if (addr != 0x800 && addr != 0x1000) {{\n{BAD}}}\n',
    'seqn': f'if (!addr) {{\n{BAD}}}\nif (addr != 0x800) {{\nif (addr != 0x1000) {{\n{BAD}}}\n}}\n',
    'nest': f'if (addr != 0x800) {{\nif (addr != 0x1000) {{\n{BAD}}}\n}}\n',
    'and1': f'if (addr != 0x1000 && addr != 0x800) {{\n{BAD}}}\n',
    'seq1': f'if (!addr) {{\n{BAD}}}\nif (addr != 0x1000 && addr != 0x800) {{\n{BAD}}}\n',
}
S800 = 'size = 0x3800;\n log_printf(1, "smc.bin should not be 0x%x bytes, using 0x3800\\n", size);\n'
S000 = 'size = 0x3000;\n log_printf(1, "smc.bin should not be 0x%x bytes, using 0x3000\\n", size);\n'
B = {
    'and': f'if (size != 0x3000 && size != 0x3800) {{\nif (addr == 0x800) {{\n{S800}}} else {{\n{S000}}}\n}}\n',
    'nest': f'if (size != 0x3000) {{\nif (size != 0x3800) {{\nif (addr == 0x800) {{\n{S800}}} else {{\n{S000}}}\n}}\n}}\n',
    'ne': f'if (size != 0x3000 && size != 0x3800) {{\nif (addr != 0x800) {{\n{S000}}} else {{\n{S800}}}\n}}\n',
    'and38': f'if (size != 0x3800 && size != 0x3000) {{\nif (addr == 0x800) {{\n{S800}}} else {{\n{S000}}}\n}}\n',
    'e1000': f'if (size != 0x3000 && size != 0x3800) {{\nif (addr == 0x1000) {{\n{S000}}} else {{\n{S800}}}\n}}\n',
}
C = {
    'lt': f'if (addr < 528 * xb.dumpPages) {{\n{TAIL}}} else {{\n{NS}}}\n',
    'ge': f'if (addr >= 528 * xb.dumpPages) {{\n{NS}}} else {{\n{TAIL}}}\n',
    'ret': f'if (addr >= 528 * xb.dumpPages) {{\n{NS}return;\n}}\n{TAIL}',
}
D = {
    'ii': 'int addr = SWAP32(h->smcBootAddr);\n	int size = SWAP32(h->smcBootSize);\n',
    'uu': 'uint32_t addr = SWAP32(h->smcBootAddr);\n	uint32_t size = SWAP32(h->smcBootSize);\n',
    'ui': 'uint32_t addr = SWAP32(h->smcBootAddr);\n	int size = SWAP32(h->smcBootSize);\n',
    'iu': 'int addr = SWAP32(h->smcBootAddr);\n	uint32_t size = SWAP32(h->smcBootSize);\n',
}
def mk(d, a, b, c):
    return 'void getImageSmc(void)\n{\n	struct flashhdr *h = (struct flashhdr *)xb.dump;\n	' + d + '\n	' + a + b + c + '}\n'
AXES = [[(f'{dk}.{ak}.{bk}.{ck}', [(OLD, mk(d, a, b, c))])
         for dk, d in D.items() for ak, a in A.items() for bk, b in B.items() for ck, c in C.items()]]
