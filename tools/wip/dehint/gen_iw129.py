# attempt 8: pin_t gone: t in a wider type, tested through a uint8_t cast (a pseudo in SImode: its reload count changes).
# IWB= base (default build/iw/a8/nopt.c = src without the pin).
import os
FLAGS = []
BASE = os.environ.get('IWB', 'build/iw/a8/nopt.c')
FOCUS = ['_imgAdd']
D = '	uint8_t t;\n'
C = 'if (t < 15) {'
S = "t = type - '1';"
AXES = [[
 ('base', []),
 ('uint', [(D, '	unsigned t;\n'), (C, 'if ((uint8_t)t < 15) {')]),
 ('int', [(D, '	int t;\n'), (C, 'if ((uint8_t)t < 15) {')]),
 ('u32', [(D, '	uint32_t t;\n'), (C, 'if ((uint8_t)t < 15) {')]),
 ('u16', [(D, '	uint16_t t;\n'), (C, 'if ((uint8_t)t < 15) {')]),
 ('i8', [(D, '	char t;\n'), (C, 'if ((uint8_t)t < 15) {')]),
 ('s8', [(D, '	signed char t;\n'), (C, 'if ((uint8_t)t < 15) {')]),
 ('mask', [(D, '	unsigned t;\n'), (C, 'if ((t & 0xff) < 15) {')]),
 ('imask', [(D, '	int t;\n'), (C, 'if ((t & 0xff) < 15) {')]),
 ('notype', [(D, ''), (C, "if ((uint8_t)(type - '1') < 15) {"), ("		" + S + "\n", '')]),
 ('notype2', [(D, ''), (C, "if (type >= '1' && type < '1' + 15) {"), ("		" + S + "\n", '')]),
 ('ty8', [(D, '	unsigned t;\n'), (S, "t = (uint8_t)(type - '1');")]),
 ('ty9', [(D, '	unsigned t;\n'), (S, "t = (uint8_t)(type - '1');"), (C, 'if ((uint8_t)t < 15) {')]),
 ('int2', [(D, '	unsigned t;\n'), (S, "t = type - 0x31u;"), (C, 'if ((uint8_t)t < 15) {')]),
]]
