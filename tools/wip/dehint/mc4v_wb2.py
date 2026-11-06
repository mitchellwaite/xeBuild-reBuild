# mode_client attempt 4: sweep of -wb helper shapes (base build/mc/b4c.c, see mc4v_wb.py)
import itertools, runpy, os
W = runpy.run_path(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'mc4v_wb.py'))
WB_OLD, ANCH = W['WB_OLD'], W['ANCH']

DECL = {
    'aj': ('\tint j = i + 1;\n\tchar *a = argv[j], *b;\n\n', 'scoped'),
    'ajk': ('\tint j = i + 1, k = i + 2;\n\tchar *a = argv[j], *b;\n\n', 'k'),
}
T1 = {
    'ja': '\tif (j == argc || !a || *a == \'-\')\n\t\tclient_usage(3, argv[i]);\n',
}
T2 = {
    'scoped': '\t{ int k = i + 2; b = argv[k];\n\tif (!b || k == argc || *b == \'-\')\n\t\tclient_usage(4, argv[i]); }\n',
    'k': '\tb = argv[k];\n\tif (!b || k == argc || *b == \'-\')\n\t\tclient_usage(4, argv[i]);\n',
}
TAIL = {
    'sm': '\t*arg2 = b;\n\tif (mode)\n\t\tclient_usage(5, argv[i]);\n',
    'ms': '\tif (mode)\n\t\tclient_usage(5, argv[i]);\n\t*arg2 = b;\n',
}
RET = {'r1': '\treturn argv[i + 1];\n', 'ra': '\treturn a;\n', 'rj': '\treturn argv[j];\n'}
CALL = {
    'c1': '\t\t\targ = wbArgs(argc, argv, i, mode, &start);\n\t\t\ti += 2;\n',
    'c2': '\t\t\targ = wbArgs(argc, argv, i, mode, &start);\n\t\t\ti = i + 2;\n',
}
V = {}
for (dk, (d, t2k)), rk, tk, ck in itertools.product(DECL.items(), RET, TAIL, CALL):
    h = ('static char *wbArgs(int argc, char **argv, int i, int mode, char **arg2)\n{\n' + d +
         T1['ja'] + T2[t2k] + TAIL[tk] + RET[rk] + '}\n\n')
    new = '\t\t} else if (!strnicmp(argv[i], "-wb", 3)) {\n' + CALL[ck]
    V['%s_%s_%s_%s' % (dk, rk, tk, ck)] = [(WB_OLD, new), (ANCH, h + ANCH)]
# pointer-index form, like getArgs
for rk in ('r1', 'ra'):
    h = ('static char *wbArgs(int argc, char **argv, int *pi, int mode, char **arg2)\n{\n'
         '\tint i = *pi;\n\tint j = i + 1;\n\tchar *a = argv[j], *b;\n\n' + T1['ja'] + T2['scoped'] +
         TAIL['sm'] + '\t*pi = i + 2;\n' + RET[rk] + '}\n\n')
    new = '\t\t} else if (!strnicmp(argv[i], "-wb", 3)) {\n\t\t\targ = wbArgs(argc, argv, &i, mode, &start);\n'
    V['pi_' + rk] = [(WB_OLD, new), (ANCH, h + ANCH)]
