# attempt 10: on build/iw/a10/d0.c.  In the head-named forms the lower of the two tied pseudos gets eax, so hdr wants the lower pseudo while its load comes second.  Locals read ahead of the
# block loop, with an arm reload: the loads then sit in the preheader by statement order, not PRE's value order.
import os
OLD = '''			if (!pageErased(xb.hdr + (b * 32 + p) * 512, xb.spare + (b * 32 + p) * 16))
				calcPageEcc(xb.hdr + (b * 32 + p) * 512, xb.spare + (b * 32 + p) * 16);
			memcpy(raw, xb.hdr + (b * 32 + p) * 512, 512);
			memcpy(raw + 512, xb.spare + (b * 32 + p) * 16, 16);
'''
RAW = '	raw = (uint8_t *)mem;\n	for (b = 0; b < xb.blocks; b++)\n		for (p = 0; p < 32; p++) {\n'
X = '(b * 32 + p) * 512'
Y = '(b * 32 + p) * 16'
DECL = '	uint8_t *raw, *s, *spare;\n'
PS, PH = '	spare = xb.spare;\n', '	h = xb.hdr;\n'
AS, AH = '				spare = xb.spare;\n', '				h = xb.hdr;\n'
V = []
for pn, pre, usehp, usesp in (
    ('sh', PS + PH, 1, 1), ('hs', PH + PS, 1, 1), ('s', PS, 0, 1), ('h', PH, 1, 0),
    ('s_h', PS + '	raw = (uint8_t *)mem;\n' + PH, 1, 1), ('h_s', PH + '	raw = (uint8_t *)mem;\n' + PS, 1, 1)):
    for an, arm in (('', ''), ('S', AS), ('H', AH), ('SH', AS + AH), ('HS', AH + AS)):
        if ('S' in an and not usesp) or ('H' in an and not usehp):
            continue
        hv = 'h' if usehp else 'xb.hdr'
        sv = 'spare' if usesp else 'xb.spare'
        body = '			if (!pageErased(%s + %s, %s + %s)) {\n				calcPageEcc(%s + %s, %s + %s);\n%s			}\n			memcpy(raw, %s + %s, 512);\n			memcpy(raw + 512, %s + %s, 16);\n' % (hv, X, sv, Y, hv, X, sv, Y, arm, hv, X, sv, Y)
        rawline = '' if 's_h' == pn or 'h_s' == pn else '	raw = (uint8_t *)mem;\n'
        V.append((pn + an, [(OLD, body), (DECL, DECL + '	uint8_t *h;\n'), (RAW, rawline + pre + '	for (b = 0; b < xb.blocks; b++)\n		for (p = 0; p < 32; p++) {\n')]))
AXES = [V]
BASE = os.environ.get('IWB', 'build/iw/a10/d0.c')
FLAGS = []
FOCUS = ['_finalizeImage']
