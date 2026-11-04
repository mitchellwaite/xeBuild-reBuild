# attempt 10: pin_hdr gone, on build/iw/a10/b_us.c (byte helper of class u: (A) flipped with no expect).  Attempt 9's reload and hdr-local forms (gen_iw159, 153), no expect now.
# Wanted: finalizeImage at 4 lines or less.  blockEccOk's 18 is a separate problem.
import os
OLD = '''			if (!pageErased(xb.hdr + (b * 32 + p) * 512, xb.spare + (b * 32 + p) * 16))
				calcPageEcc(xb.hdr + (b * 32 + p) * 512, xb.spare + (b * 32 + p) * 16);
			memcpy(raw, xb.hdr + (b * 32 + p) * 512, 512);
			memcpy(raw + 512, xb.spare + (b * 32 + p) * 16, 16);
'''
X = '(b * 32 + p) * 512'
Y = '(b * 32 + p) * 16'
DECL = '	uint8_t *raw, *s, *spare;\n'
def v(head, arm, tail):
    return head + '			if (!pageErased(H0, S0)) {\n				calcPageEcc(H0, S0);\n' + arm + '			}\n' + tail
HS = '			spare = xb.spare;\n			h = xb.hdr;\n'
SH = '			h = xb.hdr;\n			spare = xb.spare;\n'
vars = []
for hn, head, sub in (
    ('s', '			spare = xb.spare;\n', {'H0': 'xb.hdr + ' + X, 'S0': 'spare + ' + Y}),
    ('hs', HS, {'H0': 'h + ' + X, 'S0': 'spare + ' + Y}),
    ('sh', SH, {'H0': 'h + ' + X, 'S0': 'spare + ' + Y}),
    ('h', '			h = xb.hdr;\n', {'H0': 'h + ' + X, 'S0': 'xb.spare + ' + Y}),
):
    for an, arm in (('a', '				spare = xb.spare;\n'), ('b', '				h = xb.hdr;\n				spare = xb.spare;\n'), ('c', '				spare = xb.spare;\n				h = xb.hdr;\n'), ('d', '				h = xb.hdr;\n'), ('e', '')):
        useh = 'h = xb' in arm and 'h' in hn
        uses = 'spare = xb' in arm and 's' in hn
        if ('h = xb' in arm and 'h' not in hn) or ('spare = xb' in arm and 's' not in hn):
            continue
        tl = '			memcpy(raw, %s + %s, 512);\n			memcpy(raw + 512, %s + %s, 16);\n' % ('h' if useh else 'xb.hdr', X, 'spare' if uses else 'xb.spare', Y)
        body = v(head, arm, tl)
        for a, b in sub.items():
            body = body.replace(a, b)
        vars.append((hn + an, [(OLD, body), (DECL, DECL + '	uint8_t *h;\n')]))
AXES = [[('', [])] + vars]
BASE = os.environ.get('IWB', 'build/iw/a10/b_us.c')
FLAGS = []
FOCUS = ['_finalizeImage']
