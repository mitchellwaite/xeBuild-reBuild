# attempt 19: pin_hdr (A). PRED_CALL only reads the arm's first block (q.c probes; the rule itself is from memory), so an arm that starts with the ECD loop itself has no call there, and the page test's opcode prediction alone (27% for `< 1`, `> 0`) falls in (A)'s window. pageEccOk already holds a hand copy of that loop.
# `IWB=build/iw/a19/t1.c python tools/wip/dehint/iw16sweep.py tools/wip/dehint/gen_iw266.py -n 40 -t 1`
import os, itertools
BASE = os.environ.get('IWB', 'build/iw/a19/t1.c')
X = '(b * 32 + p) * 512'; Y = '(b * 32 + p) * 16'
TOP = '\t\t\tq = xb.spare;\n\t\t\th = xb.hdr;\n'
HEAD = 'pageErased(h + %s, q + %s)' % (X, Y)
CALL = '\t\t\t\tcalcPageEcc(xb.hdr + %s, xb.spare + %s);\n' % (X, Y)
RE = '\t\t\t\tq = xb.spare;\n\t\t\t\th = xb.hdr;\n'
OLD = TOP + '\t\t\tif (!' + HEAD + ') {\n' + CALL + RE + '\t\t\t}\n\t\t\tmemcpy(raw, h + %s, 512);\n\t\t\tmemcpy(raw + 512, q + %s, 16);\n' % (X, Y)
TAIL = '\t\t\tmemcpy(raw, h + %s, 512);\n\t\t\tmemcpy(raw + 512, q + %s, 16);\n' % (X, Y)
def inl(d, sp):
    return ('\t\t\t\tdata = (unsigned int *)%s;\n\t\t\t\tval = 0;\n\t\t\t\tv = 0;\n\t\t\t\tfor (i = 0; i < 0x1066; i++) {\n\t\t\t\t\tif (!(i & 31)) {\n\t\t\t\t\t\tif (i == 0x1000)\n\t\t\t\t\t\t\tdata = (unsigned int *)%s;\n\t\t\t\t\t\tv = ~*data++;\n\t\t\t\t\t}\n\t\t\t\t\tval ^= v & 1;\n\t\t\t\t\tv >>= 1;\n\t\t\t\t\tif (val & 1)\n\t\t\t\t\t\tval ^= 0x6954559;\n\t\t\t\t\tval >>= 1;\n\t\t\t\t}\n\t\t\t\tval = ~val;\n' % (d, sp))
def stores(s):
    return '\t\t\t\t{s}[12] = ({s}[12] & 0x3f) + (val << 6);\n\t\t\t\t{s}[13] = val >> 2;\n\t\t\t\t{s}[14] = val >> 10;\n\t\t\t\t{s}[15] = val >> 18;\n'.format(s=s)
F = []
DECL = ('	uint8_t *h;\n', '	uint8_t *h;\n	unsigned int val, v, *data;\n	uint8_t *ps;\n')
for tn, ecc in (('nt', '!' + HEAD), ('lt', HEAD + ' < 1'), ('le', HEAD + ' <= 0')):
    for hn, a, sp in (('xb', 'xb.hdr + ' + X, 'xb.spare + ' + Y), ('loc', 'h + ' + X, 'q + ' + Y)):
        for sn in ('ps', 'cast'):
            if sn == 'ps':
                ar = '\t\t\t\tps = %s;\n' % sp + inl(a, 'ps') + stores('ps')
            else:
                ar = inl(a, sp) + stores('(xb.spare + %s)' % Y)
            F.append(('%s_%s_%s' % (tn, hn, sn), [(OLD, TOP + '\t\t\tif (' + ecc + ') {\n' + ar + RE + '\t\t\t}\n' + TAIL), DECL]))
    # else form: erased test positive
    pass
AXES = [F]
