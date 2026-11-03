"""gen24.py: on match.c, can the out-parameter go?  updateNand returning int (const-return predictors come back, as tools/wip/README.md predicts)."""
import os

import sw

HERE = os.path.dirname(os.path.abspath(__file__))
M = open(os.path.join(HERE, 'match.c'), newline='').read()
A = 'static void flashConsole(char *dumpDir, int *pret)'
TAIL = '\tif (ret)\n\t\t*pret = ret;\n}\n'
UN_OLD = M[M.index('static void updateNand('):M.index('int mode_update(int argc')]
assert A in M and TAIL in M
CALL = '\t\t\t\tupdateNand(dumpDir, &code);\n\t\t\t\tret = code;\n'
assert CALL in M


def v(flash_tail, flash_sig, un, call):
    return M.replace(A, flash_sig).replace(TAIL, flash_tail).replace(UN_OLD, un).replace(CALL, call)


UN1 = """static int updateNand(char *dumpDir)
{
	int ret;

	if (getConsoleFiles(dumpDir)) {
		updating = 1;
		ret = buildImage();
		if (!ret)
			return flashConsole(dumpDir);
		log_printf(0, "\\n\\n***** FATAL UPDATE ERROR: %i unable to complete NAND image\\n\\n", ret);
		return 3;
	}
	log_printf(0, "\\n\\n***** FATAL UPDATE ERROR: unable to get console unique files\\n\\n");
	return 5;
}

"""
UN2 = """static int updateNand(char *dumpDir)
{
	int ret, code;

	if (getConsoleFiles(dumpDir)) {
		updating = 1;
		ret = buildImage();
		if (!ret)
			code = flashConsole(dumpDir);
		else {
			log_printf(0, "\\n\\n***** FATAL UPDATE ERROR: %i unable to complete NAND image\\n\\n", ret);
			code = 3;
		}
	} else {
		log_printf(0, "\\n\\n***** FATAL UPDATE ERROR: unable to get console unique files\\n\\n");
		code = 5;
	}
	return code;
}

"""
F = 'static int flashConsole(char *dumpDir)'
T1 = '\treturn ret;\n}\n'
vs = [
    ('r1', v(T1, F, UN1, '\t\t\t\tret = updateNand(dumpDir);\n')),
    ('r2', v(T1, F, UN2, '\t\t\t\tret = updateNand(dumpDir);\n')),
    ('r3', v('\tif (ret)\n\t\treturn ret;\n\treturn 0;\n}\n', F, UN2, '\t\t\t\tret = updateNand(dumpDir);\n')),
]
sw.run(vs, '-O3', save='gen24')
