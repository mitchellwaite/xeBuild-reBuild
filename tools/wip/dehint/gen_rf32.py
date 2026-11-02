"""Value flag (fread stays f=485) x psize forms x where the writes sit x free forms, looking for buf mem>=13680 and psize mem>=~2280."""
import importlib.util, itertools, os


def load(n):
    spec = importlib.util.spec_from_file_location(n, os.path.join(os.path.dirname(__file__), n + '.py'))
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


g = load('gen_rf14')
g31 = load('gen_rf31')
SIG = g31.SIG
R = g31.R
P0 = g31.P0
PS = g31.PS
FREE = {
 'ob': '	if (!ok && buf) {\n		free(buf);\n		buf = NULL;\n	}\n',
 'bo': '	if (buf && !ok) {\n		free(buf);\n		buf = NULL;\n	}\n',
 'n': '	if (!ok) {\n		if (buf) {\n			free(buf);\n			buf = NULL;\n		}\n	}\n',
 'b': '	if (buf) {\n		if (!ok) {\n			free(buf);\n			buf = NULL;\n		}\n	}\n',
}
FLAG = {
 'nf': '	if (buf == NULL) {\n		LOG\nLW	} else {\n		ok = RCMP;\nRW	}\n',
 'bf': '	if (buf) {\n		ok = RCMP;\nRW	} else {\n		LOG\nLW	}\n',
 'nf0': '	if (buf == NULL) {\n		LOG\nLW		ok = 0;\n	} else {\n		ok = RCMP;\nRW	}\n',
 'pre': '	ok = buf != NULL && RCMP;\n	if (buf == NULL)\n		LOG\nTW',
 'pre2': '	if (buf == NULL)\n		LOG\n	ok = buf != NULL && RCMP;\nTW',
 'pre3': '	if (buf == NULL)\n		LOG\n	ok = buf && RCMP;\nTW',
 'pre4': '	if (buf && RCMP)\n		ok = 1;\n	else if (buf == NULL)\n		LOG\nTW',
 'pre5': '	if (buf != NULL && RCMP)\n		ok = 1;\n	if (buf == NULL)\n		LOG\nTW',
}
CMPS = {'eq': '==', 'ge': '>='}


def variants():
    for (fn, fl), (pn, p), (frn, fr), (cn, c), ins in itertools.product(FLAG.items(), PS.items(), FREE.items(), CMPS.items(), ['init', 'noinit']):
        if ins == 'noinit' and fn not in ('nf0', 'pre', 'pre2', 'pre3'):
            continue
        if ins == 'init' and fn in ('nf0',):
            continue
        decl = '\tvoid *buf = NULL;\n\tsize_t size, alloc;\n\tint ok%s;\n\n' % (' = 0' if ins == 'init' else '')
        body = fl.replace('LOG', g.LOG).replace('RCMP', R + ' ' + c + ' size').replace('LW', P0).replace('RW', p).replace('TW', p.replace('\t\t', '\t', 1))
        s = SIG + decl + '\tif (dir && name) {\n\t\tchar path[1024];\n\n' + g.PREP + body + fr + '\t}\n\treturn buf;\n}\n'
        yield '|'.join([fn, pn, frn, cn, ins]), s
