# mode_client -i / -p without the "d" pins: default-assignment and mode-first shapes
import itertools, os, runpy
M = runpy.run_path(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'mc2v_ip.py'))
old = M['old']
ARMS = M['ARMS']


def shape(kind, msg, mode):
    log = 'log_printf(0, "%s\\n", arg);' % msg
    if kind == 'pre_pos':
        return '''arg = dummy;
			if (argv[i + 1] && i + 1 != argc && *argv[i + 1] != '-') {
				arg = argv[++i];
				%s
			}
			mode = %d;''' % (log, mode)
    if kind == 'pre_neg':
        return '''arg = dummy;
			if (!argv[i + 1] || i + 1 == argc || *argv[i + 1] == '-')
				;
			else {
				arg = argv[++i];
				%s
			}
			mode = %d;''' % (log, mode)
    if kind == 'mode_first':
        return '''mode = %d;
			if (!argv[i + 1] || i + 1 == argc || *argv[i + 1] == '-')
				arg = dummy;
			else {
				arg = argv[++i];
				%s
			}''' % (mode, log)
    if kind == 'mode_first_pre':
        return '''mode = %d;
			arg = dummy;
			if (argv[i + 1] && i + 1 != argc && *argv[i + 1] != '-') {
				arg = argv[++i];
				%s
			}''' % (mode, log)
    if kind == 'mode_in':
        return '''if (!argv[i + 1] || i + 1 == argc || *argv[i + 1] == '-') {
				arg = dummy;
				mode = %d;
			} else {
				arg = argv[++i];
				%s
				mode = %d;
			}''' % (mode, log, mode)
    if kind == 'orig':
        return '''if (!argv[i + 1] || i + 1 == argc || *argv[i + 1] == '-')
				arg = dummy;
			else {
				arg = argv[++i];
				%s
			}
			mode = %d;''' % (log, mode)


KINDS = ['orig', 'pre_pos', 'pre_neg', 'mode_first', 'mode_first_pre', 'mode_in']
V = {}
for a, b in itertools.product(KINDS, KINDS):
    V['i_%s__p_%s' % (a, b)] = [(old(*ARMS[0]), shape(a, *ARMS[0])), (old(*ARMS[1]), shape(b, *ARMS[1]))]
