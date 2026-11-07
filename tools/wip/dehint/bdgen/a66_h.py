"""Attempt 66: loadBlFiles' 5..21 arm and its signature / tail region at whole-structure level, as
helpers (early- or IPA-inlined), for exp_pr and the param.  Chains first, then scores:
python tools/wip/dehint/bdgen/a62_semeas.py tools/wip/dehint/bdgen/a66_h.py -x -p 90   (expect kept, gcc's default)
python tools/wip/dehint/bdgen/a62_semeas.py tools/wip/dehint/bdgen/a66_h.py -x -p 99   (expect kept, build.sh's)
python tools/wip/dehint/bdgen/a62_semeas.py tools/wip/dehint/bdgen/a66_h.py -p 0       (tail as (int)r < 0)
python tools/wip/dehint/bdgen/a60lib.py tools/wip/dehint/bdgen/a66_h.py -p 0 -o "-;exp_pr"
Helpers go before loadBlFiles (HELP marker)."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from a63_misc import T4, T5, T6, T7, FAILLOG, PASSLOG, NOKEYLOG, BODY, SE

HELP = '/* load the input files by their type; the arms only set r, which is\n'
SIGBLK = T4 + 'if (type == 5 || type == 17 || type == 11) {\n' + BODY + T4 + '}\n'
COND = 'type == 5 || type == 17 || type == 11'
LOAD = T4 + 'r = loadInputFile(e->name, e, 1, 0, NULL, 0, 0, 1);\n'
FB = (T4 + 'if (r) {\n' + T5 + 'if (type == 9) {\n' + T6 + 'if (suGetCF(&e->data, &e->size))\n' + T7 + 'r = 0;\n'
      + T5 + '} else if (type == 10) {\n' + T6 + 'if (suGetCG(&e->data, &e->size))\n' + T7 + 'r = 0;\n' + T5 + '}\n' + T4 + '}\n')
BRK = T4 + 'if (r)\n' + T5 + 'break;\n'
CK = T4 + 'r = checkBl(e->data, e->size, type, e->crc);\n'
TAILC = ('\t\t\t\t/* the expect leaves vrp1\'s signature-failed copy of this test a\n'
         '\t\t\t\t   >5 edge (else its setFlashBuild copy has frequency 0 and final\n'
         '\t\t\t\t   aligns the type-11 block after it) */\n')
TAIL = (T4 + 'if (xb.type <= BUILD_DEVGL16) {\n' + T5 + 'if (__builtin_expect(r != 0, 0))\n' + T6 + 'goto fail;\n'
        + T5 + 'break;\n' + T4 + '}\n' + T4 + 'if (type == 14)\n' + T5 + 'setFlashBuild(getBeU16(xb.files[i].data + 2));\n'
        + T4 + 'break;\n')
# console's 9/10/.. arm
CFB = ('\t\t\t\tif (r) {\n\t\t\t\t\tif (type == 9) {\n\t\t\t\t\t\tif (suGetCF(&e->data, &e->size))\n\t\t\t\t\t\t\tr = 0;\n'
       '\t\t\t\t\t} else if (type == 10) {\n\t\t\t\t\t\tif (suGetCG(&e->data, &e->size))\n\t\t\t\t\t\t\tr = 0;\n'
       '\t\t\t\t\t}\n\t\t\t\t}\n\t\t\t\tif (!r)\n\t\t\t\t\tr = checkBl(e->data, e->size, type, e->crc);\n')
C6 = (T4 + 'r = loadInputFile(e->name, e, 1, 0, NULL, 0, 0, 1);\n' + T4 + 'if (!r)\n' + T5 + 'r = checkBl(e->data, e->size, 6, e->crc);\n')

L1 = lambda s: s.replace('\t' * 7, '\t\t\t').replace('\t' * 6, '\t\t').replace('\t' * 5, '\t')


def helper(code):
    return (HELP, code + '\n' + HELP)


# ---- signature check helpers ----
SIG_ER = ('/* the signature check of a CB-type load (-1 if it fails) */\n'
          'static int checkBlSig(struct fileent *e)\n{\n'
          '\tif (!xb.pub1bl) {\n\t\t' + NOKEYLOG + '\t\treturn 0;\n\t}\n'
          '\tif (!cbVerifySig(e->data, xb.pub1bl)) {\n\t\t' + FAILLOG + '\t\treturn -1;\n\t}\n'
          '\t' + PASSLOG + '\treturn 0;\n}\n')
SIG_NR = ('/* the signature check of a CB-type load (-1 if it fails) */\n'
          'static int checkBlSig(struct fileent *e)\n{\n\tint r = 0;\n\n'
          '\tif (xb.pub1bl) {\n\t\tif (!cbVerifySig(e->data, xb.pub1bl)) {\n\t\t\t' + FAILLOG + '\t\t\tr = -1;\n'
          '\t\t} else\n\t\t\t' + PASSLOG + '\t} else\n\t\t' + NOKEYLOG + '\treturn r;\n}\n')
SIG_OK = ('/* the signature check of a CB-type load (0 if it fails) */\n'
          'static int sigOk(struct fileent *e)\n{\n'
          '\tif (!xb.pub1bl) {\n\t\t' + NOKEYLOG + '\t\treturn 1;\n\t}\n'
          '\tif (!cbVerifySig(e->data, xb.pub1bl)) {\n\t\t' + FAILLOG + '\t\treturn 0;\n\t}\n'
          '\t' + PASSLOG + '\treturn 1;\n}\n')
SIG_OKN = ('/* the signature check of a CB-type load (0 if it fails) */\n'
           'static int sigOk(struct fileent *e)\n{\n'
           '\tif (xb.pub1bl) {\n\t\tif (!cbVerifySig(e->data, xb.pub1bl)) {\n\t\t\t' + FAILLOG + '\t\t\treturn 0;\n'
           '\t\t}\n\t\t' + PASSLOG + '\t} else\n\t\t' + NOKEYLOG + '\treturn 1;\n}\n')
SIG_T = ('/* the signature check of the CB-type loads (-1 if it fails) */\n'
         'static int checkBlSig(struct fileent *e, int type)\n{\n'
         '\tif (type != 5 && type != 17 && type != 11)\n\t\treturn 0;\n'
         '\tif (!xb.pub1bl) {\n\t\t' + NOKEYLOG + '\t\treturn 0;\n\t}\n'
         '\tif (!cbVerifySig(e->data, xb.pub1bl)) {\n\t\t' + FAILLOG + '\t\treturn -1;\n\t}\n'
         '\t' + PASSLOG + '\treturn 0;\n}\n')
SIG_TN = ('/* the signature check of the CB-type loads (-1 if it fails) */\n'
          'static int checkBlSig(struct fileent *e, int type)\n{\n\tint r = 0;\n\n'
          '\tif (' + COND + ') {\n' + L1(BODY) + '\t}\n\treturn r;\n}\n')
SIG_BN = ('/* the signature check of a CB-type bootloader (-1 if it fails) */\n'
          'static int checkBlSig(uint8_t *bl, const char *name)\n{\n'
          '\tif (!xb.pub1bl) {\n\t\t' + NOKEYLOG.replace('e->name', 'name') + '\t\treturn 0;\n\t}\n'
          '\tif (!cbVerifySig(bl, xb.pub1bl)) {\n\t\t' + FAILLOG.replace('e->name', 'name') + '\t\treturn -1;\n\t}\n'
          '\t' + PASSLOG.replace('e->name', 'name') + '\treturn 0;\n}\n')
# the key test stays in the caller; the helper is the verify + its two logs
SIG_V = ('/* verify a CB-type load (-1 if it fails) */\n'
         'static int verifyBl(struct fileent *e)\n{\n'
         '\tif (!cbVerifySig(e->data, xb.pub1bl)) {\n\t\t' + FAILLOG + '\t\treturn -1;\n\t}\n'
         '\t' + PASSLOG + '\treturn 0;\n}\n')
SIG_VOK = ('/* verify a CB-type load and log the result */\n'
           'static int verifyBl(struct fileent *e)\n{\n'
           '\tint ok = cbVerifySig(e->data, xb.pub1bl);\n\n'
           '\tif (!ok)\n\t\t' + FAILLOG + '\telse\n\t\t' + PASSLOG + '\treturn ok;\n}\n')

V = {
    'src': [],
    'sig_er': [helper(SIG_ER), (SIGBLK, T4 + 'if (' + COND + ')\n' + T5 + 'r = checkBlSig(e);\n')],
    'sig_nr': [helper(SIG_NR), (SIGBLK, T4 + 'if (' + COND + ')\n' + T5 + 'r = checkBlSig(e);\n')],
    'sig_ok': [helper(SIG_OK), (SIGBLK, T4 + 'if ((' + COND + ') && !sigOk(e))\n' + T5 + 'r = -1;\n')],
    'sig_okn': [helper(SIG_OKN), (SIGBLK, T4 + 'if ((' + COND + ') && !sigOk(e))\n' + T5 + 'r = -1;\n')],
    'sig_oknest': [helper(SIG_OK), (SIGBLK, T4 + 'if (' + COND + ') {\n' + T5 + 'if (!sigOk(e))\n' + T6 + 'r = -1;\n' + T4 + '}\n')],
    'sig_t': [helper(SIG_T), (SIGBLK, T4 + 'r = checkBlSig(e, type);\n')],
    'sig_tn': [helper(SIG_TN), (SIGBLK, T4 + 'r = checkBlSig(e, type);\n')],
    'sig_bn': [helper(SIG_BN), (SIGBLK, T4 + 'if (' + COND + ')\n' + T5 + 'r = checkBlSig(e->data, e->name);\n')],
    'sig_v': [helper(SIG_V), (SIGBLK, T4 + 'if (' + COND + ') {\n' + T5 + 'if (xb.pub1bl)\n' + T6 + 'r = verifyBl(e);\n'
                                  + T5 + 'else\n' + T6 + NOKEYLOG + T4 + '}\n')],
    'sig_vok': [helper(SIG_VOK), (SIGBLK, T4 + 'if (' + COND + ') {\n' + T5 + 'if (xb.pub1bl) {\n' + T6 + 'if (!verifyBl(e))\n'
                                      + T7 + 'r = -1;\n' + T5 + '} else\n' + T6 + NOKEYLOG + T4 + '}\n')],
}

# ---- the tail as a helper ----
TL_FIN = ('/* a kit build takes its flash build number from the SE */\n'
          'static void setKitBuild(struct fileent *e, int type)\n{\n'
          '\tif (xb.type > BUILD_DEVGL16 && type == 14)\n\t\tsetFlashBuild(getBeU16(e->data + 2));\n}\n')
TL_R = ('/* the end of a CB / CF load: a kit build takes its flash build number from the SE */\n'
        'static uint32_t finishBl(struct fileent *e, int type, uint32_t r)\n{\n'
        '\tif (xb.type <= BUILD_DEVGL16)\n\t\treturn r;\n'
        '\tif (type == 14)\n\t\tsetFlashBuild(getBeU16(e->data + 2));\n\treturn r;\n}\n')
TL_K = ('/* a kit build takes its flash build number from the SE */\n'
        'static void setKitBuild(struct fileent *e)\n{\n'
        '\tsetFlashBuild(getBeU16(e->data + 2));\n}\n')
V.update({
    'tl_fin': [helper(TL_FIN), (TAILC + TAIL, T4 + 'if (r)\n' + T5 + 'goto fail;\n' + T4 + 'setKitBuild(e, type);\n' + T4 + 'break;\n')],
    'tl_fin2': [helper(TL_FIN), (TAILC + TAIL, T4 + 'setKitBuild(e, type);\n' + T4 + 'break;\n')],
    'tl_r': [helper(TL_R), (TAILC + TAIL, T4 + 'r = finishBl(e, type, r);\n' + T4 + 'break;\n')],
    'tl_k': [helper(TL_K), ('setFlashBuild(getBeU16(xb.files[i].data + 2));', 'setKitBuild(e);')],
})

# ---- the CF/CG fallback as a helper, both loaders ----
FB_H = ('/* the CF or CG from the system update when the file couldn\'t be read */\n'
        'static int useSuBl(struct fileent *e, int type)\n{\n'
        '\tif (type == 9)\n\t\treturn suGetCF(&e->data, &e->size);\n'
        '\tif (type == 10)\n\t\treturn suGetCG(&e->data, &e->size);\n\treturn 0;\n}\n')
FB_HN = ('/* the CF or CG from the system update when the file couldn\'t be read */\n'
         'static int useSuBl(struct fileent *e, int type)\n{\n\tint ok = 0;\n\n'
         '\tif (type == 9)\n\t\tok = suGetCF(&e->data, &e->size);\n'
         '\telse if (type == 10)\n\t\tok = suGetCG(&e->data, &e->size);\n\treturn ok;\n}\n')
FB_R = ('/* the CF or CG from the system update when the file couldn\'t be read */\n'
        'static uint32_t suFallback(struct fileent *e, int type, uint32_t r)\n{\n'
        '\tif (type == 9) {\n\t\tif (suGetCF(&e->data, &e->size))\n\t\t\tr = 0;\n'
        '\t} else if (type == 10) {\n\t\tif (suGetCG(&e->data, &e->size))\n\t\t\tr = 0;\n\t}\n\treturn r;\n}\n')
FBC_NEST = T4 + 'if (r) {\n' + T5 + 'if (useSuBl(e, type))\n' + T6 + 'r = 0;\n' + T4 + '}\n'
FBC_AND = T4 + 'if (r && useSuBl(e, type))\n' + T5 + 'r = 0;\n'
FBC_R = T4 + 'if (r)\n' + T5 + 'r = suFallback(e, type, r);\n'
CK_C = '\t\t\t\tif (!r)\n\t\t\t\t\tr = checkBl(e->data, e->size, type, e->crc);\n'
for lab, h, c in (('fb_nest', FB_H, FBC_NEST), ('fb_and', FB_H, FBC_AND), ('fbn_nest', FB_HN, FBC_NEST),
                  ('fbn_and', FB_HN, FBC_AND), ('fb_r', FB_R, FBC_R)):
    V[lab] = [helper(h), (FB, c, 2)]
    V[lab + '_1'] = [helper(h), (FB, c, 1)]

# ---- the 5..21 arm's load (+ fallback, SE, checkBl) as a helper ----
LD_H = ('/* load a CB / CD / CE / CF / CG-type file (a CF or CG from the system\n'
        '   update if it can\'t be read), and check it */\n'
        'static uint32_t loadUpdBl(struct fileent *e, int type)\n{\n'
        '\tuint32_t r;\n\n' + L1(LOAD + FB + BRK).replace('break;', 'return r;')
        + L1(SE) + '\treturn checkBl(e->data, e->size, type, e->crc);\n}\n')
LD_C = T4 + 'r = loadUpdBl(e, type);\n' + T4 + 'if (r)\n' + T5 + 'break;\n' + T4 + 'type = e->type;\n'
LD2_H = ('/* load a bootloader file (a CF or CG from the system update if it\n'
         '   can\'t be read) */\n'
         'static uint32_t loadSuBl(struct fileent *e, int type)\n{\n'
         '\tuint32_t r;\n\n' + L1(LOAD + FB) + '\treturn r;\n}\n')
LD2_C = T4 + 'r = loadSuBl(e, type);\n'
CK_H = ('/* check a loaded bootloader */\n'
        'static uint32_t checkEntry(struct fileent *e, int type)\n{\n'
        '\treturn checkBl(e->data, e->size, type, e->crc);\n}\n')
LC_H = ('/* load a bootloader file and check it */\n'
        'static uint32_t loadChecked(struct fileent *e, int type)\n{\n'
        '\tuint32_t r = loadInputFile(e->name, e, 1, 0, NULL, 0, 0, 1);\n\n'
        '\tif (!r)\n\t\tr = checkBl(e->data, e->size, type, e->crc);\n\treturn r;\n}\n')
V.update({
    'ld_all': [helper(LD_H), (LOAD + FB + BRK + SE + CK + BRK, LD_C)],
    'ld_su': [helper(LD2_H), (LOAD + FB, LD2_C)],
    'ld_su2': [helper(LD2_H), (LOAD + FB, LD2_C, 2)],
    'ck_all': [helper(CK_H), (CK, T4 + 'r = checkEntry(e, type);\n'), ('r = checkBl(e->data, e->size, 6, e->crc);', 'r = checkEntry(e, 6);'),
               ('\t\t\t\t\tr = checkBl(e->data, e->size, type, e->crc);\n\t\t\t\tbreak;', '\t\t\t\t\tr = checkEntry(e, type);\n\t\t\t\tbreak;')],
    'lc_6': [helper(LC_H), (C6, T4 + 'r = loadChecked(e, 6);\n')],
})

# ---- the whole 5..21 arm as a helper (IPA-inlined, its own early-return profile) ----
ARM = LOAD + FB + BRK + SE + CK + BRK + SIGBLK + TAILC + TAIL
SIGR = L1(SIGBLK)
W_HEAD = ('/* load a CB / CD / CE / CF / CG-type file (a CF or CG from the system\n'
          '   update if it can\'t be read), check it and its signature */\n'
          'static uint32_t loadCbBl(struct fileent *e, int type)\n{\n\tuint32_t r;\n\n')
W_BODY = (L1(LOAD + FB + BRK).replace('break;', 'return r;') + L1(SE) + L1(CK + BRK).replace('break;', 'return r;'))
W1 = (W_HEAD + W_BODY + SIGR
      + '\tif (xb.type <= BUILD_DEVGL16)\n\t\treturn r;\n\tif (type == 14)\n\t\tsetFlashBuild(getBeU16(e->data + 2));\n\treturn r;\n}\n')
W2 = (W_HEAD + W_BODY
      + SIGR.replace('\t\t\t\tr = -1;\n', '\t\t\t\treturn -1;\n')
      + '\tif (xb.type > BUILD_DEVGL16 && type == 14)\n\t\tsetFlashBuild(getBeU16(e->data + 2));\n\treturn 0;\n}\n')
W3 = (W_HEAD + W_BODY + SIGR
      + '\tif (xb.type <= BUILD_DEVGL16)\n\t\treturn r;\n\tif (type == 14)\n\t\tsetFlashBuild(getBeU16(e->data + 2));\n\treturn 0;\n}\n')
W4 = (W_HEAD + W_BODY + SIGR
      + '\tif (xb.type > BUILD_DEVGL16 && type == 14)\n\t\tsetFlashBuild(getBeU16(e->data + 2));\n\treturn r;\n}\n')
for lab, w in (('w1', W1), ('w2', W2), ('w3', W3), ('w4', W4)):
    V[lab] = [helper(w), (ARM, T4 + 'r = loadCbBl(e, type);\n' + T4 + 'break;\n')]
    V[lab + 'f'] = [helper(w), (ARM, T4 + 'r = loadCbBl(e, type);\n' + T4 + 'if (r && xb.type <= BUILD_DEVGL16)\n' + T5 + 'goto fail;\n' + T4 + 'break;\n')]

# ---- call-free predicates (einlined before profile_estimate, like useBuiltIn) ----
P_SIG = ('/* the bootloaders with a 1BL signature */\nstatic int isSigBl(int type)\n{\n'
         '\treturn type == 5 || type == 17 || type == 11;\n}\n')
P_SIGI = ('/* the bootloaders with a 1BL signature */\nstatic int isSigBl(int type)\n{\n'
          '\tif (type == 5 || type == 17 || type == 11)\n\t\treturn 1;\n\treturn 0;\n}\n')
P_KIT = ('/* a retail or glitch build (a failed signature stops it) */\nstatic int isRetailGlitch(void)\n{\n'
         '\treturn xb.type <= BUILD_DEVGL16;\n}\n')
P_SE = ('/* an SE (not a CF) in the CF slot */\nstatic int isSe(const uint8_t *d)\n{\n'
        '\treturn d[0] == \'S\' && d[1] == \'E\';\n}\n')
V.update({
    'p_sig': [helper(P_SIG), (SIGBLK[:SIGBLK.index('\n') + 1], T4 + 'if (isSigBl(type)) {\n')],
    'p_sigi': [helper(P_SIGI), (SIGBLK[:SIGBLK.index('\n') + 1], T4 + 'if (isSigBl(type)) {\n')],
    'p_kit': [helper(P_KIT), ('if (xb.type <= BUILD_DEVGL16) {\n' + T5 + 'if (__builtin_expect', 'if (isRetailGlitch()) {\n' + T5 + 'if (__builtin_expect')],
    'p_se': [helper(P_SE), ("if (type == 9 && e->data[0] == 'S' && e->data[1] == 'E') {", 'if (type == 9 && isSe(e->data)) {')],
})
