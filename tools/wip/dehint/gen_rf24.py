"""No flag, scoped path: the inner PHI (clobber before the outer join) keeps log's constant NULL away from dir-null's, so tail-merge can't merge their forwarders,
and read-fail's free stays where the source puts it, before the join."""
import importlib.util, itertools, os


def load(n):
    spec = importlib.util.spec_from_file_location(n, os.path.join(os.path.dirname(__file__), n + '.py'))
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


g = load('gen_rf13')
SIG = 'void *readFileIn(const char *dir, const char *name, size_t *psize, size_t align)\n{\n'
DECLS = {
 'mid': ('\tvoid *buf = NULL;\n\tsize_t size, alloc;\n\n', '\tif (dir && name) {\n\t\tchar path[1024];\n\n'),
 'in': ('\tvoid *buf = NULL;\n\n', '\tif (dir && name) {\n\t\tchar path[1024];\n\t\tsize_t size, alloc;\n\n'),
}
EXTRA = {
 'm': '	if (buf == NULL) {\n		LOG\n' + g.P0 + '	} else if (readFileTo(path, buf, size) == size) {\n		' + g.OKP + '	} else {\n' + g.P0 + '		free(buf);\n		buf = NULL;\n	}\n',
 'n': '	if (buf) {\n		if (readFileTo(path, buf, size) == size) {\n		' + g.OKP + '		} else {\n' + g.P0 + '			free(buf);\n			buf = NULL;\n		}\n	} else {\n		LOG\n' + g.P0 + '	}\n',
}


def variants():
    tails = dict(g.TAIL)
    tails.update(EXTRA)
    for (tn, t), (dn, (d1, d2)), bt in itertools.product(tails.items(), DECLS.items(), ['void']):
        s = SIG + d1.replace('void', bt, 1) + d2 + g.PREP + t.replace('LOG', g.LOG) + '\t}\n\treturn buf;\n}\n'
        yield '|'.join([tn, dn, bt]), s
