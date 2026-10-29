# PRED_GOTO on the HDD *success* arms (front end predicts user gotos not taken) -> error arm hotter
T = '\t\t\t\t'
EA = r'log_printf(0, "\n\n***** ERROR: cannot send avatar data when a HDD does not exist!\n");'
EC = r'log_printf(0, "\n\n***** ERROR: cannot send xbox compatibility data when a HDD does not exist!\n");'
SA = 'sendAvatarData(arg, cinfo->kernel);'
SC = 'sendCompatData(arg);'
def orig(s, e):
    return T + 'if (cinfo->hwFlags & 0x20)\n' + T + '\t' + s + '\n' + T + 'else\n' + T + '\t' + e + '\n' + T + 'break;'
def gsucc(s, e, l, test='cinfo->hwFlags & 0x20'):
    return (T + 'if (%s)\n' % test + T + '\tgoto %s;\n' % l + T + e + '\n' + T + 'break;\n'
            + '\t\t\t%s:\n' % l + T + s + '\n' + T + 'break;')
OA, OC = orig(SA, EA), orig(SC, EC)
GA, GC = gsucc(SA, EA, 'sav'), gsucc(SC, EC, 'scd')
P = '\tif (!(mode && arg)) {'
A = '({ __asm__(""); 0; })'
SEP = (P, '\tif (mode <= 0 || %s || !arg) {' % A)
VARS = [
 ('gA', [(OA, GA)]),
 ('gAC', [(OA, GA), (OC, GC)]),
 ('gAC_sep', [(OA, GA), (OC, GC), SEP]),
 ('gAC_sepE', [(OA, GA), (OC, GC), (P, '\tif (mode <= 0 || %s || E(!arg)) {' % A)]),
 ('gAC_eq', [(OA, GA), (OC, GC), (P, '\tif (!mode || %s || !arg) {' % A)]),
]
