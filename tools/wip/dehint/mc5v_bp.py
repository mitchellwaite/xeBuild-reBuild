# mode_client attempt 5: bpArgs without the "a"(i + 1) pin, caller-side shapes: both
# arguments through out-parameters, the index returned, start/arg order.  Base: src.
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
OLD_C = '\t\t\targ = bpArgs(argc, argv, &i, mode, &start);\n'
BODY = '''	if (!a || j == argc || *a == '-')
		client_usage(3, argv[i]);
	b = argv[i + 2];
	j = i + 2;
	if (j == argc || !b || *b == '-')
		client_usage(4, argv[i]);
'''
V = {}
# 1. void, both out-params
for tail, tk in (('\t*arg1 = argv[i + 1];\n\t*arg2 = b;\n', 'ab'), ('\t*arg2 = b;\n\t*arg1 = argv[i + 1];\n', 'ba'),
                 ('\t*arg1 = a;\n\t*arg2 = b;\n', 'aa')):
    for mpos in ('pre', 'post'):
        m = '\tif (mode)\n\t\tclient_usage(5, argv[i]);\n'
        body = BODY + (m + tail if mpos == 'pre' else tail + m) + '\t*pi = j;\n'
        h = ('static void bpArgs(int argc, char **argv, int *pi, int mode, char **arg1, char **arg2)\n{\n'
             '\tint i = *pi;\n\tint j = i + 1;\n\tchar *a = argv[j], *b;\n\n' + body + '}\n')
        V['void_%s_%s' % (tk, mpos)] = [(OLD_H, h), (OLD_C, '\t\t\tbpArgs(argc, argv, &i, mode, &arg, &start);\n')]
# 2. returns the new index
for tail, tk in (('\t*arg1 = argv[i + 1];\n\t*arg2 = b;\n', 'ab'), ('\t*arg2 = b;\n\t*arg1 = argv[i + 1];\n', 'ba')):
    body = BODY + '\t' + tail.strip('\t').replace('\n\t', '\n\t') + '\tif (mode)\n\t\tclient_usage(5, argv[i]);\n\treturn j;\n'
    h = ('static int bpArgs(int argc, char **argv, int i, int mode, char **arg1, char **arg2)\n{\n'
         '\tint j = i + 1;\n\tchar *a = argv[j], *b;\n\n' + body + '}\n')
    V['ret_%s' % tk] = [(OLD_H, h), (OLD_C, '\t\t\ti = bpArgs(argc, argv, i, mode, &arg, &start);\n')]
# 3. plain pin removal and pin moved to caller-independent spellings
V['nopin'] = [('\t__asm__("" :: "a"(i + 1));\n', '')]
