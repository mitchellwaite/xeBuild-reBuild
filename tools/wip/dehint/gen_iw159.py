# attempt 9: pin_hdr, requirement (B) without flipping the preheader's load order: explicit reloads after the ECC, so spare's PHI partition holds an original, low SSA name
# rather than only PRE's descending names.  On the expect-75 stand-in for (A); wanted IDENTICAL.
import os
OLD = '''			if (__builtin_expect(!pageErased(xb.hdr + (b * 32 + p) * 512, xb.spare + (b * 32 + p) * 16), 0))
				calcPageEcc(xb.hdr + (b * 32 + p) * 512, xb.spare + (b * 32 + p) * 16);
			memcpy(raw, xb.hdr + (b * 32 + p) * 512, 512);
			memcpy(raw + 512, xb.spare + (b * 32 + p) * 16, 16);
'''
X = '(b * 32 + p) * 512'
Y = '(b * 32 + p) * 16'
DECL = '	uint8_t *raw, *s, *spare;\n'
def v(head, arm, tail):
    t = head + '			if (__builtin_expect(!pageErased(H0, S0), 0)) {\n				calcPageEcc(H0, S0);\n' + arm + '			}\n' + tail
    return t
HS = '			spare = xb.spare;\n			h = xb.hdr;\n'
SH = '			h = xb.hdr;\n			spare = xb.spare;\n'
vars = []
for hn, head, sub in (
    ('s', '			spare = xb.spare;\n', {'H0': 'xb.hdr + ' + X, 'S0': 'spare + ' + Y}),
    ('hs', HS, {'H0': 'h + ' + X, 'S0': 'spare + ' + Y}),
    ('sh', SH, {'H0': 'h + ' + X, 'S0': 'spare + ' + Y}),
    ('h', '			h = xb.hdr;\n', {'H0': 'h + ' + X, 'S0': 'xb.spare + ' + Y}),
):
    for an, arm in (('a', '				spare = xb.spare;\n'), ('b', '				h = xb.hdr;\n				spare = xb.spare;\n'), ('c', '				spare = xb.spare;\n				h = xb.hdr;\n'), ('d', '				h = xb.hdr;\n')):
        for tn, tail in (('', None),):
            useh = 'h = xb' in arm or 'h' in hn
            uses = 'spare = xb' in arm or 's' in hn
            tl = '			memcpy(raw, %s + %s, 512);\n			memcpy(raw + 512, %s + %s, 16);\n' % ('h' if 'h = xb' in arm else 'xb.hdr', X, 'spare' if 'spare = xb' in arm else 'xb.spare', Y)
            body = v(head, arm, tl)
            for a, b in sub.items():
                body = body.replace(a, b)
            vars.append((hn + an, [(OLD, body), (DECL, DECL + '	uint8_t *h;\n')]))
AXES = [vars]
BASE = 'build/iw/a9/ex.c'
FLAGS = ['--param', 'builtin-expect-probability=75']
FOCUS = ['_finalizeImage']
