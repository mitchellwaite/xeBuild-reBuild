# mode_client attempt 4: bpArgs without the "a"(i + 1) pin (base build/mc/b4f.c, all
# expects gone).  The pin splits i + 1 into two pseudos (attempt 2); try helper shapes
# where i + 1 is a named local used in both tests, or the index is advanced in steps.
import itertools
OLD_H = '''static char *bpArgs(int argc, char **argv, int *pi, int mode, char **arg2)
{
	int i = *pi;
	int j = i + 1;
	char *a = argv[j], *b;

	if (!a || j == argc || *a == '-')
		client_usage(3, argv[i]);
	__asm__("" :: "a"(i + 1));
	b = argv[i + 2];
	j = i + 2;
	if (j == argc || !b || *b == '-')
		client_usage(4, argv[i]);
	*arg2 = b;
	if (mode)
		client_usage(5, argv[i]);
	*pi = j;
	return argv[i + 1];
}
'''
HEAD = {
    'j': '\tint i = *pi;\n\tint j = i + 1;\n\tchar *a = argv[j], *b;\n\n',
    'jn': '\tint i = *pi;\n\tint j = i + 1;\n\tchar *a, *b;\n\n\ta = argv[j];\n',
    'f': '\tint first = *pi + 1;\n\tint j = first;\n\tchar *a = argv[j], *b;\n\n',
}
T1 = {'aj': "\tif (!a || j == argc || *a == '-')\n\t\tclient_usage(3, argv[I]);\n",
      'ja': "\tif (j == argc || !a || *a == '-')\n\t\tclient_usage(3, argv[I]);\n"}
T2 = {
    'i2': "\tb = argv[I + 2];\n\tj = I + 2;\n\tif (j == argc || !b || *b == '-')\n\t\tclient_usage(4, argv[I]);\n",
    'j2b': "\tj = I + 2;\n\tb = argv[j];\n\tif (j == argc || !b || *b == '-')\n\t\tclient_usage(4, argv[I]);\n",
    'jinc': "\tj++;\n\tb = argv[j];\n\tif (j == argc || !b || *b == '-')\n\t\tclient_usage(4, argv[I]);\n",
    'k': "\t{ int k = j + 1; b = argv[k];\n\tif (k == argc || !b || *b == '-')\n\t\tclient_usage(4, argv[I]);\n\tj = k; }\n",
}
TAIL = {'sm': '\t*arg2 = b;\n\tif (mode)\n\t\tclient_usage(5, argv[I]);\n'}
END = {'r1': '\t*pi = j;\n\treturn argv[I + 1];\n', 'ra': '\t*pi = j;\n\treturn a;\n',
       'rm': '\t*pi = j;\n\treturn argv[j - 1];\n'}
V = {}
for hk, t1, t2, ek in itertools.product(HEAD, T1, T2, END):
    I = 'i' if hk != 'f' else '(first - 1)'
    body = HEAD[hk] + T1[t1] + T2[t2] + TAIL['sm'] + END[ek]
    if hk == 'f':
        body = body.replace('I + 2', 'first + 1').replace('I + 1', 'first')
    body = body.replace('[I]', '[%s]' % I).replace('I + 2', 'i + 2').replace('I + 1', 'i + 1')
    h = 'static char *bpArgs(int argc, char **argv, int *pi, int mode, char **arg2)\n{\n' + body + '}\n'
    V['%s_%s_%s_%s' % (hk, t1, t2, ek)] = [(OLD_H, h)]
