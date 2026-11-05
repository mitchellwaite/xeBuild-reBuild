# Types, the most productive lever so far (int size, int crc).  BDW picks a function; its hints are off.
import os
w = os.environ.get('BDW', 'lfc')
if w == 'lfc':
    REMOVE = ['pin_e'] if os.environ.get('BDK') else ['pin_e', 'exp_verbose']
    FOCUS = ['_loadFileCrc']
    S = 'int loadFileCrc(const char *name, struct fileent *e, int verbose, int pad, uint32_t crc)'
    def both(a, b):
        return [(S + ';', S.replace(a, b) + ';'), (S + '\n{', S.replace(a, b) + '\n{')]
    AXES = [
        [('', []), ('ci', both('uint32_t crc', 'int crc'))],
        [('', []), ('pu', [(S, S.replace('int pad', 'uint32_t pad'))])],
        [('', []), ('vu', [(S, S.replace('int verbose', 'uint32_t verbose'))]), ('vb', [(S, S.replace('int verbose', 'char verbose'))])],
        [('', []), ('su', [('	size_t size;\n	uint32_t c;\n', '	uint32_t size;\n	uint32_t c;\n')]),
         ('si', [('	size_t size;\n	uint32_t c;\n', '	int size;\n	uint32_t c;\n')])],
    ]
elif w == 'cba':
    REMOVE = ['pin_size']
    FOCUS = ['_calcBlAreaSize']
    D = '	uint32_t size, xs, x;\n'
    AXES = [[('', []), ('xi', [(D, '	uint32_t size, xs;\n	int x;\n')]), ('si', [(D, '	int size;\n	uint32_t xs, x;\n')]),
             ('sxi', [(D, '	int size, x;\n	uint32_t xs;\n')]), ('axi', [(D, '	int size, xs, x;\n')])],
            [('', []), ('ru', [('uint32_t calcBlAreaSize(void)', 'int calcBlAreaSize(void)')])]]
elif w == 'smc':
    REMOVE = ['nei_smc', 'cb1', 'cb2', 'cb3', 'cb4']
    FOCUS = ['_patchSmcConfig']
    D = '	uint32_t patched = 0;\n	int i, dead;\n'
    R = 'int iniRangeOk(const char *name, uint32_t v, uint32_t lo, uint32_t hi)'
    AXES = [
        [('', []), ('pi', [(D, '	int patched = 0;\n	int i, dead;\n')]), ('pb', [(D, '	char patched = 0;\n	int i, dead;\n')])],
        [('', []), ('vi', [(R, R.replace('uint32_t v', 'int v'))]), ('ai', [(R, R.replace('uint32_t v, uint32_t lo, uint32_t hi', 'int v, int lo, int hi'))]),
         ('li', [(R, R.replace('uint32_t lo, uint32_t hi', 'int lo, int hi'))])],
    ]
elif w == 'chk':
    REMOVE = ['pin_type', 'pin_m']
    FOCUS = ['_checkBl']
    D = '	uint32_t blsize, c;\n	int m, dead;\n'
    AXES = [
        [('', []), ('mu', [(D, '	uint32_t blsize, c;\n	uint32_t m;\n	int dead;\n')]), ('mb', [(D, '	uint32_t blsize, c;\n	uint8_t m;\n	int dead;\n')])],
        [('', []), ('bi', [('	uint32_t blsize, c;\n', '	int blsize;\n	uint32_t c;\n')])],
        [('', []), ('ts', [('int checkBl(uint8_t *bl, uint32_t size, int type, uint32_t crc)', 'int checkBl(uint8_t *bl, int size, int type, uint32_t crc)')])],
    ]
elif w == 'lb':
    REMOVE = ['exp_t10', 'lab_t5le', 'exp_pr', 'lab_badsize', 'pin_d']
    FOCUS = ['_loadBlFiles']
    S = 'static void loadBl(struct fileent *e, uint32_t i, uint32_t *pr)'
    LF = '''int loadBlFiles(void)
{
	struct fileent *e;
	uint32_t i;
	uint32_t r;
'''
    AXES = [
        [('', []), ('pi', [(S, S.replace('uint32_t *pr', 'int *pr')), (LF, LF.replace('uint32_t r;', 'int r;'))])],
        [('', []), ('ii', [(S, S.replace('uint32_t i', 'int i'))])],
        [('', []), ('tu', [('''	int type;

	type = e->type;
	switch (type) {
	case 5: case 7:''', '''	uint32_t type;

	type = e->type;
	switch (type) {
	case 5: case 7:''')])],
    ]
elif w == 'lc':
    REMOVE = ['lab_none', 'exp_t9']
    FOCUS = ['_loadConsoleBlFiles']
    LF = '''int loadConsoleBlFiles(void)
{
	struct fileent *e;
	uint32_t i;
	uint32_t r;
'''
    AXES = [
        [('', []), ('ri', [(LF, LF.replace('uint32_t r;', 'int r;'))])],
        [('', []), ('tu', [('''			int type = e->type;

			switch (type) {
			case 5: case 6:''', '''			uint32_t type = e->type;

			switch (type) {
			case 5: case 6:''')])],
    ]
