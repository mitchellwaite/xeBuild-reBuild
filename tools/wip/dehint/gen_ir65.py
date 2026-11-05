"""pin_cb: improve_allocation spills cap a129 (ivtmp of the p loop, cost 5559) for n's l0 allocno when n's cost beats it (5307 without the asm, 5627 with).  So n's uses up or the p loop's frequency down by 5%: exits ahead of the copy (continue/goto), p loop's form."""
FOCUS = ['_parseDump']
BASE = 'tools/wip/dehint/drafts/image_read_attempt3.c'
CB = '	__asm__("" : : "ri"(cb), "ri"(cb), "ri"(cb), "ri"(cb));\n'
FOR = '		for (p = 0; p < ppb; p++) {\n'
M1 = '			memcpy(xb.dump + (dst * ppb + p) * 512, raw + (blk * ppb + p) * 528, 512);\n'
M2 = '			memcpy(xb.dumpSpare + (dst * ppb + p) * 16, raw + (blk * ppb + p) * 528 + 512, 16);\n		}\n'
AXP = [('', []),
       ('dw', [(FOR, '		p = 0;\n		do {\n'), (M2, M2.replace('		}\n', '			p++;\n		} while (p < ppb);\n'))]),
       ('dw2', [(FOR, '		p = 0;\n		do {\n'), (M2, M2.replace('		}\n', '		} while (++p < ppb);\n'))]),
       ('wh', [(FOR, '		p = 0;\n		while (p < ppb) {\n'), (M2, M2.replace('		}\n', '			p++;\n		}\n'))]),
       ('sm', [(FOR, '		for (p = 0; p < ppb; p++) {\n			int d = dst * ppb + p, s = blk * ppb + p;\n\n'),
               (M1, '			memcpy(xb.dump + d * 512, raw + s * 528, 512);\n'),
               (M2, '			memcpy(xb.dumpSpare + d * 16, raw + s * 528 + 512, 16);\n		}\n')]),
       ]
G1 = '			goto next;\n		}\n		if (dst == -3)'
AXC = [('', []),
       ('c1', [(G1, '			continue;\n		}\n		if (dst == -3)')]),
       ]
AX3 = [('', []),
       ('ne', [('		if (dst == -2)\n			continue;\n', '		if (dst != -2) {\n'), ('next:\n		;\n	}\n', 'next:\n		;\n		}\n	}\n')]),
       ]
AX0 = [('', [(CB, '')]), ('k', [])]
AXES = [AXP, AXC, AX3, AX0]
