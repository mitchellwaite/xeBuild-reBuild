# loadConsoleBlFiles' case 24 through defaultBl60 as well.  Base: gen_bd25's e+oz.
BASE = 'build/bd/gen_bd25_best.c'
CC = '''e->data = malloc(0x60);
if (!e->data) {
	r = 1;
	break;
}
e->size = 0x60;
memcpy(e->data, defBl60, 0x60);
'''


def ind(s, n):
    return ''.join('\t' * n + l + '\n' for l in s.splitlines())


OLD = '''				if (!xb.glitch2mfg)
					break;
				if (loadBaseFile(e->name, e)) {
''' + ind(CC, 5) + '''				} else if (e->size != 0x60) {
''' + ind(CC, 5) + '''				}
				break;
'''
AXES = [[
    ('keep', []),
    ('h', [(OLD, '''				if (!xb.glitch2mfg)
					break;
				if (loadBaseFile(e->name, e))
					r = defaultBl60(e);
				else if (e->size != 0x60)
					r = defaultBl60(e);
				break;
''')]),
    ('hn', [(OLD, '''				if (xb.glitch2mfg) {
					if (loadBaseFile(e->name, e))
						r = defaultBl60(e);
					else if (e->size != 0x60)
						r = defaultBl60(e);
				}
				break;
''')]),
]]
