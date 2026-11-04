# attempt 18: pin_hdr. Forms of finalizeImage's ECD loop body without the pin; the pin gives hdr eax and spare ebp, without it they swap. Linux loads spare first in the preheader, so forms that compute spare first.
# `IWB=build/iw/a18/noph.c python tools/wip/dehint/iw16sweep.py tools/wip/dehint/gen_iw255.py -n 30 -t 1`
import os
BASE = os.environ.get('IWB', 'build/iw/a18/noph.c')
B = '''			if (!pageErased(xb.hdr + (b * 32 + p) * 512, xb.spare + (b * 32 + p) * 16))
				calcPageEcc(xb.hdr + (b * 32 + p) * 512, xb.spare + (b * 32 + p) * 16);
			memcpy(raw, xb.hdr + (b * 32 + p) * 512, 512);
			memcpy(raw + 512, xb.spare + (b * 32 + p) * 16, 16);
'''
D = '	uint8_t *raw, *s, *spare;\n'
def L(body, decl='uint32_t pg'):
    return [(B, body), (D, D + '	%s;\n' % decl)]
PG = 'b * 32 + p'
A = [('', []),
 ('pg', L('			pg = b * 32 + p;\n			if (!pageErased(xb.hdr + pg * 512, xb.spare + pg * 16))\n				calcPageEcc(xb.hdr + pg * 512, xb.spare + pg * 16);\n			memcpy(raw, xb.hdr + pg * 512, 512);\n			memcpy(raw + 512, xb.spare + pg * 16, 16);\n')),
 ('hs', L('			h = xb.hdr + (b * 32 + p) * 512;\n			q = xb.spare + (b * 32 + p) * 16;\n			if (!pageErased(h, q))\n				calcPageEcc(h, q);\n			memcpy(raw, h, 512);\n			memcpy(raw + 512, q, 16);\n', 'uint8_t *h, *q')),
 ('sh', L('			q = xb.spare + (b * 32 + p) * 16;\n			h = xb.hdr + (b * 32 + p) * 512;\n			if (!pageErased(h, q))\n				calcPageEcc(h, q);\n			memcpy(raw, h, 512);\n			memcpy(raw + 512, q, 16);\n', 'uint8_t *h, *q')),
 ('sh2', L('			q = xb.spare + (b * 32 + p) * 16;\n			h = xb.hdr + (b * 32 + p) * 512;\n			if (!pageErased(h, q))\n				calcPageEcc(h, q);\n			memcpy(raw, xb.hdr + (b * 32 + p) * 512, 512);\n			memcpy(raw + 512, xb.spare + (b * 32 + p) * 16, 16);\n', 'uint8_t *h, *q')),
 ('sh3', L('			q = xb.spare + (b * 32 + p) * 16;\n			if (!pageErased(xb.hdr + (b * 32 + p) * 512, q))\n				calcPageEcc(xb.hdr + (b * 32 + p) * 512, q);\n			memcpy(raw, xb.hdr + (b * 32 + p) * 512, 512);\n			memcpy(raw + 512, q, 16);\n', 'uint8_t *q')),
 ('sh4', L('			q = xb.spare + (b * 32 + p) * 16;\n			if (!pageErased(xb.hdr + (b * 32 + p) * 512, q))\n				calcPageEcc(xb.hdr + (b * 32 + p) * 512, xb.spare + (b * 32 + p) * 16);\n			memcpy(raw, xb.hdr + (b * 32 + p) * 512, 512);\n			memcpy(raw + 512, xb.spare + (b * 32 + p) * 16, 16);\n', 'uint8_t *q')),
 ('hl', L('			h = xb.hdr;\n			if (!pageErased(h + (b * 32 + p) * 512, xb.spare + (b * 32 + p) * 16))\n				calcPageEcc(xb.hdr + (b * 32 + p) * 512, xb.spare + (b * 32 + p) * 16);\n			memcpy(raw, xb.hdr + (b * 32 + p) * 512, 512);\n			memcpy(raw + 512, xb.spare + (b * 32 + p) * 16, 16);\n', 'uint8_t *h')),
 ('ql', L('			q = xb.spare;\n			if (!pageErased(xb.hdr + (b * 32 + p) * 512, q + (b * 32 + p) * 16))\n				calcPageEcc(xb.hdr + (b * 32 + p) * 512, xb.spare + (b * 32 + p) * 16);\n			memcpy(raw, xb.hdr + (b * 32 + p) * 512, 512);\n			memcpy(raw + 512, xb.spare + (b * 32 + p) * 16, 16);\n', 'uint8_t *q')),
 ('er', L('			er = pageErased(xb.hdr + (b * 32 + p) * 512, xb.spare + (b * 32 + p) * 16);\n			if (!er)\n				calcPageEcc(xb.hdr + (b * 32 + p) * 512, xb.spare + (b * 32 + p) * 16);\n			memcpy(raw, xb.hdr + (b * 32 + p) * 512, 512);\n			memcpy(raw + 512, xb.spare + (b * 32 + p) * 16, 16);\n', 'int er')),
 ('sw', [(B, '			if (pageErased(xb.hdr + (b * 32 + p) * 512, xb.spare + (b * 32 + p) * 16) == 0)\n				calcPageEcc(xb.hdr + (b * 32 + p) * 512, xb.spare + (b * 32 + p) * 16);\n			memcpy(raw, xb.hdr + (b * 32 + p) * 512, 512);\n			memcpy(raw + 512, xb.spare + (b * 32 + p) * 16, 16);\n')]),
]
PE = 'int pageErased(const uint8_t *data, const uint8_t *spare)\n'
AXES = [A]
FLAGS = []
