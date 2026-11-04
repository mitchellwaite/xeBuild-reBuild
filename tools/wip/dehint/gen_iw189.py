# attempt 11: on near11 (g3).  One hint in imgAddFile for the slots instead of two in imgAdd: that would still be a net reduction (lnp2 and pin_t gone, one new).  The big arm hotter: guard/head up.
import os
BASE = os.environ.get('IWB', 'build/iw/a11/g3.c')
CALL = '''		if (!xb.bigBlock)
			imgAdd(off, data, len, 0, 0xffff, 1);
		else
			imgAdd(off, data, len, 0x2a, 0xffff, 1);
'''
S = '			imgAdd(off, data, len, 0, 0xffff, 1);\n'
B = '			imgAdd(off, data, len, 0x2a, 0xffff, 1);\n'
HEAD = '	if (imgFits(off, len)) {\n		fsFiles[nFsFiles].block'
ALL = [
 ('', []),
 ('hb', [(CALL, '		if (!xb.bigBlock)\n' + S + '		else {\n			big: __attribute__((hot));\n' + B + '		}\n')]),
 ('xb', [(CALL, '		if (!__builtin_expect(xb.bigBlock != 0, 1))\n' + S + '		else\n' + B)]),
 ('xs', [(CALL, '		if (__builtin_expect(!xb.bigBlock, 0))\n' + S + '		else\n' + B)]),
 ('ab', [(CALL, '		if (!xb.bigBlock) {\n			if ((len & 0x3fff) > 0x3fff)\n				abort();\n' + S + '		} else\n' + B)]),
 ('ad', [(HEAD, '	if ((len & 0x3fff) > 0x3fff)\n		len++;\n' + HEAD)]),
 ('ad2', [(CALL, '		if ((len & 0x3fff) > 0x3fff)\n			len++;\n' + CALL)]),
 ('ad3', [(CALL, '		if (!xb.bigBlock && (len & 0x3fff) <= 0x3fff)\n' + S + '		else\n' + B)]),
 ('ad4', [(CALL, '		if (xb.bigBlock || (len & 0x3fff) > 0x3fff)\n' + B + '		else\n' + S)]),
]
AXES = [ALL]
FLAGS = []
