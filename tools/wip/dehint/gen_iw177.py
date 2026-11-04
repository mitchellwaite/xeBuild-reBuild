# attempt 10: on build/iw/a10/d0.c (byte helper, break form, no pin, no expect).  Preheader load order: spare's head load must have a lower SSA version than hdr's, so it has to stay
# a gimplifier temporary (arguments gimplify right to left), while a named `spare` reload somewhere keeps the partition's lowest name below hdr's (attempt 9's (B)).  Named loads in the arm and in the tail.
import os
OLD = '''			if (!pageErased(xb.hdr + (b * 32 + p) * 512, xb.spare + (b * 32 + p) * 16))
				calcPageEcc(xb.hdr + (b * 32 + p) * 512, xb.spare + (b * 32 + p) * 16);
			memcpy(raw, xb.hdr + (b * 32 + p) * 512, 512);
			memcpy(raw + 512, xb.spare + (b * 32 + p) * 16, 16);
'''
X = '(b * 32 + p) * 512'
Y = '(b * 32 + p) * 16'
DECL = '	uint8_t *raw, *s, *spare;\n'
HX, SX = 'xb.hdr + ' + X, 'xb.spare + ' + Y
V = []
HEAD = '			if (!pageErased(%s, %s))\n				calcPageEcc(%s, %s);\n'
HEADB = '			if (!pageErased(%s, %s)) {\n				calcPageEcc(%s, %s);\n%s			}\n'
def tail(pre1, hx, pre2, sx):
    return pre1 + '			memcpy(raw, %s, 512);\n' % hx + pre2 + '			memcpy(raw + 512, %s, 16);\n' % sx
L = {'s': '			spare = xb.spare;\n', 'h': '			h = xb.hdr;\n', 'S': '			sp = xb.spare + %s;\n' % Y, 'D': '			d = xb.hdr + %s;\n' % X}
# tail forms
TF = {
 't0': tail('', HX, '', SX),
 't1': tail(L['s'], HX, '', 'spare + ' + Y),
 't2': tail('', HX, L['s'], 'spare + ' + Y),
 't3': tail(L['h'], 'h + ' + X, '', SX),
 't4': tail(L['s'] + L['h'], 'h + ' + X, '', 'spare + ' + Y),
 't5': tail(L['h'] + L['s'], 'h + ' + X, '', 'spare + ' + Y),
 't6': tail(L['h'], 'h + ' + X, L['s'], 'spare + ' + Y),
 't7': tail('', HX, L['S'], 'sp'),
 't8': tail(L['S'], HX, '', 'sp'),
 't9': tail(L['D'], 'd', L['S'], 'sp'),
 't10': tail(L['S'] + L['D'], 'd', '', 'sp'),
 't11': tail(L['D'] + L['S'], 'd', '', 'sp'),
 't12': tail(L['D'], 'd', '', SX),
}
for tk, tv in TF.items():
    V.append(('e' + tk, [(OLD, HEAD % (HX, SX, HX, SX) + tv), (DECL, DECL + '	uint8_t *h, *d, *sp;\n')]))
# head temporaries for the test, named pointer for calc only
for nm, arm_pre, c1, c2 in (('c1', '				spare = xb.spare;\n', HX, 'spare + ' + Y), ('c2', '				h = xb.hdr;\n', 'h + ' + X, SX), ('c3', '				spare = xb.spare;\n				h = xb.hdr;\n', 'h + ' + X, 'spare + ' + Y), ('c4', '				h = xb.hdr;\n				spare = xb.spare;\n', 'h + ' + X, 'spare + ' + Y)):
    for tk, tv in TF.items():
        V.append((nm + tk, [(OLD, '			if (!pageErased(%s, %s)) {\n' % (HX, SX) + arm_pre + '				calcPageEcc(%s, %s);\n			}\n' % (c1, c2) + tv), (DECL, DECL + '	uint8_t *h, *d, *sp;\n')]))
AXES = [V]
BASE = os.environ.get('IWB', 'build/iw/a10/d0.c')
FLAGS = []
FOCUS = ['_finalizeImage']
