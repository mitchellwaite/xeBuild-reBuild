# attempt 11: on near11 (g3): npages' spelling and pieces around it: does anything change the 12 slot lines (r163 npages against r136 off+len)?  Also a local for the sum, which adds references to npages in imgAddFile's copy.
import os
BASE = os.environ.get('IWB', 'build/iw/a11/g3.c')
ARM = '''			if (len % 512)
				npages = (len + 512) / 512;
			else
				npages = len / 512;
'''
FOR = '		for (end = p + npages; p < end; p++) {\n'
AXES = [
 [('', []),
  ('n1', [(ARM, '			npages = len % 512 ? (len + 512) / 512 : len / 512;\n')]),
  ('n2', [(ARM, '			npages = len / 512;\n			if (len % 512)\n				npages++;\n')]),
  ('n3', [(ARM, '			npages = len % 512 ? len / 512 + 1 : len / 512;\n')]),
  ('n4', [(ARM, '			npages = (len + 511) / 512;\n')]),
  ('n5', [(ARM, '			if (len % 512 == 0)\n				npages = len / 512;\n			else\n				npages = (len + 512) / 512;\n')]),
 ],
 [('', []),
  ('f1', [(FOR, '		end = p + npages;\n		for (; p < end; p++) {\n')]),
  ('f2', [(FOR, '		for (end = npages + p; p < end; p++) {\n')]),
  ('f3', [(FOR, '		if (npages)\n		for (end = p + npages; p < end; p++) {\n')]),
  ('f4', [(FOR, '		end = p + npages;\n		while (p < end) {\n'), ('				}\n			}\n		}\n	}\n#undef BLK', '				}\n			}\n			p++;\n		}\n	}\n#undef BLK')]),
 ],
]
FLAGS = []
FOCUS = ['_imgAddFile']
