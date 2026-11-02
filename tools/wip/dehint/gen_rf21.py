"""Failure-write bodies of gen_rf20 x return/free tails.  `buf = NULL` makes the return PHI constant on the free arm at profile_estimate,
so null-return (10%) + call (29%) put free at 4.3% (f=341); the free's epilogue copy needs f>=1000 (>=12.7%).  Tails that avoid the constant arg there."""
import importlib.util, itertools, os


def load(n):
    spec = importlib.util.spec_from_file_location(n, os.path.join(os.path.dirname(__file__), n + '.py'))
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


g = load('gen_rf14')
g20 = load('gen_rf20')
TAIL = {
 't1': '	if (!ok && buf) {\n		free(buf);\n		buf = NULL;\n	}\n	RETbuf;\n',
 't2': '	if (!ok && buf)\n		free(buf);\n	RETok ? buf : NULL;\n',
 't2b': '	if (buf && !ok)\n		free(buf);\n	RETok ? buf : NULL;\n',
 't4': '	if (!ok && buf) {\n		free(buf);\n		RETNULL;\n	}\n	RETbuf;\n',
 't6': '	if (ok)\n		ret = buf;\n	else if (buf)\n		free(buf);\n	RETret;\n',
 't6b': '	if (!ok && buf)\n		free(buf);\n	else\n		ret = buf;\n	RETret;\n',
 't6c': '	if (buf && !ok)\n		free(buf);\n	else\n		ret = buf;\n	RETret;\n',
 't6d': '	if (!ok && buf)\n		free(buf);\n	if (ok)\n		ret = buf;\n	RETret;\n',
 't7': '	if (ok)\n		RETbuf;\n	if (buf)\n		free(buf);\n	RETNULL;\n',
 't9': '	if (!ok) {\n		if (buf)\n			free(buf);\n		buf = NULL;\n	}\n	RETbuf;\n',
 't10': '	if (!ok) {\n		if (buf)\n			free(buf);\n		RETNULL;\n	}\n	RETbuf;\n',
 't11': '	if (!ok && buf)\n		free(buf);\n	if (!ok)\n		buf = NULL;\n	RETbuf;\n',
}
B = {k: v for k, v in g20.BODY.items()}
B['A'] = '	if (buf) {\n		if (RD == size)\n			ok = 1;\n	} else\n		LOG\n	if (ok) {\n		if (psize)\n			*psize = alloc;\n	} else if (psize)\n		*psize = 0;\n'
B['A2'] = '	if (buf == NULL)\n		LOG\n	else if (RD == size)\n		ok = 1;\n	if (ok) {\n		if (psize)\n			*psize = alloc;\n	} else if (psize)\n		*psize = 0;\n'
B['S'] = '	if (buf) {\n		if (RD == size)\n			ok = 1;\n	} else\n		LOG\n	if (psize) {\n		if (ok)\n			*psize = alloc;\n		else\n			*psize = 0;\n	}\n'
B['D'] = '	if (buf) {\n		if (RD == size)\n			ok = 1;\n	} else\n		LOG\n	if (!ok && psize)\n		*psize = 0;\n	if (ok && psize)\n		*psize = alloc;\n'


def variants():
    for (bn, b), (tn, t), rt in itertools.product(B.items(), TAIL.items(), ['in', 'out']):
        decl = '\tvoid *buf = NULL;\n\tsize_t size, alloc;\n\tint ok = 0;\n'
        if 'ret' in t:
            decl = '\tvoid *buf = NULL, *ret = NULL;\n\tsize_t size, alloc;\n\tint ok = 0;\n'
        body = b.replace('LOG', g.LOG).replace('RD', g.RD).replace('OK', g20.OK1).replace('P0', g20.P0)
        if rt == 'in':
            # single-exit: nest the body, the value falls out after the if
            eo, ec = g.ENTRY['nest']
            tail = t.replace('RET', 'return ')
            s = g.HEAD + decl + '\n' + eo + g.PREP + body + tail + ec + '\treturn NULL;\n}\n'
        else:
            eo, ec = g.ENTRY['or']
            tail = t.replace('RET', 'return ')
            s = g.HEAD + decl + '\n' + eo + g.PREP + body + tail + '}\n'
        yield '|'.join([bn, tn, rt]), s
