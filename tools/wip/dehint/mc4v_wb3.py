# mode_client attempt 4: -wb helper with a pointer index (like getArgs), shapes around
# mc4v_wb2's pi_r1 (6 lines: the -r arm's `i + 1 == argc || !a` test order flips)
import itertools, runpy, os
W = runpy.run_path(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'mc4v_wb.py'))
WB_OLD, ANCH = W['WB_OLD'], W['ANCH']
NEW = '\t\t} else if (!strnicmp(argv[i], "-wb", 3)) {\n\t\t\targ = wbArgs(argc, argv, &i, mode, &start);\n'

HEAD = {
    'i': '\tint i = *pi;\n\tint j = i + 1;\n\tchar *a = argv[j], *b;\n\n',
    'ij': '\tint i = *pi, j = i + 1;\n\tchar *a = argv[j], *b;\n\n',
    'j': '\tint j = *pi + 1;\n\tchar *a = argv[j], *b;\n\n',
}
T1 = {
    'ja': "\tif (j == argc || !a || *a == '-')\n\t\tclient_usage(3, argv[I]);\n",
    'aj': "\tif (!a || j == argc || *a == '-')\n\t\tclient_usage(3, argv[I]);\n",
}
T2 = {
    'scoped': "\t{ int k = I + 2; b = argv[k];\n\tif (!b || k == argc || *b == '-')\n\t\tclient_usage(4, argv[I]); }\n",
    'jinc': "\tj++;\n\tb = argv[j];\n\tif (!b || j == argc || *b == '-')\n\t\tclient_usage(4, argv[I]);\n",
}
TAIL = {
    'sm': '\t*arg2 = b;\n\tif (mode)\n\t\tclient_usage(5, argv[I]);\n',
    'ms': '\tif (mode)\n\t\tclient_usage(5, argv[I]);\n\t*arg2 = b;\n',
}
END = {
    'p2r1': '\t*pi = I + 2;\n\treturn argv[I + 1];\n',
    'p2ra': '\t*pi = I + 2;\n\treturn a;\n',
    'pjr1': '\t*pi = j;\n\treturn argv[I + 1];\n',
    'pe2': '\t*pi += 2;\n\treturn argv[*pi - 1];\n',
}
V = {}
for hk, t1, t2, tk, ek in itertools.product(HEAD, T1, T2, TAIL, END):
    if ek == 'pjr1' and t2 != 'jinc':
        continue
    I = 'i' if hk != 'j' else '(j - 1)'
    body = HEAD[hk] + T1[t1] + T2[t2] + TAIL[tk] + END[ek]
    body = body.replace('I + 2', 'i + 2' if I == 'i' else 'j + 1').replace('I + 1', 'i + 1' if I == 'i' else 'j').replace('[I]', '[%s]' % I)
    h = 'static char *wbArgs(int argc, char **argv, int *pi, int mode, char **arg2)\n{\n' + body + '}\n\n'
    V['%s_%s_%s_%s_%s' % (hk, t1, t2, tk, ek)] = [(WB_OLD, NEW), (ANCH, h + ANCH)]
