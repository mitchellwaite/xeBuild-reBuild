# clientInfo round 3: keep `out != 0` (thread order) and get the forwarder after the tail
import os, runpy
V0 = runpy.run_path(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'mc2v_ci.py'))['V']
HINT = V0['nohint'][0]
OLD = '''	if (out) {
		strcpy(path, dir);
		strcat(path, "/nanddump.bin");
		log_printf(0, "dumping console flash to %s\\n", path);
		/* .rdata order hint (testing success first flips the branch) */
		__asm__("" :: "i"("success!\\n"));
		if (!netDumpNand(path))
			log_printf(0, "failed!\\n");
		else
			log_printf(0, "success!\\n");
	}
}'''
HEAD = '''		strcpy(path, dir);
		strcat(path, "/nanddump.bin");
		log_printf(0, "dumping console flash to %s\\n", path);
'''
S = '''		if (netDumpNand(path))
			log_printf(0, "success!\\n");
		else
			log_printf(0, "failed!\\n");
'''
F = '''		if (!netDumpNand(path))
			log_printf(0, "failed!\\n");
		else
			log_printf(0, "success!\\n");
'''
V = {
    'else_ret_s': [(OLD, '	if (out) {\n' + HEAD + S + '	} else\n		return;\n}')],
    'else_ret_f': [(OLD, '	if (out) {\n' + HEAD + F + '	} else\n		return;\n}')],
    'ret_end_s': [(OLD, '	if (out) {\n' + HEAD + S + '	}\n	return;\n}')],
    'ret_in_s': [(OLD, '	if (out) {\n' + HEAD + S + '		return;\n	}\n}')],
    'ret_in_f': [(OLD, '	if (out) {\n' + HEAD + F + '		return;\n	}\n}')],
    'neg_ret_s': [(OLD, '	if (out == NULL)\n		return;\n' + HEAD.replace('\t\t', '\t') + S.replace('\t\t', '\t'))[:2] + ('}',)],
}
V['neg_ret_s'] = [(OLD, '	if (out == NULL)\n		return;\n' + (HEAD + S).replace('\n\t', '\n').lstrip('\t') + '}')]
V['neg_ret_s'][0] = (OLD, V['neg_ret_s'][0][1].replace('return;\n' + HEAD[2:], 'return;\n\t' + HEAD[2:]))
