"""parseDump without the dead test: entry is set by the exits' probabilities (a `continue` after -1's addRemap alone makes it 136).  Forms of each exit, watching entry and tail (irfq.py)."""
BASE = 'build/ir/a5/nod.c'
FOCUS = ['_parseDump']
S1 = '''			if (!addRemap(blk, dst, blocks))
				return 0;
			goto next;
'''
S4 = '''			if (!addRemap(blk, -1, blocks))
				return 0;
			dst = blk;
'''
S3 = '''		if (dst != blk && !addRemap(dst, blk, blocks))
			return 0;
next:
		;
'''
Z = '''			if (!notZeropair()) {
				log_printf(0, "\\n\\n***** ERROR: nanddump.bin is a ZEROPAIR/XELL image, discarding\\n");
				return 0;
			}
'''
ZL = 'log_printf(0, "\\n\\n***** ERROR: nanddump.bin is a ZEROPAIR/XELL image, discarding\\n");\n'
L = '''			if (!spareLbaOk(ppb)) {
				log_printf(0, "\\n\\n***** ERROR: nanddump.bin has mixed LBA in the same block which usually occurs\\n");
				log_printf(0, "             due to an improper nandpro write method, discarding\\n");
				return 0;
			}
'''
LOG1 = 'log_printf(1, "bad block at 0x%x'
A1 = [('1g', []),
      ('1pos', [(S1, '			if (addRemap(blk, dst, blocks))\n				goto next;\n			return 0;\n')]),
      ('1posc', [(S1, '			if (addRemap(blk, dst, blocks))\n				continue;\n			return 0;\n')]),
      ('1else', [(S1, '			if (!addRemap(blk, dst, blocks))\n				return 0;\n			else\n				goto next;\n')]),
      ('1val', [(S1, '			return_val:\n			goto next;\n')]) if False else ('1z', [(S1, '			if (addRemap(blk, dst, blocks) == 0)\n				return 0;\n			goto next;\n')]),
      ]
A4 = [('4k', []),
      ('4pos', [(S4, '			if (addRemap(blk, -1, blocks))\n				dst = blk;\n			else\n				return 0;\n')]),
      ('4neg', [(S4, '			if (!addRemap(blk, -1, blocks))\n				return 0;\n			else\n				dst = blk;\n')]),
      ]
A3 = [('3k', []),
      ('3n', [(S3, '		if (dst != blk) {\n			if (!addRemap(dst, blk, blocks))\n				return 0;\n		}\nnext:\n		;\n')]),
      ('3c', [(S3, '		if (dst != blk) {\n			if (addRemap(dst, blk, blocks))\n				continue;\n			return 0;\n		}\nnext:\n		;\n')]),
      ('3cc', [(S3, '		if (dst != blk && !addRemap(dst, blk, blocks))\n			return 0;\n		continue;\nnext:\n		;\n')]),
      ('3p', [(S3, '		if (dst == blk || addRemap(dst, blk, blocks))\n			continue;\n		return 0;\nnext:\n		;\n')]),
      ('3e', [(S3, '		if (dst == blk)\n			continue;\n		if (!addRemap(dst, blk, blocks))\n			return 0;\nnext:\n		;\n')]),
      ]
AZ = [('zk', []),
      ('zn', [(Z, '			if (notZeropair()) {\n				if (!spareLbaOk(ppb)) {\n					log_printf(0, "\\n\\n***** ERROR: nanddump.bin has mixed LBA in the same block which usually occurs\\n");\n					log_printf(0, "             due to an improper nandpro write method, discarding\\n");\n					return 0;\n				}\n			} else {\n				' + ZL + '				return 0;\n			}\n'), (L, '')]),
      ]
AXES = [A1, A4, A3, AZ]
