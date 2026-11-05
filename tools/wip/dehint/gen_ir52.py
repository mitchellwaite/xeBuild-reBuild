"""parseDump without the barrier (draft 3): 4 loose lines.  (1) `n_98 == _125` for `_125 == n_133` at site 2: ch2's n takes a name from the free list, lower with no asm.
(2) `mov ebp,edi; jmp` for the shared `mov ebp,[esp+2c]; jmp`: site 2's two exits reach Z by two edges with their own copy (forwarder gone, LRA inherits edi on one).
Axes: rejoin shapes for the arm's end, things that shift the free list."""
FOCUS = ['_parseDump']
BASE = 'tools/wip/dehint/drafts/image_read_attempt3.c'
BAR = '''			__asm__("");
			dst = blk;
		} else {
rem: __attribute__((hot));
			if (dst != blk) {
				if (blk >= blocks - 32)
					log_printf(1, "copying nanddump data from block 0x%x to block 0x%x for file extraction integrity\\n", blk, dst);
				else {
					log_printf(0, "***** WARNING: ignoring possible remap of block 0x%x to block 0x%x\\n", blk, dst);
					log_printf(0, "               this dump may have some bad data!\\n", blk, dst);
					dst = blk;
				}
			}
		}
'''
INNER = '''if (dst != blk) {
				if (blk >= blocks - 32)
					log_printf(1, "copying nanddump data from block 0x%x to block 0x%x for file extraction integrity\\n", blk, dst);
				else {
					log_printf(0, "***** WARNING: ignoring possible remap of block 0x%x to block 0x%x\\n", blk, dst);
					log_printf(0, "               this dump may have some bad data!\\n", blk, dst);
					dst = blk;
				}
			}
'''
AXS = [
    ('e', [(BAR, '''			dst = blk;
		} else {
rem: __attribute__((hot));
			''' + INNER + '''		}
''')]),
    ('rj', [(BAR, '''			dst = blk;
		}
rem: __attribute__((hot));
		''' + INNER)]),
    ('rj2', [(BAR, '''			dst = blk;
			goto copy;
		}
rem: __attribute__((hot));
		''' + INNER + '''copy:
''')]),
    ('rj3', [(BAR, '''		} else {
rem: __attribute__((hot));
			''' + INNER + '''			blk2 = dst;
		}
		dst = blk2;
''')]),
]
DECL = [('', []),
        ('d1', [('	int blk, dst, p, b2;\n', '	int dst, blk, p, b2;\n')]),
        ('s1', [('		src = raw + blk * 528 * ppb;\n		dst = checkBlock(src, blk, blocks);\n', '		dst = checkBlock(src = raw + blk * 528 * ppb, blk, blocks);\n')]),
        ('rr', [('	int rr = xb.dumpPages % ppb;\n\n	if (rr) {', '	if (xb.dumpPages % ppb) {')]),
        ('rr2', [('	int ppb = xb.dumpBigBlock ? 256 : 32;\n	int blocks = xb.dumpPages / ppb;\n', '	int ppb = xb.dumpBigBlock ? 256 : 32;\n	int blocks;\n'),
                 ('	int rr = xb.dumpPages % ppb;\n\n	if (rr) {', '	int rr = xb.dumpPages % ppb;\n\n	blocks = xb.dumpPages / ppb;\n	if (rr) {')]),
        ]
AXES = [AXS, DECL]
