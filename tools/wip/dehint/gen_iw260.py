# attempt 19: pin_hdr. A local for xb.hdr and/or xb.spare in the ECD page body, with a type whose TYPE_CANONICAL differs from uint8_t *: a PHI mixing the two may keep a copy at expand, which is a transient reference to hdr at IRA.
# `IWB=build/iw/a18/noph.c python tools/wip/dehint/iw16sweep.py tools/wip/dehint/gen_iw260.py -n 30 -t 2`
import os, itertools
BASE = os.environ.get('IWB', 'build/iw/a18/noph.c')
B = '''			if (!pageErased(xb.hdr + (b * 32 + p) * 512, xb.spare + (b * 32 + p) * 16))
				calcPageEcc(xb.hdr + (b * 32 + p) * 512, xb.spare + (b * 32 + p) * 16);
			memcpy(raw, xb.hdr + (b * 32 + p) * 512, 512);
			memcpy(raw + 512, xb.spare + (b * 32 + p) * 16, 16);
'''
D = '	uint8_t *raw, *s, *spare;\n'
X = '(b * 32 + p) * 512'
Y = '(b * 32 + p) * 16'
TY = {'u': 'uint8_t *', 'c': 'const uint8_t *', 'v': 'const void *', 'n': 'void *', 'k': 'const char *'}
# (name, top statements, head args, arm args, after statements, memcpy sources); %h, %q are the locals
SH = [
 ('hT', 'h = xb.hdr;\n', 'h + X', 'xb.spare + Y', 'xb.hdr + X', 'xb.spare + Y', '', 'xb.hdr + X', 'xb.spare + Y', 'h'),
 ('qT', 'q = xb.spare;\n', 'xb.hdr + X', 'q + Y', 'xb.hdr + X', 'xb.spare + Y', '', 'xb.hdr + X', 'xb.spare + Y', 'q'),
 ('qhT', 'q = xb.spare;\nh = xb.hdr;\n', 'h + X', 'q + Y', 'xb.hdr + X', 'xb.spare + Y', '', 'xb.hdr + X', 'xb.spare + Y', 'hq'),
 ('hqT', 'h = xb.hdr;\nq = xb.spare;\n', 'h + X', 'q + Y', 'xb.hdr + X', 'xb.spare + Y', '', 'xb.hdr + X', 'xb.spare + Y', 'hq'),
 ('hA', '', 'xb.hdr + X', 'xb.spare + Y', 'xb.hdr + X', 'xb.spare + Y', 'h = xb.hdr;\n', 'h + X', 'xb.spare + Y', 'h'),
 ('qhA', '', 'xb.hdr + X', 'xb.spare + Y', 'xb.hdr + X', 'xb.spare + Y', 'q = xb.spare;\nh = xb.hdr;\n', 'h + X', 'q + Y', 'hq'),
 ('hqA', '', 'xb.hdr + X', 'xb.spare + Y', 'xb.hdr + X', 'xb.spare + Y', 'h = xb.hdr;\nq = xb.spare;\n', 'h + X', 'q + Y', 'hq'),
 ('dT', 'd = xb.hdr + X;\n', 'd', 'xb.spare + Y', 'xb.hdr + X', 'xb.spare + Y', '', 'xb.hdr + X', 'xb.spare + Y', 'd'),
 ('dA', '', 'xb.hdr + X', 'xb.spare + Y', 'xb.hdr + X', 'xb.spare + Y', 'd = xb.hdr + X;\n', 'd', 'xb.spare + Y', 'd'),
 ('dB', 'd = xb.hdr + X;\n', 'd', 'xb.spare + Y', 'xb.hdr + X', 'xb.spare + Y', 'd = xb.hdr + X;\n', 'd', 'xb.spare + Y', 'd'),
 ('hB', 'h = xb.hdr;\n', 'h + X', 'xb.spare + Y', 'xb.hdr + X', 'xb.spare + Y', 'h = xb.hdr;\n', 'h + X', 'xb.spare + Y', 'h'),
]
def mk(sh, th, tq):
    n, top, ha, hb, aa, ab, aft, ma, mb, vs = sh
    def R(s):
        return s.replace('X', X).replace('Y', Y)
    def ind(s):
        return ''.join('\t\t\t' + l + '\n' for l in s.split('\n') if l)
    body = ind(R(top)) + '\t\t\tif (!pageErased(%s, %s))\n\t\t\t\tcalcPageEcc(%s, %s);\n' % (R(ha), R(hb), R(aa), R(ab)) + ind(R(aft)) + '\t\t\tmemcpy(raw, %s, 512);\n\t\t\tmemcpy(raw + 512, %s, 16);\n' % (R(ma), R(mb))
    decl = ''
    if 'h' in vs: decl += '\t%sh;\n' % TY[th]
    if 'd' in vs: decl += '\t%sd;\n' % TY[th]
    if 'q' in vs: decl += '\t%sq;\n' % TY[tq]
    return ('%s_%s%s' % (n, th, tq), [(B, body), (D, D + decl)])
A = []
for sh in SH:
    for th in TY:
        for tq in TY:
            if 'q' not in sh[9] and tq != 'u': continue
            if ('h' not in sh[9] and 'd' not in sh[9]) and th != 'u': continue
            if th in 'vn' and 'd' not in sh[9] and 'h' in sh[9]: pass
            A.append(mk(sh, th, tq))
AXES = [A]
