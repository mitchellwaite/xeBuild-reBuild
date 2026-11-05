"""getImageSmc: as with detectController's pin_lo2, can one asm do the work of the addr pin and the unreachable (or of the optimize attribute)?
Positions of the addr pin, unreachable dropped or kept, attribute dropped or kept."""
FOCUS = ['_getImageSmc']
BASE = 'tools/wip/dehint/drafts/image_read_attempt2.c'
ATTR = '__attribute__((optimize("no-if-conversion", "no-if-conversion2", "no-tree-tail-merge"))) void getImageSmc'
UN = '''			if (!h)
				__builtin_unreachable();
'''
PIN = '''	} else
		__asm__("" : "+D"(addr));
'''
A = '"+D"(addr)'
ASM = '__asm__("" : ' + A + ');\n'
J = '	if (__builtin_expect(addr < 528 * xb.dumpPages, 0)) {\n'
S3 = '''			size = 0x3000;
'''
S8 = '''			size = 0x3800;
'''
AXP = [
    ('pk', []),
    ('pj', [(PIN, '	}\n'), (J, '	' + ASM + J)]),
    ('p3', [(PIN, '	}\n'), (S3, S3 + '			' + ASM)]),
    ('pe', [(PIN, '	} else\n		__asm__("" : "+D"(addr));\n'), (S3, S3 + '			' + ASM)]),
    ('p38', [(PIN, '	}\n'), (S3, S3 + '			' + ASM), (S8, S8 + '			' + ASM)]),
    ('pu', [(PIN, '	} else\n		__asm__("" : : "D"(addr));\n')]),
]
AXU = [('uk', []), ('u0', [(UN, '')])]
AXO = [('ok', []), ('o0', [(ATTR, 'void getImageSmc')])]
AXES = [AXP, AXU, AXO]
