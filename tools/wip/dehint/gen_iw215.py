# attempt 14: imgAdd's type arms on near13. ivopts' big-copy names are the VDEF and load of the dead `s[9..7] = xb.spare*` arm (iw14pop.py), so its shape is the lever: arm order, type tests, small arm forms.
import os
BASE = os.environ.get('IWB', 'tools/wip/dehint/drafts/image_write_near13.c')
A = '''					if (type != 0x2a && type != 0x2c) {
						pages = len / 512;
						if (len % 512)
							pages++;
						left = pages;
						if (left & 3)
							left = (left + 4) & ~3;
						s[9] = (((off & 0x1ffff) ? 256 - (off & 0x1ffff) / 512 : 256) - left) >> 2;
						s[5] = 1;
						s[8] = len >> 8;
						s[7] = len;
					} else {
						if (type == 0x2c)
							s[5] = 1;
						s[9] = xb.spare9;
						s[8] = xb.spare8;
						s[7] = xb.spare7;
					}
'''
BODY = A.split('{\n', 1)[1].split('					} else {')[0]
EL = A.split('} else {\n')[1].rsplit('					}\n', 1)[0]
EL1 = '''						s[9] = xb.spare9;
						s[8] = xb.spare8;
						s[7] = xb.spare7;
						if (type == 0x2c)
							s[5] = 1;
'''
EL2 = '''						if (type != 0x2a)
							s[5] = 1;
						s[9] = xb.spare9;
						s[8] = xb.spare8;
						s[7] = xb.spare7;
'''
def form(t, b, e, swap):
    if swap:
        return '					if (%s) {\n%s					} else {\n%s					}\n' % (t[1], e, b)
    return '					if (%s) {\n%s					} else {\n%s					}\n' % (t[0], b, e)
T = [('type != 0x2a && type != 0x2c', 'type == 0x2a || type == 0x2c')]
AX0 = []
for en, e in (('', EL), ('e1', EL1), ('e2', EL2)):
    for sn, sw in (('', False), ('sw', True)):
        AX0.append(('+'.join(x for x in (en, sn) if x), [(A, form(T[0], BODY, e, sw))]))
# early-out spelling: the 2a/2c arm as a local bool
AX0.append(('fl', [(A, '					if (type == 0x2c || type == 0x2a) {\n' + EL + '					} else {\n' + BODY + '					}\n')]))
AX0.append(('fl2', [(A, '					if (type == 0x2a)\n						goto fs;\n					if (type == 0x2c) {\n						s[5] = 1;\n					fs:\n						s[9] = xb.spare9;\n						s[8] = xb.spare8;\n						s[7] = xb.spare7;\n					} else {\n' + BODY + '					}\n')]))
S = '''					s[9] = 32 - pages;
					s[2] = 1;
					if (type != '0') {
						s[8] = len >> 8;
						s[7] = len;
					}
'''
AX1 = [('', []),
 ('s1', [(S, '''					s[2] = 1;
					s[9] = 32 - pages;
					if (type != '0') {
						s[8] = len >> 8;
						s[7] = len;
					}
''')]),
 ('s2', [(S, '''					s[9] = 32 - pages;
					s[2] = 1;
					if (type != '0') {
						s[7] = len;
						s[8] = len >> 8;
					}
''')]),
 ('s3', [(S, '''					s[9] = 32 - pages;
					s[2] = 1;
					if (type == '0')
						continue;
					s[8] = len >> 8;
					s[7] = len;
''')]),
]
ST = '	fsTable[-xb.fsStart + blk] = SWAP16_IMAGE_WRITE(0x1ffd);\n'
AXES = [AX0, AX1,
 [('', []), ('st0', [(ST, '	fsTable[blk - xb.fsStart] = SWAP16_IMAGE_WRITE(0x1ffd);\n')])],
]
FLAGS = []
