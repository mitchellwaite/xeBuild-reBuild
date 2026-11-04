# attempt 19: pin_hdr. Named h and q for xb.hdr and xb.spare, read at the top of the page, re-read in the ECC arm and/or after it, so the source has its own PHI; both typed u (uint8_t *) or c (const uint8_t *). Grid on noph.
# `IWB=build/iw/a18/noph.c python tools/wip/dehint/iw16sweep.py tools/wip/dehint/gen_iw261.py -n 30 -t 2`
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
SETS = {'': [], 'h': ['h = xb.hdr;'], 'q': ['q = xb.spare;'], 'qh': ['q = xb.spare;', 'h = xb.hdr;'], 'hq': ['h = xb.hdr;', 'q = xb.spare;']}
A = []
for top, arm, aft in itertools.product(SETS, SETS, SETS):
    if not (top or arm or aft): continue
    if top and arm and aft: continue
    used = set(top + arm + aft)
    for th in 'uc' if 'h' in used else 'u':
        for tq in 'uc' if 'q' in used else 'u':
            T = {'u': 'uint8_t *', 'c': 'const uint8_t *'}
            hh = 'h' if 'h' in top else 'xb.hdr'
            qq = 'q' if 'q' in top else 'xb.spare'
            # arm's call uses the top locals; the arm's re-read comes after the call
            armb = '\t\t\t\tcalcPageEcc(xb.hdr + %s, xb.spare + %s);\n' % (X, Y)
            s = ''.join('\t\t\t%s\n' % l for l in SETS[top])
            s += '\t\t\tif (!pageErased(%s + %s, %s + %s))' % (hh, X, qq, Y)
            if arm:
                s += ' {\n' + armb + ''.join('\t\t\t\t%s\n' % l for l in SETS[arm]) + '\t\t\t}\n'
            else:
                s += '\n' + armb
            s += ''.join('\t\t\t%s\n' % l for l in SETS[aft])
            mh = 'h' if ('h' in top and ('h' in arm or 'h' in aft)) or 'h' in aft else 'xb.hdr'
            mq = 'q' if ('q' in top and ('q' in arm or 'q' in aft)) or 'q' in aft else 'xb.spare'
            s += '\t\t\tmemcpy(raw, %s + %s, 512);\n\t\t\tmemcpy(raw + 512, %s + %s, 16);\n' % (mh, X, mq, Y)
            decl = ''
            if 'h' in used: decl += '\t%sh;\n' % T[th]
            if 'q' in used: decl += '\t%sq;\n' % T[tq]
            A.append(('t%s_a%s_f%s_%s%s' % (top, arm, aft, th, tq), [(B, s), (D, D + decl)]))
AXES = [A]
