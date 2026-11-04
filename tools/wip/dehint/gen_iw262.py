# attempt 19: pin_hdr. Re-reading xb.spare into its named local in the ECC arm lowers spare's IRA cost below hdr's (216 v 176), which is the tie the pin breaks. Wanted also: spare's load first in the preheader. Grid: where each local is read, which name carries spare, whether hdr is named, what the arm's call and memcpy use.
# `IWB=build/iw/a18/noph.c python tools/wip/dehint/iw19irasweep.py tools/wip/dehint/gen_iw262.py -t 4`
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
A = []
for qn, qt in (('q', 'uint8_t *'), ('q', 'const uint8_t *'), ('spare', None)):
  for hmode in ('none', 'topfirst', 'topafter', 'topexpr', 'late'):
    for ht in ('uint8_t *', 'const uint8_t *'):
      if hmode == 'none' and ht != 'uint8_t *': continue
      for callq in ('x', 'q'):
        for armq in ('after', 'afterblk'):
          for mh in ('x', 'h'):
            if hmode in ('none', 'topexpr') and mh == 'h': continue
            s = ''
            if hmode == 'topfirst': s += '\t\t\th = xb.hdr;\n'
            s += '\t\t\t%s = xb.spare;\n' % qn
            if hmode == 'topafter': s += '\t\t\th = xb.hdr;\n'
            if hmode == 'topexpr': s += '\t\t\th = xb.hdr + %s;\n' % X
            ha = 'h + ' + X if hmode in ('topfirst', 'topafter') else ('h' if hmode == 'topexpr' else 'xb.hdr + ' + X)
            s += '\t\t\tif (!pageErased(%s, %s + %s)) {\n' % (ha, qn, Y)
            s += '\t\t\t\tcalcPageEcc(xb.hdr + %s, %s + %s);\n' % (X, 'xb.spare' if callq == 'x' else qn, Y)
            if armq == 'after': s += '\t\t\t\t%s = xb.spare;\n\t\t\t}\n' % qn
            else: s += '\t\t\t\t%s = xb.spare;\n\t\t\t}\n' % qn
            if hmode == 'late': s += '\t\t\th = xb.hdr;\n'
            mm = ('h + ' + X) if (mh == 'h' or hmode == 'late') else ('xb.hdr + ' + X)
            s += '\t\t\tmemcpy(raw, %s, 512);\n\t\t\tmemcpy(raw + 512, %s + %s, 16);\n' % (mm, qn, Y)
            decl = ''
            if qt: decl += '\t%s%s;\n' % (qt, qn)
            if hmode != 'none': decl += '\t%sh;\n' % ht
            lab = '%s%s_%s%s_c%s_%s_m%s' % (qn, 'c' if qt and 'const' in qt else '', hmode, 'c' if 'const' in ht else '', callq, armq[:3] + armq[-1], mh)
            if armq == 'afterblk': continue
            A.append((lab, [(B, s), (D, D + decl)]))
AXES = [A]
