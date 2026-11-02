"""Scoped path, `if (psize == NULL)`-style tests, so the psize==NULL edge is the block's first successor: dom2's first thread for read-fail is the free path."""
import importlib.util, itertools, os


def load(n):
    spec = importlib.util.spec_from_file_location(n, os.path.join(os.path.dirname(__file__), n + '.py'))
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


g = load('gen_rf14')
SIG = 'void *readFileIn(const char *dir, const char *name, size_t *psize, size_t align)\n{\n'
OKSET = {
 'ok': ('ok', '!ok', 'ok = 0'),
 'err': ('!err', 'err', 'err = 0'),
}
PS = {
 'g1': '	if (psize == NULL)\n		goto done;\n	if (OK)\n		*psize = alloc;\n	else\n		*psize = 0;\ndone:\n',
 'g2': '	if (!psize)\n		goto done;\n	if (NOK)\n		*psize = 0;\n	else\n		*psize = alloc;\ndone:\n',
 'e1': '	if (psize == NULL)\n		;\n	else if (OK)\n		*psize = alloc;\n	else\n		*psize = 0;\n',
 'e2': '	if (psize == NULL)\n		;\n	else if (NOK)\n		*psize = 0;\n	else\n		*psize = alloc;\n',
 'c1': '	if (psize != NULL) {\n		if (OK)\n			*psize = alloc;\n		else\n			*psize = 0;\n	}\n',
}
FREE = {
 'ob': '	if (NOK && buf) {\n		free(buf);\n		buf = NULL;\n	}\n',
 'bo': '	if (buf && NOK) {\n		free(buf);\n		buf = NULL;\n	}\n',
}
FLAG = {
 'ok': {k: v for k, v in g.FLAG.items() if k in ('nf', 'bf', 'i1', 'i1b', 'o1', 'o2')},
 'err': {'err': g.FLAG['err'], 'errb': g.FLAG['errb']},
}


def variants():
    for fam in ('ok', 'err'):
        O, N, _ = OKSET[fam]
        for (fn, (init, fl)), (pn, p), (frn, fr) in itertools.product(FLAG[fam].items(), PS.items(), FREE.items()):
            s = SIG + '\tvoid *buf = NULL;\n\tsize_t size, alloc;\n\tint %s;\n\n' % init + '\tif (dir && name) {\n\t\tchar path[1024];\n\n' + g.PREP + fl.replace('LOG', g.LOG).replace('RD', g.RD) + p.replace('NOK', N).replace('OK', O) + fr.replace('NOK', N) + '\t}\n\treturn buf;\n}\n'
            yield '|'.join([fn, pn, frn]), s
