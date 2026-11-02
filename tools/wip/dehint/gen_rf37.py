"""Attempt 3: static read helper without name/buf tests: a call at profile_estimate in the buf arm, no ghost once inlined."""
import importlib.util, itertools, os


def load(n):
    spec = importlib.util.spec_from_file_location(n, os.path.join(os.path.dirname(__file__), n + '.py'))
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


g = load('gen_rf14')
g31 = load('gen_rf31')
g35 = load('gen_rf35')
SIG, P0, FRE = g31.SIG, g31.P0, g31.FRE
PS = dict(g35.PS)
HEAD = 'static RT readData(const char *name, void *buf, size_t size)\n{\n'
H = {
 'int': (HEAD.replace('RT', 'int') + '	FILE *f;\n	int ret = 0;\n\n	if (size) {\n		f = fopen(name, "rb");\n		if (f) {\n			if (size <= (size_t)getFileSize(f)) {\n				fread(buf, size, 1, f);\n				fclose(f);\n				ret = size;\n			}\n		}\n	}\n	return ret;\n}\n\n', 'readData(path, buf, size) == size'),
 'szt': (HEAD.replace('RT', 'size_t') + '	FILE *f;\n	size_t ret = 0;\n\n	if (size) {\n		f = fopen(name, "rb");\n		if (f) {\n			if (size <= (size_t)getFileSize(f)) {\n				fread(buf, size, 1, f);\n				fclose(f);\n				ret = size;\n			}\n		}\n	}\n	return ret;\n}\n\n', 'readData(path, buf, size) == size'),
 'ok1': (HEAD.replace('RT', 'int') + '	FILE *f;\n	int ok = 1;\n\n	if (size) {\n		ok = 0;\n		f = fopen(name, "rb");\n		if (f) {\n			if (size <= (size_t)getFileSize(f)) {\n				fread(buf, size, 1, f);\n				fclose(f);\n				ok = 1;\n			}\n		}\n	}\n	return ok;\n}\n\n', 'readData(path, buf, size)'),
 'ok0': (HEAD.replace('RT', 'int') + '	FILE *f;\n	int ok = 0;\n\n	if (size == 0)\n		return 1;\n	f = fopen(name, "rb");\n	if (f) {\n		if (size <= (size_t)getFileSize(f)) {\n			fread(buf, size, 1, f);\n			fclose(f);\n			ok = 1;\n		}\n	}\n	return ok;\n}\n\n', 'readData(path, buf, size)'),
 'ret': (HEAD.replace('RT', 'int') + '	FILE *f;\n\n	if (size == 0)\n		return 1;\n	f = fopen(name, "rb");\n	if (f == NULL)\n		return 0;\n	if (size > (size_t)getFileSize(f))\n		return 0;\n	fread(buf, size, 1, f);\n	fclose(f);\n	return 1;\n}\n\n', 'readData(path, buf, size)'),
}
FR = '		if (!ok) {\n' + FRE + '		}\n'
SH = {
 'nf': '	if (buf == NULL) {\n		LOG\nP0	} else {\n		BODY	}\n',
 'bf': '	if (buf) {\n		BODY	} else {\n		LOG\nP0	}\n',
}
FL = {'val': 'int ok = RD;\n', 'set': 'int ok = 0;\nif (RD)\n ok = 1;\n'}
DIR = {
 'd1': 'if (RD) {\n if (psize)\n *psize = alloc;\n} else {\n if (psize)\n *psize = 0;\n free(buf);\n buf = NULL;\n}\n',
 'd2': 'if (!(RD)) {\n if (psize)\n *psize = 0;\n free(buf);\n buf = NULL;\n} else if (psize)\n *psize = alloc;\n',
 'd3': 'if (RD) {\n if (psize)\n *psize = alloc;\n return buf;\n}\nif (psize)\n *psize = 0;\nfree(buf);\nbuf = NULL;\n',
 'd4': 'if (!(RD)) {\n if (psize)\n *psize = 0;\n free(buf);\n return NULL;\n}\nif (psize)\n *psize = alloc;\n',
}


def wrap(h, sh, body):
    b = sh.replace('LOG', g.LOG).replace('P0', P0).replace('BODY', body)
    return h + SIG + '\tvoid *buf = NULL;\n\tsize_t size, alloc;\n\n\tif (dir && name) {\n\t\tchar path[1024];\n\n' + g.PREP + b + '\t}\n\treturn buf;\n}\n'


def variants():
    for (hn, (h, rd)), (sn, sh) in itertools.product(H.items(), SH.items()):
        for (fn, fl), (pn, p) in itertools.product(FL.items(), PS.items()):
            yield '|'.join([hn, sn, fn, pn]), wrap(h, sh, fl.replace('RD', rd) + p + FR)
        for dn, d in DIR.items():
            yield '|'.join([hn, sn, dn]), wrap(h, sh, d.replace('RD', rd))
