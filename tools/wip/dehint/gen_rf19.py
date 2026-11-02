"""`if (ok)` outside `if (psize)`: threading the flag needs no joiner, so size==0 and read-ok share one `if (psize)`;
the free stays on a compound test, so the log path's return PHI keeps buf until dom3."""
import importlib.util, itertools, os


def load(n):
    spec = importlib.util.spec_from_file_location(n, os.path.join(os.path.dirname(__file__), n + '.py'))
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


g = load('gen_rf14')
FREE = {
 'ob': '	if (!ok && buf) {\n		free(buf);\n		buf = NULL;\n	}\n',
 'bo': '	if (buf && !ok) {\n		free(buf);\n		buf = NULL;\n	}\n',
}
PS = {
 'A': '	if (ok) {\n		if (psize)\n			*psize = alloc;\n	} else if (psize)\n		*psize = 0;\n',
 'B': '	if (!ok) {\n		if (psize)\n			*psize = 0;\n	} else if (psize)\n		*psize = alloc;\n',
 'C': '	if (ok) {\n		if (psize)\n			*psize = alloc;\n	} else {\n		if (psize)\n			*psize = 0;\n	}\n',
 'D': '	if (!ok && psize)\n		*psize = 0;\n	if (ok && psize)\n		*psize = alloc;\n',
 'E': '	if (ok && psize)\n		*psize = alloc;\n	if (!ok && psize)\n		*psize = 0;\n',
 'F': '	if (ok && psize)\n		*psize = alloc;\n	else if (psize)\n		*psize = 0;\n',
 'G': '	if (psize && ok)\n		*psize = alloc;\n	else if (psize)\n		*psize = 0;\n',
}


def variants():
    for (en, (eo, ec)), (fn, (init, fl)), (pn, p), (frn, fr), ty in itertools.product(
            g.ENTRY.items(), g.FLAG.items(), PS.items(), FREE.items(), ['int']):
        if fn in ('err', 'errb', 'bn'):
            continue
        decl = '\tvoid *buf = NULL;\n\tsize_t size, alloc;\n\t%s %s;\n\n' % (ty, init)
        s = g.HEAD + decl + eo + g.PREP + fl.replace('LOG', g.LOG).replace('RD', g.RD) + p + fr + ec + '\treturn buf;\n}\n'
        yield '|'.join([en, fn, pn, frn, ty]), s
