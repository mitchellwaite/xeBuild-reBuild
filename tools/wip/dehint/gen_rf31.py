"""s12 family (`int ok = read == size` local to the read arm, s=0): psize write forms and flag forms, looking for psize refs high enough to pop before path."""
import importlib.util, itertools, os


def load(n):
    spec = importlib.util.spec_from_file_location(n, os.path.join(os.path.dirname(__file__), n + '.py'))
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


g = load('gen_rf14')
SIG = 'void *readFileIn(const char *dir, const char *name, size_t *psize, size_t align)\n{\n'
R = 'readFileTo(path, buf, size)'
P0 = '		if (psize)\n			*psize = 0;\n'
FRE = '			free(buf);\n			buf = NULL;\n'
PS = {
 'nest': '		if (psize) {\n			if (ok)\n				*psize = alloc;\n			else\n				*psize = 0;\n		}\n',
 'nestn': '		if (psize) {\n			if (!ok)\n				*psize = 0;\n			else\n				*psize = alloc;\n		}\n',
 'tern': '		if (psize)\n			*psize = ok ? alloc : 0;\n',
 'ternn': '		if (psize)\n			*psize = !ok ? 0 : alloc;\n',
 'mul': '		if (psize)\n			*psize = ok * alloc;\n',
 'cc': '		if (ok && psize)\n			*psize = alloc;\n		if (!ok && psize)\n			*psize = 0;\n',
 'ccn': '		if (!ok && psize)\n			*psize = 0;\n		if (ok && psize)\n			*psize = alloc;\n',
 'cce': '		if (ok && psize)\n			*psize = alloc;\n		else if (psize)\n			*psize = 0;\n',
 'cce2': '		if (psize && ok)\n			*psize = alloc;\n		else if (psize)\n			*psize = 0;\n',
 'cce3': '		if (!ok && psize)\n			*psize = 0;\n		else if (psize)\n			*psize = alloc;\n',
 'okif': '		if (ok) {\n			if (psize)\n				*psize = alloc;\n		} else if (psize)\n			*psize = 0;\n',
 'okif2': '		if (!ok) {\n			if (psize)\n				*psize = 0;\n		} else if (psize)\n			*psize = alloc;\n',
}
FLAG = {
 'val': 'int ok = RCMP;\n',
 'set': 'int ok = 0;\n		if (RCMP)\n			ok = 1;\n',
 'seti': 'int ok = 1;\n		if (RNCMP)\n			ok = 0;\n',
 'dec': 'int ok;\n		ok = RCMP;\n',
 'chr': 'char ok = RCMP;\n',
 'szt': 'size_t ok = RCMP;\n',
}
SH = {
 'nf': '	if (buf == NULL) {\n		LOG\nP0	} else {\n		BODY	}\n',
 'bf': '	if (buf) {\n		BODY	} else {\n		LOG\nP0	}\n',
}
FR = {
 'if': '		if (!ok) {\nFRE		}\n',
 'ifb': '		if (ok == 0) {\nFRE		}\n',
}
CMPS = {'eq': ('==', '!='), 'ge': ('>=', '<')}


def variants():
    for (sn, sh), (fn, fl), (pn, p), (cn, (c, nc)) in itertools.product(SH.items(), FLAG.items(), PS.items(), CMPS.items()):
        fr = FR['if']
        body = fl.replace('RNCMP', R + ' ' + nc + ' size').replace('RCMP', R + ' ' + c + ' size') + p + fr.replace('FRE', FRE)
        b = sh.replace('LOG', g.LOG).replace('P0', P0).replace('BODY', body)
        s = SIG + '\tvoid *buf = NULL;\n\tsize_t size, alloc;\n\n\tif (dir && name) {\n\t\tchar path[1024];\n\n' + g.PREP + b + '\t}\n\treturn buf;\n}\n'
        yield '|'.join([sn, fn, pn, cn]), s
