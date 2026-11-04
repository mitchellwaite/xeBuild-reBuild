# attempt 18: pin_hdr. gen_iw255 `hl` (h = xb.hdr at the loop head, used only by pageErased) gives hdr eax and spare ebp without the pin, 236 lines. Crosses: which loads are held in locals, where they're loaded, which calls use them.
# `IWB=build/iw/a18/noph.c python tools/wip/dehint/iw16sweep.py tools/wip/dehint/gen_iw256.py -n 30 -t 1`
import os, itertools
BASE = os.environ.get('IWB', 'build/iw/a18/noph.c')
B = '''			if (!pageErased(xb.hdr + (b * 32 + p) * 512, xb.spare + (b * 32 + p) * 16))
				calcPageEcc(xb.hdr + (b * 32 + p) * 512, xb.spare + (b * 32 + p) * 16);
			memcpy(raw, xb.hdr + (b * 32 + p) * 512, 512);
			memcpy(raw + 512, xb.spare + (b * 32 + p) * 16, 16);
'''
D = '	uint8_t *raw, *s, *spare;\n'
HS = '	for (b = 0; b < xb.blocks; b++)\n		for (p = 0; p < 32; p++) {\n'
HH = 'xb.hdr + (b * 32 + p) * 512'
QQ = 'xb.spare + (b * 32 + p) * 16'
hh = 'h + (b * 32 + p) * 512'
qq = 'q + (b * 32 + p) * 16'
opts = []
# where: inner = at the top of the page body, block = per block, func = before the loops. order: h then q, q then h, h only, q only
for where in ('in', 'bl', 'fn'):
    for ord_ in ('hq', 'qh', 'h', 'q'):
        for useE in (0, 1):          # pageErased's args use the local
            for useC in (0, 1):      # calcPageEcc's
                for useM in (0, 1):  # the memcpys'
                    if not (useE or useC or useM):
                        continue
                    lo = {'hq': ['h = xb.hdr;', 'q = xb.spare;'], 'qh': ['q = xb.spare;', 'h = xb.hdr;'], 'h': ['h = xb.hdr;'], 'q': ['q = xb.spare;']}[ord_]
                    a = lambda u: (hh if u and 'h' in ord_ else HH, qq if u and 'q' in ord_ else QQ)
                    e, c, m = a(useE), a(useC), a(useM)
                    body = '			if (!pageErased(%s, %s))\n				calcPageEcc(%s, %s);\n			memcpy(raw, %s, 512);\n			memcpy(raw + 512, %s, 16);\n' % (e[0], e[1], c[0], c[1], m[0], m[1])
                    dl = '	uint8_t *h, *q;\n'
                    if where == 'in':
                        ed = [(B, ''.join('			%s\n' % x for x in lo) + body)]
                    elif where == 'bl':
                        ed = [(B, body), (HS, '	for (b = 0; b < xb.blocks; b++) {\n' + ''.join('		%s\n' % x for x in lo) + '		for (p = 0; p < 32; p++) {\n'),
                              ('			raw += 528;\n		}\n	log_printf(1, "done!\n");\n	if (xb.nandMu', '			raw += 528;\n		}\n	}\n	log_printf(1, "done!\n");\n	if (xb.nandMu')]
                    else:
                        ed = [(B, body), (HS, ''.join('	%s\n' % x for x in lo) + HS)]
                    opts.append(('%s_%s_%d%d%d' % (where, ord_, useE, useC, useM), ed + [(D, D + dl)]))
AXES = [opts]
FLAGS = []
