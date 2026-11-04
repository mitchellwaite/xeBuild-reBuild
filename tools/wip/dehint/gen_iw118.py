# attempt 7: hot label lnp2 gone, on src (IWB= for others): npages' shapes x memset/end forms (r136 = off + len's references decide the slot swap in imgAddFile)
import os
N = '''		if (len % 512)
			npages = (len + 512) / 512;
		else
			npages = len / 512;
		if (!partial)
			npages = 32;
		else {
			/* imgAddFile's clone: keeps DOM2's threading from zeroing the npages guard edge */
			lnp2: __attribute__((hot));
		}
'''
CALC = '''if (len % 512)
				npages = (len + 512) / 512;
			else
				npages = len / 512;
'''
F = {
 'plain': '''		if (len % 512)
			npages = (len + 512) / 512;
		else
			npages = len / 512;
		if (!partial)
			npages = 32;
''',
 'le': '''		if (len % 512)
			npages = (len + 512) / 512;
		else
			npages = len / 512;
		if (partial <= 0)
			npages = 32;
''',
 'n1': '		if (partial) {\n			' + CALC + '		} else\n			npages = 32;\n',
 'n3': '''		if (!partial)
			npages = 32;
		else if (len % 512)
			npages = (len + 512) / 512;
		else
			npages = len / 512;
''',
 'n6': '''		npages = 32;
		if (partial)
			npages = len % 512 ? (len + 512) / 512 : len / 512;
''',
}
M = '		memset(xb.hdr + off + len, 0, ((off + len + 0x3fff) & ~0x3fff) - (off + len));\n'
IE = '	imgEnd = off + len;\n'
AXES = [
 [(k, [(N, v)]) for k, v in F.items()],
 [('', []),
  ('m1', [(M, '		memset(xb.hdr + (off + len), 0, ((off + len + 0x3fff) & ~0x3fff) - (off + len));\n')]),
  ('m2', [(M, '		memset(xb.hdr + off + len, 0, ((off + len + 0x3fff) & ~0x3fff) - off - len);\n')]),
  ('m3', [(M, '		memset(xb.hdr + off + len, 0, 0x4000 - ((off + len) & 0x3fff));\n')]),
  ('m4', [(M, '		memset(xb.hdr + off + len, 0, ((off + len + 0x3fff) & ~0x3fff) - off - len);\n'), (IE, '	imgEnd = len + off;\n')]),
  ('m5', [(M, '		memset(&xb.hdr[off + len], 0, ((off + len + 0x3fff) & ~0x3fff) - (off + len));\n')]),
 ],
]
BASE = os.environ.get('IWB', 'src/image_write.c')
FLAGS = []
