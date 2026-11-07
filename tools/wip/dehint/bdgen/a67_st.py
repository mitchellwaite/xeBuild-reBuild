"""Attempt 67: attempt 66's sig_t (the signature helper with the type test inside, the only family with
the SE jmp block at 1) with the no-key log moved out of the helper / the key test before the call / a
tri-state return, and combinations with tl_k and p_se.
python tools/wip/dehint/bdgen/a62_semeas.py tools/wip/dehint/bdgen/a67_st.py -x -p 90   (and -x -p 99, -p 0)
python tools/wip/dehint/bdgen/a60lib.py tools/wip/dehint/bdgen/a67_st.py -p 0 -o "-;exp_pr"  (and -p 99)"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from a63_misc import T4, T5, T6, T7, FAILLOG, PASSLOG, NOKEYLOG, BODY
from a66_h import V as V66, helper, SIGBLK, COND, SIG_T, TL_K, P_SE

TT = '\tif (type != 5 && type != 17 && type != 11)\n\t\treturn 0;\n'
VER = ('\tif (!cbVerifySig(e->data, xb.pub1bl)) {\n\t\t' + FAILLOG + '\t\treturn -1;\n\t}\n'
       '\t' + PASSLOG + '\treturn 0;\n}\n')
HD = '/* the signature check of the CB-type loads (-1 if it fails) */\nstatic int checkBlSig(struct fileent *e, int type)\n{\n'
# key tested by the caller
SIG_TK = HD + TT + VER
SIG_TKN = (HD + '\tif (' + COND + ') {\n\t\tif (!cbVerifySig(e->data, xb.pub1bl)) {\n\t\t\t' + FAILLOG + '\t\t\treturn -1;\n'
           '\t\t}\n\t\t' + PASSLOG + '\t}\n\treturn 0;\n}\n')
# no key: 1 (the caller logs)
SIG_T3 = (HD.replace('(-1 if it fails)', '(-1 if it fails, 1 with no key)') + TT
          + '\tif (!xb.pub1bl)\n\t\treturn 1;\n' + VER)
# the no-key log in the helper, key test first
SIG_TKF = (HD + '\tif (!xb.pub1bl) {\n\t\tif (' + COND + ')\n\t\t\t' + NOKEYLOG + '\t\treturn 0;\n\t}\n' + TT + VER)
# the type test inside as a switch
SIG_TS = (HD + '\tswitch (type) {\n\tcase 5: case 11: case 17:\n\t\tbreak;\n\tdefault:\n\t\treturn 0;\n\t}\n'
          '\tif (!xb.pub1bl) {\n\t\t' + NOKEYLOG + '\t\treturn 0;\n\t}\n' + VER)
# r passed in (the helper returns it or -1)
SIG_TR = ('/* the signature check of the CB-type loads (-1 if it fails) */\nstatic uint32_t checkBlSig(struct fileent *e, int type, uint32_t r)\n{\n'
          + TT.replace('return 0', 'return r') + '\tif (!xb.pub1bl) {\n\t\t' + NOKEYLOG + '\t\treturn r;\n\t}\n'
          + VER.replace('return 0', 'return r'))

V = {
    'src': [],
    'sig_t': V66['sig_t'],
    'tk_else': [helper(SIG_TK), (SIGBLK, T4 + 'if (xb.pub1bl)\n' + T5 + 'r = checkBlSig(e, type);\n'
                                 + T4 + 'else if (' + COND + ')\n' + T5 + NOKEYLOG)],
    'tk_nkfirst': [helper(SIG_TK), (SIGBLK, T4 + 'if (!xb.pub1bl) {\n' + T5 + 'if (' + COND + ')\n' + T6 + NOKEYLOG
                                    + T4 + '} else\n' + T5 + 'r = checkBlSig(e, type);\n')],
    'tkn_else': [helper(SIG_TKN), (SIGBLK, T4 + 'if (xb.pub1bl)\n' + T5 + 'r = checkBlSig(e, type);\n'
                                   + T4 + 'else if (' + COND + ')\n' + T5 + NOKEYLOG)],
    't3': [helper(SIG_T3), (SIGBLK, T4 + 'r = checkBlSig(e, type);\n' + T4 + 'if (r == 1) {\n' + T5 + NOKEYLOG
                            + T5 + 'r = 0;\n' + T4 + '}\n')],
    't3b': [helper(SIG_T3), (SIGBLK, T4 + 'r = checkBlSig(e, type);\n' + T4 + 'if (r > 0) {\n' + T5 + NOKEYLOG
                             + T5 + 'r = 0;\n' + T4 + '}\n')],
    'tkf': [helper(SIG_TKF), (SIGBLK, T4 + 'r = checkBlSig(e, type);\n')],
    'ts': [helper(SIG_TS), (SIGBLK, T4 + 'r = checkBlSig(e, type);\n')],
    'tr': [helper(SIG_TR), (SIGBLK, T4 + 'r = checkBlSig(e, type, r);\n')],
}
V['sig_t_k'] = [helper(SIG_T + '\n' + TL_K), (SIGBLK, T4 + 'r = checkBlSig(e, type);\n'),
                ('setFlashBuild(getBeU16(xb.files[i].data + 2));', 'setKitBuild(e);')]
V['sig_t_se'] = [helper(SIG_T + '\n' + P_SE), (SIGBLK, T4 + 'r = checkBlSig(e, type);\n'),
                 ("if (type == 9 && e->data[0] == 'S' && e->data[1] == 'E') {", 'if (type == 9 && isSe(e->data)) {')]
V['tk_se'] = [helper(SIG_TK + '\n' + P_SE), V['tk_else'][1],
              ("if (type == 9 && e->data[0] == 'S' && e->data[1] == 'E') {", 'if (type == 9 && isSe(e->data)) {')]
