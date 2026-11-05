# lab_none: r = 1's block has to outrank the shrink-wrapped return in bb-reorder's last round
# (14 and 20 with the plain for and the helper).  Forms of case 24's failure and of the loop head.
BASE = 'build/bd/none.c'
FOCUS = ['_loadConsoleBlFiles']
OLD = '''				if (!xb.glitch2mfg)
					break;
				if (loadBaseFile(e->name, e))
					r = defaultBl60(e);
				else if (e->size != 0x60)
					r = defaultBl60(e);
				break;
'''
CC = '''e->data = malloc(0x60);
if (!e->data) {
	r = 1;
	break;
}
e->size = 0x60;
memcpy(e->data, defBl60, 0x60);
'''
CD = '''e->data = malloc(0x60);
if (e->data) {
	e->size = 0x60;
	memcpy(e->data, defBl60, 0x60);
} else
	r = 1;
'''
CE = '''e->data = malloc(0x60);
if (!e->data)
	r = 1;
else {
	e->size = 0x60;
	memcpy(e->data, defBl60, 0x60);
}
'''


def ind(s, n):
    return ''.join('\t' * n + l + '\n' for l in s.splitlines())


def dup(c):
    return '''				if (!xb.glitch2mfg)
					break;
				if (loadBaseFile(e->name, e)) {
''' + ind(c, 5) + '''				} else if (e->size != 0x60) {
''' + ind(c, 5) + '''				}
				break;
'''


def nest(c):
    return '''				if (xb.glitch2mfg) {
					if (!loadBaseFile(e->name, e)) {
						if (e->size != 0x60) {
''' + ind(c, 7) + '''						}
					} else {
''' + ind(c, 6) + '''					}
				}
				break;
'''


A = [('h', []), ('dC', [(OLD, dup(CC))]), ('dD', [(OLD, dup(CD))]), ('dE', [(OLD, dup(CE))]),
     ('nC', [(OLD, nest(CC))]), ('nD', [(OLD, nest(CD))])]
LO = '''	for (i = 1; i < (uint32_t)xb.nFiles; i++) {
		e = &xb.files[i];
		r = 0;
		if (strnicmp(e->name, "none", 4) || e->crc) {
			int type = e->type;

			switch (type) {
			case 5: case 6: case 7: case 8: case 11: case 12: case 13: case 14:
			case 17: case 18: case 19:
				log_printf(1, "skipping'''
LN = LO.replace('for (i = 1; i < (uint32_t)xb.nFiles; i++) {', 'for (i = 1; (int)i < xb.nFiles; i++) {')
B = [('for', []), ('sint', [(LO, LN)])]
AXES = [A, B]
