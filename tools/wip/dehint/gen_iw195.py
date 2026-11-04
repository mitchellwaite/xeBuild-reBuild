# attempt 12: net -1 route: one empty asm on npages in imgAdd replacing both lnp2 and pin_t: it adds a reference at the guard's frequency, which is what imgAddFile's slot order needs (r163 needs +5 REG_FREQ units against r136). Only to size up the idea; plain C is preferred.
import os
BASE = os.environ.get('IWB', 'tools/wip/dehint/drafts/image_write_near11.c')
ARM = '''			else
				npages = len / 512;
		} else
			npages = 32;
		p = 0;
'''
TT = "		if ((uint8_t)t < 15) {\n"
FOR = '		for (end = p + npages; p < end; p++) {\n'
PIN = '__asm__("" :: "g"(npages));'
A = [('', []),
 ('a1', [(ARM, '''			else
				npages = len / 512;
			''' + PIN + '''
		} else
			npages = 32;
		p = 0;
''')]),
 ('a2', [(ARM, ARM.replace('		p = 0;\n', '		' + PIN + '\n		p = 0;\n'))]),
 ('a3', [(FOR, '		' + PIN + '\n' + FOR)]),
 ('a4', [(ARM, '''			else
				npages = len / 512;
		} else
			npages = 32;
		p = 0;
		''' + PIN.replace('"g"', '"rm"') + '\n')]),
 ('a5', [(FOR, '		' + PIN.replace('"g"', '"rm"') + '\n' + FOR)]),
 ('a6', [(FOR, '		' + PIN.replace('"g"', '"r"') + '\n' + FOR)]),
 ('a7', [(ARM, '''			else
				npages = len / 512;
			''' + PIN.replace('"g"', '"r"') + '''
		} else
			npages = 32;
		p = 0;
''')]),
]
B = [('', []),
 ('T', [('	unsigned t;\n', '	uint8_t t;\n'), (TT, '		if (t < 15) {\n')]),
]
AXES = [A, B]
FLAGS = []
