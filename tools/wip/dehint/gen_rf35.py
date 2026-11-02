"""Value flag with mask spelling x wider psize forms."""
import importlib.util, itertools, os


def load(n):
    spec = importlib.util.spec_from_file_location(n, os.path.join(os.path.dirname(__file__), n + '.py'))
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


g = load('gen_rf14')
g33 = load('gen_rf33')
g34 = load('gen_rf34')
SIG, R, P0, FRE, SPR = g33.SIG, g33.R, g33.P0, g33.FRE, g33.SPR
PS = dict(g33.PS)
PS.update({
 'x1': '		if (psize && !ok)\n			*psize = 0;\n		else if (psize)\n			*psize = alloc;\n',
 'x2': '		if (!ok && psize)\n			*psize = 0;\n		else if (ok && psize)\n			*psize = alloc;\n',
 'x3': '		if (!ok && psize)\n			*psize = 0;\n		if (psize && ok)\n			*psize = alloc;\n',
 'x4': '		if (psize) {\n			if (ok)\n				*psize = alloc;\n		}\n		if (!ok && psize)\n			*psize = 0;\n',
 'x5': '		if (psize) {\n			if (!ok)\n				*psize = 0;\n		}\n		if (ok && psize)\n			*psize = alloc;\n',
 'x6': '		if (!ok && psize)\n			*psize = 0;\n		if (ok) {\n			if (psize)\n				*psize = alloc;\n		}\n',
 'x7': '		if (ok && psize)\n			*psize = alloc;\n		if (!ok) {\n			if (psize)\n				*psize = 0;\n		}\n',
 'x8': '		if (psize) {\n			if (ok)\n				*psize = alloc;\n			if (!ok)\n				*psize = 0;\n		}\n',
 'x9': '		if (psize) {\n			*psize = alloc;\n			if (!ok)\n				*psize = 0;\n		}\n',
 'x10': '		if (psize) {\n			*psize = 0;\n			if (ok)\n				*psize = alloc;\n		}\n',
})
FR = {
 'if': '		if (!ok) {\nFRE		}\n',
 'el': '		if (ok)\n			return buf;\n		free(buf);\n		buf = NULL;\n',
}
BODY = {
 'val': '	if (buf == NULL) {\n		LOG\nP0	} else {\n		int ok = R CMP size;\nPSFR	}\n',
 'dec': '	if (buf) {\n		int ok = R CMP size;\nPSFR	} else {\n		LOG\nP0	}\n',
}
AL = {'a0': g33.AL['a0'], 'p2': g34.AL['p2'], 'p3': g34.AL['p3']}


def variants():
    for (an, al), (bn, b), (pn, p), c, (fn, fr) in itertools.product(AL.items(), BODY.items(), PS.items(), ['==', '>='], FR.items()):
        if fn == 'el':
            continue
        body = b.replace('LOG', g.LOG).replace('P0', P0).replace('PSFR', p + fr).replace('FRE', FRE).replace('R CMP', R + ' ' + c)
        s = SIG + '\tvoid *buf = NULL;\n\tsize_t size, alloc;\n\n\tif (dir && name) {\n\t\tchar path[1024];\n\n' + SPR + al + '	buf = calloc(alloc, 1);\n' + body + '\t}\n\treturn buf;\n}\n'
        yield '|'.join([an, bn, pn, c]), s
