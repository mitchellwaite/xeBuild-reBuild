"""Attempt 68: setKitBuild (attempt 67's k1, (int)r < 0, no param) with callee bodies whose return
block gets the call path's edge before the false edge (so the inlined continuation's forwarder
redirects the false edge first and the call path ends up last at the switch join).
python tools/wip/dehint/bdgen/a68_phi.py tools/wip/dehint/bdgen/a68_kit.py
python tools/wip/dehint/bdgen/a60lib.py tools/wip/dehint/bdgen/a68_kit.py -p 0 -o "-" """
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from a63_misc import T4, T5, T6
from a66_h import helper

TAILC = ('\t\t\t\t/* the expect leaves vrp1\'s signature-failed copy of this test a\n'
         '\t\t\t\t   >5 edge (else its setFlashBuild copy has frequency 0 and final\n'
         '\t\t\t\t   aligns the type-11 block after it) */\n')
OLDTAIL = (TAILC + T4 + 'if (xb.type <= BUILD_DEVGL16) {\n' + T5 + 'if (__builtin_expect(r != 0, 0))\n' + T6 + 'goto fail;\n'
           + T5 + 'break;\n' + T4 + '}\n' + T4 + 'if (type == 14)\n' + T5 + 'setFlashBuild(getBeU16(xb.files[i].data + 2));\n')
SF = 'setFlashBuild(getBeU16(e->data + 2));\n'
BODY = {
    '1': '\tif (type == 14)\n\t\t' + SF,
    '7': '\tif (type == 14)\n\t\t' + SF + '\telse\n\t\treturn;\n',
    '8': '\tif (type == 14) {\n\t\t' + SF + '\t\treturn;\n\t}\n\treturn;\n',
    '9': '\tif (type != 14)\n\t\t;\n\telse\n\t\t' + SF,
    'a': '\tswitch (type) {\n\tcase 14:\n\t\t' + SF + '\t\treturn;\n\tdefault:\n\t\treturn;\n\t}\n',
    'b': '\tswitch (type) {\n\tdefault:\n\t\tbreak;\n\tcase 14:\n\t\t' + SF + '\t\tbreak;\n\t}\n',
    'c': '\tdo {\n\t\tif (type != 14)\n\t\t\tbreak;\n\t\t' + SF + '\t} while (0);\n',
}
TST = {'n': '(int)r < 0'}
V = {}
for b in BODY:
    for t in TST:
        h = ('/* an SE in a kit build sets the flash build number */\n'
             'static void setKitBuild(struct fileent *e, int type)\n{\n' + BODY[b] + '}\n')
        new = (T4 + 'if (xb.type <= BUILD_DEVGL16) {\n' + T5 + 'if (' + TST[t] + ')\n' + T6 + 'goto fail;\n'
               + T5 + 'break;\n' + T4 + '}\n' + T4 + 'setKitBuild(e, type);\n')
        V['b' + b + t] = [helper(h), (OLDTAIL, new)]
# no ISRA clone: a pointer argument (eipa_sra's versioning copy rebuilds the callee's edges in block
# order, which puts the false edge first in the return block's preds again)
SFB = 'setFlashBuild(getBeU16(bl + 2));\n'
BODYP = {k: v.replace(SF, SFB) for k, v in BODY.items()}
ARGS = {'d': ('const uint8_t *bl, int type', 'e->data, type'),
        't': ('int type, const uint8_t *bl', 'type, e->data'),
        'x': ('const uint8_t *bl, int type', 'xb.files[i].data, type')}
for b in BODYP:
    for a, (proto, call) in ARGS.items():
        h = ('/* an SE in a kit build sets the flash build number */\n'
             'static void setKitBuild(' + proto + ')\n{\n' + BODYP[b] + '}\n')
        new = (T4 + 'if (xb.type <= BUILD_DEVGL16) {\n' + T5 + 'if ((int)r < 0)\n' + T6 + 'goto fail;\n'
               + T5 + 'break;\n' + T4 + '}\n' + T4 + 'setKitBuild(' + call + ');\n')
        V['p' + b + a] = [helper(h), (OLDTAIL, new)]
# diagnostics: an int helper whose (unused) return value is a statement in its return block, so the
# inlined return block isn't a forwarder until DCE (after vrp1)
NEWN = (T4 + 'if (xb.type <= BUILD_DEVGL16) {\n' + T5 + 'if ((int)r < 0)\n' + T6 + 'goto fail;\n'
        + T5 + 'break;\n' + T4 + '}\n' + T4 + 'setKitBuild(e, type);\n')
for k, ret in (('type', 'type'), ('size', 'e->size'), ('xbt', 'xb.type'), ('crc', 'e->crc')):
    h = ('static int setKitBuild(struct fileent *e, int type)\n{\n' + BODY['1'] + '\treturn ' + ret + ';\n}\n')
    V['d_' + k] = [helper(h), (OLDTAIL, NEWN)]
# the d_xbt diagnostic with the setFlashBuild argument spelled as src's xb.files[i].data
for k, (proto, body, call) in {
        'x': ('const uint8_t *bl, int type', SFB, 'xb.files[i].data, type'),
        'i': ('uint32_t i, int type', 'setFlashBuild(getBeU16(xb.files[i].data + 2));\n', 'i, type'),
        'e': ('struct fileent *e, int type', SF, '&xb.files[i], type'),
}.items():
    h = ('static int setKitBuild(' + proto + ')\n{\n\tif (type == 14)\n\t\t' + body + '\treturn xb.type;\n}\n')
    V['dx_' + k] = [helper(h), (OLDTAIL, NEWN.replace('setKitBuild(e, type)', 'setKitBuild(' + call + ')'))]
# natural return values with the (i, type) helper
SFI = 'setFlashBuild(getBeU16(xb.files[i].data + 2));\n'
CALLI = NEWN.replace('setKitBuild(e, type)', 'setKitBuild(i, type)')
V['ri0'] = [helper('static int setKitBuild(uint32_t i, int type)\n{\n\tif (type == 14)\n\t\t' + SFI + '\treturn 0;\n}\n'), (OLDTAIL, CALLI)]
V['ri1'] = [helper('static int setKitBuild(uint32_t i, int type)\n{\n\tif (type != 14)\n\t\treturn 0;\n\t' + SFI + '\treturn 1;\n}\n'), (OLDTAIL, CALLI)]
V['riv'] = [helper('static void setKitBuild(uint32_t i, int type)\n{\n\tif (type == 14)\n\t\t' + SFI + '}\n'), (OLDTAIL, CALLI)]
V['rir'] = [helper('static uint32_t setKitBuild(uint32_t i, int type, uint32_t r)\n{\n\tif (type == 14)\n\t\t' + SFI + '\treturn r;\n}\n'),
            (OLDTAIL, NEWN.replace('setKitBuild(e, type);', 'r = setKitBuild(i, type, r);'))]
V['rie'] = [helper('static int setKitBuild(uint32_t i, int type)\n{\n\tif (type == 14)\n\t\t' + SFI + '\treturn xb.files[i].type;\n}\n'), (OLDTAIL, CALLI)]
# diagnostic: a goto (PRED_GOTO predict statement) in the call's continuation
T3 = '\t' * 3
JOIN = (T3 + '}\n\t\t}\n\t\tif (r) {\n', T3 + '}\n\t\t}\n\tdone:\n\t\tif (r) {\n')
V['g_k'] = [helper('static void setKitBuild(uint32_t i, int type)\n{\n\tif (type == 14)\n\t\t' + SFI + '}\n'),
            (OLDTAIL, CALLI.replace('setKitBuild(i, type);\n', 'setKitBuild(i, type);\n' + T4 + 'goto done;\n')), JOIN]
V['g_ke'] = [helper('static void setKitBuild(uint32_t i, int type)\n{\n\tif (type == 14)\n\t\t' + SFI + '\telse\n\t\tgoto out;\nout:\n\t;\n}\n'), (OLDTAIL, CALLI)]
# the kit test inside the helper, the helper called on every build; the tail tests the build
# type only for the failure
KT = {
    'h1': '\tif (xb.type > BUILD_DEVGL16 && type == 14)\n\t\t' + SFI,
    'h2': '\tif (xb.type > BUILD_DEVGL16) {\n\t\tif (type == 14)\n\t\t\t' + SFI + '\t}\n',
    'h3': '\tif (type == 14 && xb.type > BUILD_DEVGL16)\n\t\t' + SFI,
    'h4': '\tif (xb.type <= BUILD_DEVGL16)\n\t\treturn;\n\tif (type == 14)\n\t\t' + SFI,
}
KTAIL = {
    'a': T4 + 'if (xb.type <= BUILD_DEVGL16 && (int)r < 0)\n' + T5 + 'goto fail;\n' + T4 + 'setKitBuild(i, type);\n',
    'n': T4 + 'if (xb.type <= BUILD_DEVGL16) {\n' + T5 + 'if ((int)r < 0)\n' + T6 + 'goto fail;\n' + T4 + '}\n' + T4 + 'setKitBuild(i, type);\n',
    'p': T4 + 'setKitBuild(i, type);\n' + T4 + 'if (xb.type <= BUILD_DEVGL16 && (int)r < 0)\n' + T5 + 'goto fail;\n',
    'q': T4 + 'setKitBuild(i, type);\n' + T4 + 'if (xb.type <= BUILD_DEVGL16) {\n' + T5 + 'if ((int)r < 0)\n' + T6 + 'goto fail;\n' + T4 + '}\n',
}
for hk, hb in KT.items():
    for tk, tb in KTAIL.items():
        V['kt_' + hk + tk] = [helper('/* a kit build: an SE sets the flash build number */\nstatic void setKitBuild(uint32_t i, int type)\n{\n' + hb + '}\n'),
                              (OLDTAIL, tb)]
# return types of the IPA-inlined int callees whose results go into r (uint32_t): with no
# conversion their return blocks are PHI forwarders that mergephi2 merges into the switch join,
# appending edges after setKitBuild's false edge
RT = {'x': ('static int loadXell(struct fileent *e)', 'static uint32_t loadXell(struct fileent *e)'),
      'b': ('static int loadBl24(struct fileent *e)', 'static uint32_t loadBl24(struct fileent *e)'),
      'd': ('static int defaultBl60(struct fileent *e)', 'static uint32_t defaultBl60(struct fileent *e)')}
import itertools as _it
for n in (1, 2, 3):
    for ks in _it.combinations('xbd', n):
        k = ''.join(ks)
        V['rt_' + k] = V['riv'] + [RT[c] for c in ks]
        V['rt_' + k + '_e'] = V['k1n0'] + [RT[c] for c in ks] if 'k1n0' in V else None
        if V['rt_' + k + '_e'] is None:
            del V['rt_' + k + '_e']
        V['rt_' + k + '_src'] = [RT[c] for c in ks]
V['rii'] = [helper('static int setKitBuild(uint32_t i, int type, int r)\n{\n\tif (type == 14)\n\t\t' + SFI + '\treturn r;\n}\n'),
            (OLDTAIL, NEWN.replace('setKitBuild(e, type);', 'r = setKitBuild(i, type, r);'))]
# return-value spellings of the (i, type) helper (the value is unused at the call site)
for k, ret in (('q', 'type == 14'), ('n', 'xb.nFiles'), ('d', 'xb.files[i].data != NULL'), ('s', 'xb.seReplacesCf')):
    V['rv_' + k] = [helper('static int setKitBuild(uint32_t i, int type)\n{\n\tif (type == 14)\n\t\t' + SFI + '\treturn ' + ret + ';\n}\n'), (OLDTAIL, CALLI)]
# the candidate (rv_q) with the other tail spellings, and at p99
V['rv_qz'] = V['rv_q'] + [('if ((int)r < 0)\n' + T6 + 'goto fail;', 'if (r != 0)\n' + T6 + 'goto fail;')]
V['rv_qr'] = V['rv_q'] + [('if ((int)r < 0)\n' + T6 + 'goto fail;', 'if (r)\n' + T6 + 'goto fail;')]
V['rv_qe'] = V['rv_q'] + [('if ((int)r < 0)\n' + T6 + 'goto fail;', 'if (__builtin_expect(r != 0, 0))\n' + T6 + 'goto fail;')]
