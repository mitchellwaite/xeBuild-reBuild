"""parseDump, no barrier: rejoin shapes.  With the asm, mergephi3 keeps block C (site 2's end) and frees one name fewer: n then pops _133 instead of _100.  Without it: label positions, where the arm rejoins, `dst = blk` placement."""
FOCUS = ['_parseDump']
BASE = 'build/ir/a3/rj.c'
HEAD = '''			if (!addRemapP(blk, blk, blk, -1, blocks))
				return 0;
			dst = blk;
		}
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
'''
CP = '''log_printf(1, "copying nanddump data from block 0x%x to block 0x%x for file extraction integrity\\n", blk, dst);
'''
W1 = '''log_printf(0, "***** WARNING: ignoring possible remap of block 0x%x to block 0x%x\\n", blk, dst);
				log_printf(0, "               this dump may have some bad data!\\n", blk, dst);
'''
R = '''			if (!addRemapP(blk, blk, blk, -1, blocks))
				return 0;
'''
V = {
    'base': HEAD,
    'nol': HEAD.replace('rem: __attribute__((hot));\n', ''),
    'lin': R + '			dst = blk;\n		}\n		if (dst != blk) {\nrem: __attribute__((hot));\n			if (blk >= blocks - 32)\n				' + CP + '			else {\n				' + W1 + '				dst = blk;\n			}\n		}\n',
    'lwa': R + '			dst = blk;\n		}\n		if (dst != blk) {\n			if (blk >= blocks - 32) {\nrem: __attribute__((hot));\n				' + CP + '			} else {\n				' + W1 + '				dst = blk;\n			}\n		}\n',
    'lwb': R + '			dst = blk;\n		}\n		if (dst != blk) {\n			if (blk >= blocks - 32)\n				' + CP + '			else {\nrem: __attribute__((hot));\n				' + W1 + '				dst = blk;\n			}\n		}\n',
    'lelse': R + '			dst = blk;\n		} else {\nrem: __attribute__((hot));\n		}\n		if (dst != blk) {\n			if (blk >= blocks - 32)\n				' + CP + '			else {\n				' + W1 + '				dst = blk;\n			}\n		}\n',
    'inv': R + '			dst = blk;\n		}\nrem: __attribute__((hot));\n		if (dst != blk && blk >= blocks - 32)\n			' + CP + '		else if (dst != blk) {\n				' + W1 + '				dst = blk;\n		}\n',
    'eq': R + '			dst = blk;\n		}\nrem: __attribute__((hot));\n		if (dst == blk) {\n		} else if (blk >= blocks - 32)\n				' + CP + '		else {\n				' + W1 + '				dst = blk;\n		}\n',
    'wlow': R + '			dst = blk;\n		}\nrem: __attribute__((hot));\n		if (dst != blk) {\n			if (blk < blocks - 32) {\n				' + W1 + '				dst = blk;\n			} else\n				' + CP + '		}\n',
    'flag': R + '			dst = blk;\n			goto copy;\n		}\nrem: __attribute__((hot));\n		if (dst != blk) {\n			if (blk >= blocks - 32)\n				' + CP + '			else {\n				' + W1 + '				dst = blk;\n			}\n		}\ncopy:\n',
    'first': '			dst = blk;\n' + R + '		}\nrem: __attribute__((hot));\n		if (dst != blk) {\n			if (blk >= blocks - 32)\n				' + CP + '			else {\n				' + W1 + '				dst = blk;\n			}\n		}\n',
}
AXES = [[(k, [(HEAD, v)]) for k, v in V.items()]]
