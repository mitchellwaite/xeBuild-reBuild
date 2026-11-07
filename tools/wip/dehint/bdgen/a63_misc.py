"""Attempt 63: natural edits in loadBlFiles' 5..21 arm not in attempt 62's a62_s.py, for target A
(exp_pr kept, no --param): the SE chain at p90 first, then the score with no param.
python tools/wip/dehint/bdgen/a62_semeas.py tools/wip/dehint/bdgen/a63_misc.py -x -p 90
python tools/wip/dehint/bdgen/a60lib.py tools/wip/dehint/bdgen/a63_misc.py -p 0 -o "-" """
T4, T5, T6, T7 = '\t' * 4, '\t' * 5, '\t' * 6, '\t' * 7
SIG = T4 + 'if (type == 5 || type == 17 || type == 11) {\n'
PUB = T5 + 'if (xb.pub1bl) {\n' + T6 + 'if (!cbVerifySig(e->data, xb.pub1bl)) {\n'
FAILLOG = 'log_printf(0, "\\n***** ERROR: loaded %s, but signature check failed!\\n", e->name);\n'
PASSLOG = 'log_printf(1, "loaded %s, signature check passed!\\n", e->name);\n'
NOKEYLOG = 'log_printf(1, "loaded %s, could not check signature rsa key not present!\\n", e->name);\n'
BODY = (T5 + 'if (xb.pub1bl) {\n' + T6 + 'if (!cbVerifySig(e->data, xb.pub1bl)) {\n' + T7 + FAILLOG + T7 + 'r = -1;\n'
        + T6 + '} else\n' + T7 + PASSLOG + T5 + '} else\n' + T6 + NOKEYLOG)
SE = (T4 + "if (type == 9 && e->data[0] == 'S' && e->data[1] == 'E') {\n" + T5 + '/* an SE where the CF goes */\n'
      + T5 + 'e->type = type = 14;\n' + T5 + 'xb.cfLdv = 0;\n' + T5 + 'xb.seReplacesCf = 1;\n' + T4 + '}\n')
CK = T4 + 'r = checkBl(e->data, e->size, type, e->crc);\n'
V = {
    'src': [],
    'sig_etype': [(SIG, T4 + 'if (e->type == 5 || e->type == 17 || e->type == 11) {\n')],
    'ck_etype': [(CK, T4 + 'r = checkBl(e->data, e->size, e->type, e->crc);\n')],
    'type_uns': [('\t\t\tint type = e->type;\n\n\t\t\tswitch (type) {\n\t\t\tcase 5: case 7:',
                  '\t\t\tunsigned type = e->type;\n\n\t\t\tswitch (type) {\n\t\t\tcase 5: case 7:')],
    'se_order': [(SE, SE.replace(T5 + 'e->type = type = 14;\n' + T5 + 'xb.cfLdv = 0;\n' + T5 + 'xb.seReplacesCf = 1;\n',
                                 T5 + 'xb.cfLdv = 0;\n' + T5 + 'xb.seReplacesCf = 1;\n' + T5 + 'e->type = type = 14;\n'))],
    'se_split': [(SE, SE.replace('e->type = type = 14;', 'type = 14;\n' + T5 + 'e->type = 14;'))],
    'se_nested': [(SE, T4 + "if (type == 9) {\n" + T5 + "if (e->data[0] == 'S' && e->data[1] == 'E') {\n" + T6 + '/* an SE where the CF goes */\n'
                   + T6 + 'e->type = type = 14;\n' + T6 + 'xb.cfLdv = 0;\n' + T6 + 'xb.seReplacesCf = 1;\n' + T5 + '}\n' + T4 + '}\n')],
    'sig_switch': [(SIG + BODY + T4 + '}\n', T4 + 'switch (type) {\n' + T4 + 'case 5: case 11: case 17:\n' + BODY + T4 + '}\n')],
    'pub_local': [(BODY, T5 + '{\n' + T6 + 'const uint8_t *key = xb.pub1bl;\n\n' + T6 + 'if (key) {\n' + T7 + 'if (!cbVerifySig(e->data, key)) {\n'
                   + T7 + '\t' + FAILLOG + T7 + '\tr = -1;\n' + T7 + '} else\n' + T7 + '\t' + PASSLOG + T6 + '} else\n' + T7 + NOKEYLOG + T5 + '}\n')],
    'nokey_first': [(BODY, T5 + 'if (!xb.pub1bl)\n' + T6 + NOKEYLOG + T5 + 'else if (!cbVerifySig(e->data, xb.pub1bl)) {\n'
                     + T6 + FAILLOG + T6 + 'r = -1;\n' + T5 + '} else\n' + T6 + PASSLOG)],
    'ver_flat': [(BODY, T5 + 'if (xb.pub1bl && !cbVerifySig(e->data, xb.pub1bl)) {\n' + T6 + FAILLOG + T6 + 'r = -1;\n'
                  + T5 + '} else if (xb.pub1bl)\n' + T6 + PASSLOG + T5 + 'else\n' + T6 + NOKEYLOG)],
    'pass_first': [(BODY, T5 + 'if (xb.pub1bl) {\n' + T6 + 'if (cbVerifySig(e->data, xb.pub1bl))\n' + T7 + PASSLOG + T6 + 'else {\n'
                    + T7 + FAILLOG + T7 + 'r = -1;\n' + T6 + '}\n' + T5 + '} else\n' + T6 + NOKEYLOG)],
}
