"""loadFlashFile without noinline: the mask as its own statement (s_two in gen_ir18 stays out of
the caller but changes RA).  Numbering variants."""
BASE = 'tools/wip/dehint/drafts/image_read_attempt1.c'
NO = [('int loadFlashFile(int i, uint32_t block) __attribute__((noinline));', 'int loadFlashFile(int i, uint32_t block);')]
S = '''		left -= 0x4000;
		done += 0x4000;
		block = SWAP16(fs->map[block]) & 0x1fff;
		off = fsOffset + (block << 14);
	}
	if (left)
		memcpy(xb.flashBuf[i] + done, xb.dump + off, left);
	return verifyFlashFile(i);
'''
T = '''		left -= 0x4000;
		done += 0x4000;
%s
		off = fsOffset + (block << 14);
	}
	if (left)
		memcpy(xb.flashBuf[i] + done, xb.dump + off, left);
	return verifyFlashFile(i);
'''
L = '''	uint32_t off = fsOffset + (block << 14);
	uint32_t left = xb.flashSize[i];
	uint32_t done = 0;

	xb.flashBuf[i] = calloc(left, 1);
'''
V = {
    'two': '		block = SWAP16(fs->map[block]);\n		block &= 0x1fff;',
    'n_u': '		{\n			uint32_t next = SWAP16(fs->map[block]);\n			block = next & 0x1fff;\n		}',
    'n_i': '		{\n			int next = SWAP16(fs->map[block]);\n			block = next & 0x1fff;\n		}',
    'twoi': '		block = SWAP16(fs->map[block]);\n		block = (int)block & 0x1fff;',
    'mask': '		block = fs->map[block];\n		block = SWAP16(block) & 0x1fff;',
    'mask2': '		block = fs->map[block];\n		block = SWAP16(block);\n		block &= 0x1fff;',
    'mask3': '		{\n			uint16_t m = fs->map[block];\n			block = SWAP16(m);\n			block &= 0x1fff;\n		}',
    'umask': '		block = SWAP16((uint32_t)fs->map[block]) & 0x1fff;',
    'pre': '		block &= 0xffff;\n		block = SWAP16(fs->map[block]) & 0x1fff;',
}
AXL = [('', []),
       ('o1', [(L, '''	uint32_t off, left, done;

	off = fsOffset + (block << 14);
	left = xb.flashSize[i];
	done = 0;
	xb.flashBuf[i] = calloc(left, 1);
''')]),
       ('o2', [(L, '''	uint32_t left = xb.flashSize[i];
	uint32_t off = fsOffset + (block << 14);
	uint32_t done = 0;

	xb.flashBuf[i] = calloc(left, 1);
''')]),
       ]
AXES = [[('', NO)], [(k, [(S, T % v)]) for k, v in V.items()], AXL]
