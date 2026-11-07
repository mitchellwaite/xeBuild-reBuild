"""Attempt 67: a67_kit.py's k1 (the kit arm's type == 14 test and setFlashBuild in an IPA-inlined
setKitBuild(e, type), PRED_CALL on the tail test) crossed with helper bodies, call arguments, tail
spellings, the kit-first orientation and the failed arm's r = -1 order.  Labels: b<body>a<arg>t<tail>o<orient>f<fail>.
python tools/wip/dehint/bdgen/a60lib.py tools/wip/dehint/bdgen/a67_kx.py -p 0 -o "-" """
import itertools, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from a63_misc import T4, T5, T6, T7, FAILLOG
from a66_h import helper

TAILC = ('\t\t\t\t/* the expect leaves vrp1\'s signature-failed copy of this test a\n'
         '\t\t\t\t   >5 edge (else its setFlashBuild copy has frequency 0 and final\n'
         '\t\t\t\t   aligns the type-11 block after it) */\n')
OLDTAIL = (TAILC + T4 + 'if (xb.type <= BUILD_DEVGL16) {\n' + T5 + 'if (__builtin_expect(r != 0, 0))\n' + T6 + 'goto fail;\n'
           + T5 + 'break;\n' + T4 + '}\n' + T4 + 'if (type == 14)\n' + T5 + 'setFlashBuild(getBeU16(xb.files[i].data + 2));\n')
BODY = {
    '1': '\tif (type == 14)\n\t\tsetFlashBuild(getBeU16(e->data + 2));\n',
    '2': '\tif (type != 14)\n\t\treturn;\n\tsetFlashBuild(getBeU16(e->data + 2));\n',
    '3': '\tif (type == 14) {\n\t\tsetFlashBuild(getBeU16(e->data + 2));\n\t\treturn;\n\t}\n',
    '4': '\tswitch (type) {\n\tcase 14:\n\t\tsetFlashBuild(getBeU16(e->data + 2));\n\t\tbreak;\n\t}\n',
    '5': '\tif (type == 14) {\n\t\tuint16_t build = getBeU16(e->data + 2);\n\n\t\tsetFlashBuild(build);\n\t}\n',
    '6': '\tif (type != 14)\n\t\treturn;\n\telse\n\t\tsetFlashBuild(getBeU16(e->data + 2));\n',
}
ARG = {'e': 'e', 'x': '&xb.files[i]'}
TST = {'n': '(int)r < 0', 'r': 'r', 'z': 'r != 0'}


def mk(b, a, t, o, f):
    h = ('/* an SE in a kit build sets the flash build number */\n'
         'static void setKitBuild(struct fileent *e, int type)\n{\n' + BODY[b] + '}\n')
    call = 'setKitBuild(%s, type);\n' % ARG[a]
    if o == 's':
        new = (T4 + 'if (xb.type <= BUILD_DEVGL16) {\n' + T5 + 'if (' + TST[t] + ')\n' + T6 + 'goto fail;\n'
               + T5 + 'break;\n' + T4 + '}\n' + T4 + call)
    else:
        new = (T4 + 'if (xb.type > BUILD_DEVGL16) {\n' + T5 + call + T5 + 'break;\n' + T4 + '}\n'
               + T4 + 'if (' + TST[t] + ')\n' + T5 + 'goto fail;\n')
    ed = [helper(h), (OLDTAIL, new)]
    if f == 'b':
        ed.append((T7 + FAILLOG + T7 + 'r = -1;\n', T7 + 'r = -1;\n' + T7 + FAILLOG))
    return ed


V = {'src': []}
for b, a, t, o, f in itertools.product(BODY, ARG, TST, 'sk', 'ab'):
    if f == 'b' or a == 'x': continue
    V['b%sa%st%so%sf%s' % (b, a, t, o, f)] = mk(b, a, t, o, f)
H1 = ('/* an SE in a kit build sets the flash build number */\n'
      'static void setKitBuild(struct fileent *e, int type)\n{\n' + BODY['1'] + '}\n')
for t in TST:
    V['ei_' + t] = [helper(H1), (OLDTAIL, T4 + 'if (xb.type > BUILD_DEVGL16)\n' + T5 + 'setKitBuild(e, type);\n'
                                 + T4 + 'else if (' + TST[t] + ')\n' + T5 + 'goto fail;\n')]
    V['el_' + t] = [helper(H1), (OLDTAIL, T4 + 'if (xb.type <= BUILD_DEVGL16) {\n' + T5 + 'if (' + TST[t] + ')\n' + T6 + 'goto fail;\n'
                                 + T4 + '} else\n' + T5 + 'setKitBuild(e, type);\n')]
# the none test as a continue (changes the join's predecessor order)
NONE = ('\t\tif (strnicmp(e->name, "none", 4) || e->crc) {\n\t\t\tint type = e->type;\n',
        '\t\tif (!strnicmp(e->name, "none", 4) && !e->crc)\n\t\t\tcontinue;\n\t\t{\n\t\t\tint type = e->type;\n')
for k in ('src', 'b1aetnosfa', 'b1aetrosfa', 'b1aetzosfa', 'b3aetnosfa', 'b4aetnosfa'):
    V['nc_' + k] = V[k] + [NONE]
# the helper passes r through (the inlined continuation holds the return value)
HR = ('/* an SE in a kit build sets the flash build number */\n'
      'static uint32_t setKitBuild(struct fileent *e, int type, uint32_t r)\n{\n'
      '\tif (type == 14)\n\t\tsetFlashBuild(getBeU16(e->data + 2));\n\treturn r;\n}\n')
HI = ('/* an SE in a kit build sets the flash build number (1 if it did) */\n'
      'static int setKitBuild(struct fileent *e, int type)\n{\n'
      '\tif (type != 14)\n\t\treturn 0;\n\tsetFlashBuild(getBeU16(e->data + 2));\n\treturn 1;\n}\n')
TL0 = (T4 + 'if (xb.type <= BUILD_DEVGL16) {\n' + T5 + 'if ((int)r < 0)\n' + T6 + 'goto fail;\n' + T5 + 'break;\n' + T4 + '}\n')
V['rr_n'] = [helper(HR), (OLDTAIL, TL0 + T4 + 'r = setKitBuild(e, type, r);\n')]
V['ri_n'] = [helper(HI), (OLDTAIL, TL0 + T4 + 'setKitBuild(e, type);\n')]
