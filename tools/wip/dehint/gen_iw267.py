# attempt 19: pin_hdr (A). calcPageEcc written out in the arm, `val = calcEcd(...)` and the four stores. If calcEcd counts as pure at estimate time the arm has no call with side effects for PRED_CALL (from memory, checked by the dump this generator is judged on), so `< 1` alone gives 27%.
# `IWB=build/iw/a19/t1.c python tools/wip/dehint/iw16sweep.py tools/wip/dehint/gen_iw267.py -n 60 -t 1`
import os, itertools
BASE = os.environ.get('IWB', 'build/iw/a19/t1.c')
X = '(b * 32 + p) * 512'; Y = '(b * 32 + p) * 16'
TOP = '\t\t\tq = xb.spare;\n\t\t\th = xb.hdr;\n'
HEAD = 'pageErased(h + %s, q + %s)' % (X, Y)
CALL = '\t\t\t\tcalcPageEcc(xb.hdr + %s, xb.spare + %s);\n' % (X, Y)
RE = '\t\t\t\tq = xb.spare;\n\t\t\t\th = xb.hdr;\n'
OLD = TOP + '\t\t\tif (!' + HEAD + ') {\n' + CALL + RE + '\t\t\t}\n\t\t\tmemcpy(raw, h + %s, 512);\n\t\t\tmemcpy(raw + 512, q + %s, 16);\n' % (X, Y)
TAIL = '\t\t\tmemcpy(raw, h + %s, 512);\n\t\t\tmemcpy(raw + 512, q + %s, 16);\n' % (X, Y)
def st(s):
    return '\t\t\t\t{s}[12] = ({s}[12] & 0x3f) + (val << 6);\n\t\t\t\t{s}[13] = val >> 2;\n\t\t\t\t{s}[14] = val >> 10;\n\t\t\t\t{s}[15] = val >> 18;\n'.format(s=s)
F = []
D = ('	uint8_t *h;\n', '	uint8_t *h;\n	uint32_t val;\n	uint8_t *ps;\n')
for tn, ecc in (('nt', '!' + HEAD), ('lt', HEAD + ' < 1'), ('le', HEAD + ' <= 0')):
    for an, a, sp in (('xx', 'xb.hdr + ' + X, 'xb.spare + ' + Y), ('lo', 'h + ' + X, '(uint8_t *)q + ' + Y)):
        ar1 = '\t\t\t\tps = %s;\n\t\t\t\tval = calcEcd(%s, ps);\n' % (sp, a) + st('ps')
        ar2 = '\t\t\t\tval = calcEcd(%s, %s);\n\t\t\t\tps = %s;\n' % (a, sp, sp) + st('ps')
        ar3 = '\t\t\t\tval = calcEcd(%s, %s);\n' % (a, sp) + st('(xb.spare + %s)' % Y)
        for sn, ar in (('p1', ar1), ('p2', ar2), ('e', ar3)):
            F.append(('%s_%s_%s' % (tn, an, sn), [(OLD, TOP + '\t\t\tif (' + ecc + ') {\n' + ar + RE + '\t\t\t}\n' + TAIL), D]))
AXES = [F]
