# attempt 13: more of the real spare structs on near8 + nohdr (build/iw/a13/n8.c). Linux's stores read as bitfield writes for
# FsBlockType (byte 12, 6 bits) and BlockID0 (4 bits); which of imgAdd's stores go through the type field, with what operand.
import os
BASE = os.environ.get('IWB', 'build/iw/a13/n8.c')
DEF = 'struct spare {\n'
S = '					s[12] = (s[12] & 0xc0) | (type & 0x3f);\n'
SB = '''				if (type > 1) {
					s[12] = (s[12] & 0xc0) | (type & 0x3f);
					if (type != 0x2a'''
SS = '''				if (type > 1) {
					s[12] = (s[12] & 0xc0) | (type & 0x3f);
					s[9] = 32 - pages;'''
F = {'b': '					((struct spt *)s)->type = type;\n',
     'm': '					((struct spt *)s)->type = type & 0x3f;\n',
     'y': S}
ATTR = '__attribute__((optimize("no-tree-scev-cprop"))) void writeFsTable'
DEAD = '''	if ((off & 0x3fff) > 0x3fff)
		off += 0x4000;
'''
AXES = [
 [('', [(DEF, 'struct spt { uint8_t b[12]; uint8_t type:6, ecc3:2; };\n' + DEF)])],
 [('B' + k, [(SB, SB.replace(S, v))]) for k, v in F.items()],
 [('S' + k, [(SS, SS.replace(S, v))]) for k, v in F.items()],
 [('', []), ('noattr', [(ATTR, 'void writeFsTable')])],
 [('', []), ('nodead', [(DEAD, '')])],
]
FLAGS = []
