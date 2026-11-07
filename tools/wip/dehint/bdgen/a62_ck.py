"""Attempt 62: the checkBl result test's form and the loop's r type, for exp_pr's SE chain.
python tools/wip/dehint/bdgen/a61_semeas.py tools/wip/dehint/bdgen/a62_ck.py   (cheap)
python tools/wip/dehint/bdgen/a60lib.py tools/wip/dehint/bdgen/a62_ck.py -o "-;exp_pr"  (score)"""
CK = '''				r = checkBl(e->data, e->size, type, e->crc);
				if (r)
					break;
				if (type == 5'''
def ck(test):
    return [(CK, CK.replace('if (r)\n', 'if (%s)\n' % test))]
RDECL = ('\tfor (i = 1; i < (uint32_t)xb.nFiles; i++) {\n\t\tuint32_t r = 0;\n\n\t\te = &xb.files[i];\n\t\tif (strnicmp(e->name, "none", 4) || e->crc) {\n\t\t\tint type',
         '\tfor (i = 1; i < (uint32_t)xb.nFiles; i++) {\n\t\tint r = 0;\n\n\t\te = &xb.files[i];\n\t\tif (strnicmp(e->name, "none", 4) || e->crc) {\n\t\t\tint type')
V = {
    'src': [],
    'ck_ne': ck('r != 0'),
    'ck_neg': ck('(int)r < 0'),
    'ck_le': ck('(int)r <= -1'),
    'ck_m1': ck('(int)r <= -1 || 0'),
    'int_r': [RDECL],
    'int_ck_neg': [RDECL] + ck('r < 0'),
    'int_ck_lt0': [RDECL] + ck('r < 0') ,
    'ck_ret': [(CK, CK.replace('r = checkBl(e->data, e->size, type, e->crc);\n\t\t\t\tif (r)', 'if ((r = checkBl(e->data, e->size, type, e->crc)))'))],
    'ck_not': [(CK, CK.replace('r = checkBl(e->data, e->size, type, e->crc);\n\t\t\t\tif (r)', 'if ((r = checkBl(e->data, e->size, type, e->crc)) != 0)'))],
}
EXP = 'if (__builtin_expect(r != 0, 0))\n\t\t\t\t\t\tgoto fail;'
TN = {'tn': 'if ((int)r < 0)\n\t\t\t\t\t\tgoto fail;', 'tr': 'if (r)\n\t\t\t\t\t\tgoto fail;'}
TNI = {'tn': 'if (r < 0)\n\t\t\t\t\t\tgoto fail;', 'tr': 'if (r)\n\t\t\t\t\t\tgoto fail;'}
for k in ('ck_neg', 'int_ck_neg', 'int_r'):
    for tk in TN:
        V[k + '_' + tk] = V[k] + [(EXP, (TNI if k.startswith('int') else TN)[tk])]
