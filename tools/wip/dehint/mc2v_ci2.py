# clientInfo round 2: `if (!out) return;` + success first fixes .rdata and the tail layout;
# left: the jump-threaded copies of the bad-block head come in the other order (xor ebp).
import itertools, os, runpy
V0 = runpy.run_path(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'mc2v_ci.py'))['V']
B = V0['ret_succ_first']
CD = '''		if (createDir(dir))
			out = dir;
		else
			log_printf(0, "unable to dump details to %s, disabling\\n", dir);
'''
OPTS = {
    'cd': [(CD, '''		if (!createDir(dir))
			log_printf(0, "unable to dump details to %s, disabling\\n", dir);
		else
			out = dir;
''')],
    'cd0': [(CD, '''		if (createDir(dir) == 0)
			log_printf(0, "unable to dump details to %s, disabling\\n", dir);
		else
			out = dir;
''')],
    'bad': [('	if (bad && len) {\n', '	if (bad != NULL && len > 0) {\n')],
    'badn': [('	if (bad && len) {\n', '	if (bad && len != 0) {\n')],
    'ret_out': [('	if (!out)\n		return;\n	{\n', '	if (out == NULL)\n		return;\n	{\n')],
    'retelse': [('	if (!out)\n		return;\n	{\n', '	if (!out)\n		return;\n	else {\n')],
    'loopgt': [('i >= 0; i -= 2', 'i > -1; i -= 2')],
    'iff': [('			if (i)\n				log_printf(0, ",");\n', '			if (i > 0)\n				log_printf(0, ",");\n')],
    'dirnull': [('	if (dir) {\n		log_printf(0, "creating', '	if (dir != NULL) {\n		log_printf(0, "creating')],
}
V = {}
keys = list(OPTS)
for n in range(1, 3):
    for c in itertools.combinations(keys, n):
        if 'cd' in c and 'cd0' in c or 'bad' in c and 'badn' in c or 'ret_out' in c and 'retelse' in c:
            continue
        V['+'.join(c)] = B + sum((OPTS[k] for k in c), [])
