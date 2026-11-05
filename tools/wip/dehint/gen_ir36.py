"""getImageSmc from attempt 2's draft: the subset lattice of its hints crossed with the polarity of the last test."""
FOCUS = ['_getImageSmc']
BASE = 'tools/wip/dehint/drafts/image_read_attempt2.c'
ATTR = '__attribute__((optimize("no-if-conversion", "no-if-conversion2", "no-tree-tail-merge"))) void getImageSmc'
V = '''	} else {
		vhot: __attribute__((hot));
	}
'''
GOOD = '''		xb.smc.data = malloc(size);
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
BADL = '''		log_printf(1, "SMC at 0x%x of size 0x%x is not sane, skipping smc.bin in NAND image\\n", addr, size);
'''
OLD = '	if (__builtin_expect(addr < 528 * xb.dumpPages, 0)) {\n' + GOOD + '	} else {\n' + BADL + '	}\n'
AXP = [
    ('ek', []),
    ('e0', [(OLD, '	if (addr < 528 * xb.dumpPages) {\n' + GOOD + '	} else {\n' + BADL + '	}\n')]),
    ('ge', [(OLD, '	if (addr >= 528 * xb.dumpPages) {\n' + BADL + '	} else {\n' + GOOD + '	}\n')]),
    ('ret', [(OLD, '	if (addr >= 528 * xb.dumpPages) {\n' + BADL + '		return;\n	}\n' + GOOD)]),
]
AX = [
    [('ok', []), ('o0', [(ATTR, 'void getImageSmc')])],
    [('vk', []), ('v0', [(V, '	}\n')])],
    [('sk', []), ('s0', [('		shot: __attribute__((hot));\n', '')])],
    [('bk', []), ('b0', [('	bhot: __attribute__((hot));\n', '')])],
    [('uk', []), ('u0', [('''			if (!h)
				__builtin_unreachable();
''', '')])],
    [('pk', []), ('p0', [('''	} else
		__asm__("" : "+D"(addr));
''', '''	}
''')])],
]
AXES = AX + [AXP]
