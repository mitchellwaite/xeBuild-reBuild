"""Scoped path.  Failures write *psize = 0 in their arms, the ok write is compound (f=3930 at estimate) in the tail or the arm's test, for the psize refs IRA wants."""
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
P0C = '		if (!ok && psize)\n			*psize = 0;\n'
FRE = '		free(buf);\n		buf = NULL;\n'
SHAPES = {
 # ok flag only for the tail write
 's1': ('ok = 0', '	if (buf == NULL) {\n		LOG\nP0	} else if (R CMP size)\n		ok = 1;\n	else {\nP0	}\n	if (ok && psize)\n		*psize = alloc;\n', True),
 's2': ('ok = 0', '	if (buf == NULL) {\n		LOG\nP0	} else if (R NCMP size) {\nP0	} else\n		ok = 1;\n	if (ok && psize)\n		*psize = alloc;\n', True),
 's3': ('ok = 0', '	if (buf) {\n		if (R CMP size)\n			ok = 1;\n		else {\nP0		}\n	} else {\n		LOG\nP0	}\n	if (ok && psize)\n		*psize = alloc;\n', True),
 's4': ('ok = 0', '	if (buf) {\n		if (R NCMP size) {\nP0		} else\n			ok = 1;\n	} else {\n		LOG\nP0	}\n	if (psize && ok)\n		*psize = alloc;\n', True),
 # log writes in its arm, read path decides with the flag
 's5': ('ok = 0', '	if (buf == NULL) {\n		LOG\nP0	} else {\n		if (R CMP size)\n			ok = 1;\n		if (!ok && psize)\n			*psize = 0;\n		if (ok && psize)\n			*psize = alloc;\n	}\n', True),
 's6': ('ok = 0', '	if (buf == NULL) {\n		LOG\nP0	} else {\n		if (R CMP size)\n			ok = 1;\n		if (psize) {\n			if (ok)\n				*psize = alloc;\n			else\n				*psize = 0;\n		}\n	}\n', True),
 's7': ('ok = 0', '	if (buf == NULL) {\n		LOG\nP0	} else {\n		ok = R CMP size;\n		if (psize) {\n			if (ok)\n				*psize = alloc;\n			else\n				*psize = 0;\n		}\n	}\n', True),
 's8': ('ok', '	if (buf == NULL) {\n		LOG\nP0		ok = 0;\n	} else {\n		ok = R CMP size;\n		if (psize) {\n			if (ok)\n				*psize = alloc;\n			else\n				*psize = 0;\n		}\n	}\n', True),
 's9': ('ok = 0', '	if (buf) {\n		if (R CMP size)\n			ok = 1;\n		if (psize) {\n			if (ok)\n				*psize = alloc;\n			else\n				*psize = 0;\n		}\n	} else {\n		LOG\nP0	}\n', True),
 's10': ('ok = 0', '	if (buf) {\n		if (R CMP size)\n			ok = 1;\n		if (!ok && psize)\n			*psize = 0;\n		if (ok && psize)\n			*psize = alloc;\n	} else {\n		LOG\nP0	}\n', True),
 's11': ('ok = 0', '	if (buf) {\n		if (R CMP size)\n			ok = 1;\n		if (psize)\n			*psize = ok ? alloc : 0;\n	} else {\n		LOG\nP0	}\n', True),
 # free inside the read arm, flag gone
 's12': (None, '	if (buf == NULL) {\n		LOG\nP0	} else {\n		int ok = R CMP size;\n		if (psize) {\n			if (ok)\n				*psize = alloc;\n			else\n				*psize = 0;\n		}\n		if (!ok) {\nFRE		}\n	}\n', False),
 's13': (None, '	if (buf) {\n		int ok = R CMP size;\n		if (psize) {\n			if (ok)\n				*psize = alloc;\n			else\n				*psize = 0;\n		}\n		if (!ok) {\nFRE		}\n	} else {\n		LOG\nP0	}\n', False),
 's14': (None, '	if (buf) {\n		int ok = 0;\n		if (R CMP size)\n			ok = 1;\n		if (psize) {\n			if (ok)\n				*psize = alloc;\n			else\n				*psize = 0;\n		}\n		if (!ok) {\nFRE		}\n	} else {\n		LOG\nP0	}\n', False),
 's15': (None, '	if (buf == NULL) {\n		LOG\nP0	} else {\n		int ok = 0;\n		if (R CMP size)\n			ok = 1;\n		if (psize) {\n			if (ok)\n				*psize = alloc;\n			else\n				*psize = 0;\n		}\n		if (!ok) {\nFRE		}\n	}\n', False),
 's16': (None, '	if (buf) {\n		size_t got = R;\n		if (psize)\n			*psize = got CMP size ? alloc : 0;\n		if (got NCMP size) {\nFRE		}\n	} else {\n		LOG\nP0	}\n', False),
 's17': (None, '	if (buf) {\n		if (R CMP size) {\n			if (psize)\n				*psize = alloc;\n		} else {\n			if (psize)\n				*psize = 0;\n			free(buf);\n			buf = NULL;\n		}\n	} else {\n		LOG\nP0	}\n', False),
}
FREE = {
 'ob': '	if (!ok && buf) {\n		free(buf);\n		buf = NULL;\n	}\n',
 'bo': '	if (buf && !ok) {\n		free(buf);\n		buf = NULL;\n	}\n',
 'n': '	if (!ok) {\n		if (buf) {\n			free(buf);\n			buf = NULL;\n		}\n	}\n',
 'b': '	if (buf) {\n		if (!ok) {\n			free(buf);\n			buf = NULL;\n		}\n	}\n',
}
CMPS = {'eq': ('==', '!='), 'ge': ('>=', '<')}


def variants():
    for (sn, (init, b, wantfree)), (fn, f), (cn, (c, nc)) in itertools.product(SHAPES.items(), FREE.items(), CMPS.items()):
        if not wantfree and fn != 'ob':
            continue
        decl = '\tvoid *buf = NULL;\n\tsize_t size, alloc;\n' + ('\tint %s;\n' % init if init else '') + '\n'
        body = b.replace('LOG', g.LOG).replace('R NCMP', R + ' ' + nc).replace('R CMP', R + ' ' + c).replace('= R;', '= ' + R + ';').replace('CMP', c).replace('NCMP', nc).replace('P0', P0).replace('FRE', FRE)
        body = body.replace('got N' + c, 'got ' + nc)
        s = SIG + decl + '\tif (dir && name) {\n\t\tchar path[1024];\n\n' + g.PREP + body + (f if wantfree else '') + '\t}\n\treturn buf;\n}\n'
        yield '|'.join([sn, fn if wantfree else '-', cn]), s
