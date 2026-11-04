# attempt 9: pin_hdr (B), as gen_iw159 but with page pointers: `sp = xb.spare + Y`, `d = xb.hdr + X`, so the loads stay gimplifier temporaries (low versions, value ids
# in statement order) while the reload after the ECC keeps originals in the partitions.  On the expect-75 stand-in; wanted IDENTICAL.
import itertools, os
OLD = '''			if (__builtin_expect(!pageErased(xb.hdr + (b * 32 + p) * 512, xb.spare + (b * 32 + p) * 16), 0))
				calcPageEcc(xb.hdr + (b * 32 + p) * 512, xb.spare + (b * 32 + p) * 16);
			memcpy(raw, xb.hdr + (b * 32 + p) * 512, 512);
			memcpy(raw + 512, xb.spare + (b * 32 + p) * 16, 16);
'''
XH = 'xb.hdr + (b * 32 + p) * 512'
XS = 'xb.spare + (b * 32 + p) * 16'
LD = {'d': '%s = %s;\n' % ('d', XH), 's': '%s = %s;\n' % ('sp', XS)}
DECL = '	uint8_t *raw, *s, *spare;\n'
def lines(order, n):
    return ''.join('\t' * n + LD[c] for c in order)
vars = []
for hn, head in (('sd', 'sd'), ('ds', 'ds'), ('s', 's'), ('d', 'd'), ('', '')):
    for an, arm in (('', ''), ('sd', 'sd'), ('ds', 'ds'), ('s', 's'), ('d', 'd')):
        for tn, tail in (('', ''), ('Ts', 's'), ('Td', 'd'), ('Tds', 'ds'), ('Tsd', 'sd')):
            if any(c in arm for c in tail):
                continue
            hd = 'd' if 'd' in head else XH
            hs = 'sp' if 's' in head else XS
            # the tail uses the variable only if it's defined on both paths
            bothd = 'd' in head or 'd' in tail
            boths = 's' in head or 's' in tail
            if ('d' in arm and 'd' not in head) or ('s' in arm and 's' not in head):
                continue
            if not (head or tail):
                continue
            td = 'd' if bothd else XH
            ts = 'sp' if boths else XS
            if 'd' in tail and 'd' in head:
                continue
            if 's' in tail and 's' in head:
                continue
            body = lines(head, 3) + '			if (__builtin_expect(!pageErased(%s, %s), 0)) {\n				calcPageEcc(%s, %s);\n' % (hd, hs, hd, hs) + lines(arm, 4) + '			}\n' + lines(tail, 3) + '			memcpy(raw, %s, 512);\n			memcpy(raw + 512, %s, 16);\n' % (td, ts)
            vars.append(('H%s+A%s+%s' % (hn, an, tn), [(OLD, body), (DECL, DECL + '	uint8_t *d, *sp;\n')]))
AXES = [vars]
BASE = 'build/iw/a9/ex.c'
FLAGS = ['--param', 'builtin-expect-probability=75']
FOCUS = ['_finalizeImage']
