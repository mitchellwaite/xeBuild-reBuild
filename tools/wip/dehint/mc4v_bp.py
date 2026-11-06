# mode_client attempt 4: -bp arm as a helper call (base build/mc/b4e.c: reboot shape, -eb
# oneArg, -wb wbArgs).  With and without the "a"(i + 1) pin; shared wbArgs too.
import itertools, runpy, os
W = runpy.run_path(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'mc4v_wb.py'))
BP_OLD = W['BP_OLD']
ANCH = 'static char *wbArgs('
NEWP = '\t\t} else if (!strnicmp(argv[i], "-bp", 3)) {\n\t\t\targ = bpArgs(argc, argv, &i, mode, &start);\n'
NEWW = '\t\t} else if (!strnicmp(argv[i], "-bp", 3)) {\n\t\t\targ = wbArgs(argc, argv, &i, mode, &start);\n'
NEWV = '\t\t} else if (!strnicmp(argv[i], "-bp", 3)) {\n\t\t\targ = bpArgs(argc, argv, i, mode, &start);\n\t\t\ti += 2;\n'

T1 = {
    'orig': "\tif (!argv[i + 1] || i + 1 == argc || *argv[i + 1] == '-')\n\t\tclient_usage(3, argv[i]);\n",
    'ja': "\tif (j == argc || !a || *a == '-')\n\t\tclient_usage(3, argv[i]);\n",
    'aj': "\tif (!a || j == argc || *a == '-')\n\t\tclient_usage(3, argv[i]);\n",
}
PIN = {'pin': '\t__asm__("" :: "a"(i + 1));\n', 'np': ''}
T2 = {
    'orig': "\tb = argv[i + 2];\n\tj = i + 2;\n\tif (j == argc || !b || *b == '-')\n\t\tclient_usage(4, argv[i]);\n",
    'jinc': "\tj++;\n\tb = argv[j];\n\tif (j == argc || !b || *b == '-')\n\t\tclient_usage(4, argv[i]);\n",
    'jinc2': "\tj++;\n\tb = argv[j];\n\tif (!b || j == argc || *b == '-')\n\t\tclient_usage(4, argv[i]);\n",
    'j2': "\tj = i + 2;\n\tb = argv[j];\n\tif (j == argc || !b || *b == '-')\n\t\tclient_usage(4, argv[i]);\n",
}
TAIL = {'sm': '\t*arg2 = b;\n\tif (mode)\n\t\tclient_usage(5, argv[i]);\n',
        'ms': '\tif (mode)\n\t\tclient_usage(5, argv[i]);\n\t*arg2 = b;\n'}
END = {'pj': '\t*pi = j;\n\treturn argv[i + 1];\n', 'pjm': '\t*pi = j;\n\treturn argv[j - 1];\n'}
V = {'shared': [(BP_OLD, NEWW)]}
for t1, pk, t2, tk, ek in itertools.product(T1, PIN, T2, TAIL, END):
    head = '\tint i = *pi;\n\tint j = i + 1;\n\tchar *a = argv[j], *b;\n\n' if t1 != 'orig' else \
        '\tint i = *pi;\n\tint j;\n\tchar *b;\n\n'
    if t1 == 'orig' and t2 in ('jinc', 'jinc2'):
        head = '\tint i = *pi;\n\tint j = i + 1;\n\tchar *b;\n\n'
    body = head + T1[t1] + PIN[pk] + T2[t2] + TAIL[tk] + END[ek]
    h = 'static char *bpArgs(int argc, char **argv, int *pi, int mode, char **arg2)\n{\n' + body + '}\n\n'
    V['%s_%s_%s_%s_%s' % (t1, pk, t2, tk, ek)] = [(BP_OLD, NEWP), (ANCH, h + ANCH)]
# value-index form (like oneArg)
for pk in PIN:
    body = ('\tchar *b;\n\tint j;\n\n' + T1['orig'] + PIN[pk] + T2['orig'] + TAIL['sm'] + '\treturn argv[i + 1];\n')
    h = 'static char *bpArgs(int argc, char **argv, int i, int mode, char **arg2)\n{\n' + body + '}\n\n'
    V['val_' + pk] = [(BP_OLD, NEWV), (ANCH, h + ANCH)]
