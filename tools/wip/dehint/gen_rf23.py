"""Scoped path.  Failures reach `if (psize) *psize = 0` with no flag test on the way (goto or else), and read-ok skips it, so dom2 can thread read-fail's psize==NULL edge
past `if (!ok && buf)`, leaving `*psize = 0; if (buf)` one block for dom3 to thread log through."""
import importlib.util, itertools, os


def load(n):
    spec = importlib.util.spec_from_file_location(n, os.path.join(os.path.dirname(__file__), n + '.py'))
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


g = load('gen_rf14')
SIG = 'void *readFileIn(const char *dir, const char *name, size_t *psize, size_t align)\n{\n'
OKS = {
 '1': 'ok = 1;\n\t\tif (psize)\n\t\t\t*psize = alloc;\n',
 '2': 'if (psize)\n\t\t\t*psize = alloc;\n\t\tok = 1;\n',
}
P0 = '	if (psize)\n		*psize = 0;\n'
BODY = {
 'h1': '	if (buf && RD == size) {\n		OK	} else {\n		if (buf == NULL)\n			LOG\nP0	}\n',
 'h1n': '	if (buf == NULL || RD != size) {\n		if (buf == NULL)\n			LOG\nP0	} else {\n		OK	}\n',
 'h2': '	if (buf == NULL) {\n		LOG\n		goto fail;\n	}\n	if (RD == size) {\n		OK		goto out;\n	}\nfail:\nP0out:\n',
 'h3': '	if (buf) {\n		if (RD == size) {\n		OK		goto out;\n		}\n	} else\n		LOG\nP0out:\n',
 'h4': '	if (buf == NULL)\n		LOG\n	else if (RD == size) {\n		OK		goto out;\n	}\nP0out:\n',
 'h5': '	if (buf == NULL) {\n		LOG\n		goto fail;\n	}\n	if (RD != size)\n		goto fail;\n	OK	goto out;\nfail:\nP0out:\n',
 'h6': '	if (buf) {\n		if (RD != size)\n			goto fail;\n		OK		goto out;\n	}\n	LOG\nfail:\nP0out:\n',
}
FREE = {
 'ob': '	if (!ok && buf) {\n		free(buf);\n		buf = NULL;\n	}\n',
 'bo': '	if (buf && !ok) {\n		free(buf);\n		buf = NULL;\n	}\n',
}
DECLS = {
 'mid': ('\tvoid *buf = NULL;\n\tsize_t size, alloc;\n\tint ok = 0;\n\n', '\tif (dir && name) {\n\t\tchar path[1024];\n\n', '\t}\n\treturn buf;\n}\n'),
 'fn': ('\tchar path[1024];\n\tvoid *buf = NULL;\n\tsize_t size, alloc;\n\tint ok = 0;\n\n', '\tif (dir && name) {\n', '\t}\n\treturn buf;\n}\n'),
}


def variants():
    for (bn, b), (on, ok), (fn, f), (dn, (d1, d2, d3)) in itertools.product(BODY.items(), OKS.items(), FREE.items(), DECLS.items()):
        body = b.replace('LOG', g.LOG).replace('RD', g.RD).replace('OK', ok).replace('P0', P0)
        yield '|'.join([bn, on, fn, dn]), SIG + d1 + d2 + g.PREP + body + f + d3
