# attempt 19: pin_hdr. Around gen_iw261's tqh_aqh_f_uc: q and h read at the top of the page and again in the ECC arm, memcpy through them. Preheader and hdr/spare registers are right there; r187, r192 and the block's raw are what's left. Crosses page-index form, arm forms, types, the arm's call arguments, names.
# `IWB=build/iw/a18/noph.c python tools/wip/dehint/iw16sweep.py tools/wip/dehint/gen_iw263.py -n 30 -t 4`
import os, itertools
BASE = os.environ.get('IWB', 'build/iw/a18/noph.c')
B = '''			if (!pageErased(xb.hdr + (b * 32 + p) * 512, xb.spare + (b * 32 + p) * 16))
				calcPageEcc(xb.hdr + (b * 32 + p) * 512, xb.spare + (b * 32 + p) * 16);
			memcpy(raw, xb.hdr + (b * 32 + p) * 512, 512);
			memcpy(raw + 512, xb.spare + (b * 32 + p) * 16, 16);
'''
D = '	uint8_t *raw, *s, *spare;\n'
T = {'u': 'uint8_t *', 'c': 'const uint8_t *'}
A = []
for idx in ('e', 'pg', 'pgb', 'off'):
  for top in ('qh', 'hq'):
    for arm in ('qh', 'hq', 'h', 'q'):
      for call in ('xx', 'hq', 'hx', 'xq'):
        for th, tq in (('c', 'u'), ('u', 'c'), ('c', 'c'), ('u', 'u')):
          for name in ('q', 'spare'):
            if name == 'spare' and tq == 'c': continue
            X = {'e': '(b * 32 + p) * 512', 'pg': 'pg * 512', 'pgb': 'pg * 512', 'off': 'off'}[idx]
            Y = {'e': '(b * 32 + p) * 16', 'pg': 'pg * 16', 'pgb': 'pg * 16', 'off': 'off / 32'}[idx]
            s = ''
            if idx == 'pg': s += '\t\t\tpg = b * 32 + p;\n'
            if idx == 'pgb': s += '\t\t\tpg = b0 + p;\n'
            if idx == 'off': s += '\t\t\toff = (b * 32 + p) * 512;\n'
            rd = {'q': '%s = xb.spare;' % name, 'h': 'h = xb.hdr;'}
            s += ''.join('\t\t\t%s\n' % rd[c] for c in top)
            s += '\t\t\tif (!pageErased(h + %s, %s + %s)) {\n' % (X, name, Y)
            s += '\t\t\t\tcalcPageEcc(%s + %s, %s + %s);\n' % ('xb.hdr' if call[0] == 'x' else 'h', X, 'xb.spare' if call[1] == 'x' else name, Y)
            s += ''.join('\t\t\t\t%s\n' % rd[c] for c in arm)
            s += '\t\t\t}\n\t\t\tmemcpy(raw, h + %s, 512);\n\t\t\tmemcpy(raw + 512, %s + %s, 16);\n' % (X, name, Y)
            decl = '\t%sh;\n' % T[th]
            if name == 'q': decl += '\t%sq;\n' % T[tq]
            if idx in ('pg', 'pgb'): decl += '\tuint32_t pg;\n'
            if idx == 'pgb': decl += '\tuint32_t b0;\n'
            if idx == 'off': decl += '\tuint32_t off;\n'
            ed = [(B, s), (D, D + decl)]
            if idx == 'pgb':
                ed.append(('		for (p = 0; p < 32; p++) {\n			pg = b0', '		for (p = 0; p < 32; p++) {\n			pg = b0'))
            A.append(('%s_t%s_a%s_c%s_%s%s_%s' % (idx, top, arm, call, th, tq, name[0]), ed))
AXES = [[a for a in A if not a[0].startswith('pgb')]]
def FILTER(c):
    # only forms that keep the arm's spare reload (the reference reloads both); drop this to see the rest
    return any(k in c[0][0] for k in ('_aqh_', '_ahq_', '_aq_'))
