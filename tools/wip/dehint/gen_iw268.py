# attempt 19: pin_hdr gone (gen_iw267 IDENTICAL). Which parts of that shape are needed, and which spelling reads most natural. Base is noph; the arm is calcPageEcc written out, the test `<= 0`, `< 1` or `> 0` with else.
# `IWB=build/iw/a18/noph.c python tools/wip/dehint/iw16sweep.py tools/wip/dehint/gen_iw268.py -n 80 -t 4`
import os, itertools
BASE = os.environ.get('IWB', 'build/iw/a18/noph.c')
B = '''			if (!pageErased(xb.hdr + (b * 32 + p) * 512, xb.spare + (b * 32 + p) * 16))
				calcPageEcc(xb.hdr + (b * 32 + p) * 512, xb.spare + (b * 32 + p) * 16);
			memcpy(raw, xb.hdr + (b * 32 + p) * 512, 512);
			memcpy(raw + 512, xb.spare + (b * 32 + p) * 16, 16);
'''
D = '	uint8_t *raw, *s, *spare;\n'
X = '(b * 32 + p) * 512'; Y = '(b * 32 + p) * 16'
T = {'u': 'uint8_t *', 'c': 'const uint8_t *'}
RD = {'q': 'q = xb.spare;', 'h': 'h = xb.hdr;'}
A = []
for test in ('le', 'lt'):
 for top in ('qh', 'hq', 'q', 'h', ''):
  for arm in ('qh', 'hq', 'q', 'h', ''):
   for th, tq in (('u', 'c'), ('c', 'c'), ('u', 'u'), ('c', 'u')):
    for pn in ('s', 'x'):
     for scope in ('fn', 'blk'):
      used = set(top + arm)
      if 'h' not in used and th != 'u': continue
      if 'q' not in used and tq != 'u': continue
      hh = 'h' if 'h' in top else 'xb.hdr'
      qq = 'q' if 'q' in top else 'xb.spare'
      mh = 'h' if 'h' in top and 'h' in arm else 'xb.hdr'
      mq = 'q' if 'q' in top and 'q' in arm else 'xb.spare'
      c = 'pageErased(%s + %s, %s + %s) %s' % (hh, X, qq, Y, {'le': '<= 0', 'lt': '< 1'}[test])
      ss = 's' if pn == 's' else '(xb.spare + %s)' % Y
      b = ''.join('\t\t\t%s\n' % RD[k] for k in top) + '\t\t\tif (%s) {\n' % c
      if scope == 'blk': b += '\t\t\t\tuint32_t val;\n\n'
      b += '\t\t\t\ts = xb.spare + %s;\n\t\t\t\tval = calcEcd(xb.hdr + %s, s);\n' % (Y, X)
      if pn == 'x': continue
      b += '\t\t\t\ts[12] = (s[12] & 0x3f) + (val << 6);\n\t\t\t\ts[13] = val >> 2;\n\t\t\t\ts[14] = val >> 10;\n\t\t\t\ts[15] = val >> 18;\n'
      b += ''.join('\t\t\t\t%s\n' % RD[k] for k in arm)
      b += '\t\t\t}\n\t\t\tmemcpy(raw, %s + %s, 512);\n\t\t\tmemcpy(raw + 512, %s + %s, 16);\n' % (mh, X, mq, Y)
      d = ''
      if 'h' in used: d += '\t%sh;\n' % T[th]
      if 'q' in used: d += '\t%sq;\n' % T[tq]
      if scope == 'fn': d += '\tuint32_t val;\n'
      A.append(('%s_t%s_a%s_%s%s_%s_%s' % (test, top, arm, th, tq, pn, scope), [(B, b), (D, D + d)]))
AXES = [A]
