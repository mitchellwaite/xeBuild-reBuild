"""Non-empty true arm (`*psize = alloc` there) so size==0 and read-ok meet at the arm in vrp1; the flag is only used by the free."""
import importlib.util, itertools, os


def load(n):
    spec = importlib.util.spec_from_file_location(n, os.path.join(os.path.dirname(__file__), n + '.py'))
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


g = load('gen_rf14')
LOG, RD = g.LOG, g.RD
OK1 = 'ok = 1;\n\t\t\tif (psize)\n\t\t\t\t*psize = alloc;\n'
OK2 = 'if (psize)\n\t\t\t\t*psize = alloc;\n\t\t\tok = 1;\n'
P0 = 'if (psize)\n\t\t\t\t*psize = 0;\n'
BODY = {
 # separate failure writes
 'a': '	if (buf) {\n		if (RD == size) {\n			OK		} else {\n			P0		}\n	} else {\n		LOG\n		P0	}\n',
 'b': '	if (buf == NULL) {\n		LOG\n		P0	} else if (RD == size) {\n			OK	} else {\n			P0	}\n',
 'c': '	if (buf == NULL) {\n		LOG\n		P0	} else if (RD != size) {\n			P0	} else {\n			OK	}\n',
 # shared failure write
 'd': '	if (buf) {\n		if (RD == size) {\n			OK		}\n	} else\n		LOG\n	if (!ok && psize)\n		*psize = 0;\n',
 'e': '	if (buf == NULL)\n		LOG\n	else if (RD == size) {\n			OK	}\n	if (!ok && psize)\n		*psize = 0;\n',
 'f': '	if (buf) {\n		if (RD == size) {\n			OK		}\n	} else\n		LOG\n	if (!ok) {\n		if (psize)\n			*psize = 0;\n	}\n',
 'g': '	if (buf == NULL)\n		LOG\n	else if (RD == size) {\n			OK	}\n	if (!ok) {\n		if (psize)\n			*psize = 0;\n	}\n',
 'h': '	if (buf) {\n		if (RD == size) {\n			OK		}\n	} else\n		LOG\n	if (psize && !ok)\n		*psize = 0;\n',
}
FREE = {
 'ob': '	if (!ok && buf) {\n		free(buf);\n		buf = NULL;\n	}\n',
 'bo': '	if (buf && !ok) {\n		free(buf);\n		buf = NULL;\n	}\n',
 'n': '	if (!ok) {\n		if (buf) {\n			free(buf);\n			buf = NULL;\n		}\n	}\n',
}


def variants():
    for (en, (eo, ec)), (bn, b), (frn, fr), (okn, ok) in itertools.product(g.ENTRY.items(), BODY.items(), FREE.items(), [('1', OK1), ('2', OK2)]):
        decl = '\tvoid *buf = NULL;\n\tsize_t size, alloc;\n\tint ok = 0;\n\n'
        s = g.HEAD + decl + eo + g.PREP + b.replace('LOG', LOG).replace('RD', RD).replace('OK', ok).replace('P0', P0) + fr + ec + '\treturn buf;\n}\n'
        yield '|'.join([en, bn, frn, okn]), s
