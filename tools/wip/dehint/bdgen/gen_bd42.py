# Declaration types, after extractSmcConfig's int size: checkBl's and isUpdateBl's params against their hints.
# BDW picks the group.
import os
w = os.environ.get('BDW', 'chk')
if w == 'chk':
    REMOVE = ['pin_type']
    FOCUS = ['_checkBl', '_loadBlFiles', '_loadConsoleBlFiles']
    S = 'int checkBl(uint8_t *bl, uint32_t size, int type, uint32_t crc)'
    AXES = [
        [('', []), ('si', [(S, S.replace('uint32_t size', 'int size'))])],
        [('', []), ('tu', [(S, S.replace('int type', 'uint32_t type'))])],
        [('', []), ('ci', [(S, S.replace('uint32_t crc', 'int crc'))])],
        [('', []), ('bc', [(S, S.replace('uint8_t *bl', 'void *bl'))])],
    ]
elif w == 'upd':
    REMOVE = ['exp_upd']
    FOCUS = ['_addUpdateBls', '_isUpdateBl']
    O = 'return type == 23 || type == 15 || type == 16 || type == 9 || type == 10 || type == 24 || type == 25;'
    S = 'int isUpdateBl(int type)'
    F = {
        'sw': '''switch (type) {
	case 9: case 10: case 15: case 16: case 23: case 24: case 25:
		return 1;
	}
	return 0;''',
        'ifs': '''if (type == 23 || type == 15)
		return 1;
	return type == 16 || type == 9 || type == 10 || type == 24 || type == 25;''',
        'fl': '''int r = 0;

	if (type == 23 || type == 15 || type == 16 || type == 9 || type == 10 || type == 24 || type == 25)
		r = 1;
	return r;''',
        'q': 'return (type == 23 || type == 15 || type == 16 || type == 9 || type == 10 || type == 24 || type == 25) ? 1 : 0;',
    }
    AXES = [[('', [])] + [(k, [(O, v)]) for k, v in F.items()],
            [('', []), ('tu', [(S, 'int isUpdateBl(uint32_t type)')])]]
else:
    REMOVE = ['noclone']
    S = '''int loadInputFile(const char *name, struct fileent *e, int pad, uint32_t crc, uint8_t *meta,
		  int su, int fs, int common)'''
    AXES = [
        [('', []), ('ci', [(S, S.replace('uint32_t crc', 'int crc'))])],
        [('', []), ('mv', [(S, S.replace('uint8_t *meta', 'void *meta'))])],
    ]
