"""Two separate dir/name tests: each is predicted on its own at profile_estimate, which lowers
the frequency of everything after them relative to the entry block (`dir && name` folds to one
test at .786).  size's thread scales with that, align's and the return value's keep the entry refs."""
import importlib.util, os, itertools


def load(n):
    spec = importlib.util.spec_from_file_location(n, os.path.join(os.path.dirname(__file__), n + '.py'))
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


G4 = load('gen_rf4')
G5 = load('gen_rf5')

ENTRY = {
 'two': ('	if (dir == NULL)\n		return NULL;\n	if (name == NULL)\n		return NULL;\n', ''),
 'twobuf': ('	if (dir == NULL)\n		return buf;\n	if (name == NULL)\n		return buf;\n', ''),
 'nest2': ('	if (dir) {\n	if (name) {\n', '	}\n	}\n'),
 'nest2n': ('	if (dir != NULL) {\n	if (name == NULL)\n		return NULL;\n', '	}\n'),
 'gotoout': ('	if (dir == NULL)\n		goto out;\n	if (name == NULL)\n		goto out;\n', 'out:\n'),
 'swap': ('	if (name == NULL)\n		return NULL;\n	if (dir == NULL)\n		return NULL;\n', ''),
}


def tails():
    for tn, t in G4.TAIL.items():
        yield tn, '', t.replace('LOG', G4.LOG)
    for (rn, (init, r)), (pn, p), (fn, f) in itertools.product(G5.READ.items(), G5.PSIZE.items(), G5.FREE.items()):
        d = '\tint ok = %d;\n' % init if init != 2 else '\tint ok;\n'
        yield '%s|%s|%s' % (rn, pn, fn), d, r.replace('LOG', G4.LOG) + p + f


def variants():
    for (en, (eo, ec)), (tn, d, t), bt in itertools.product(ENTRY.items(), list(tails()), ['void', 'unsigned char']):
        s = G4.HEAD + '\t%s *buf = NULL;\n\tsize_t size, alloc;\n%s\n' % (bt, d) + eo + G4.PREP + t + ec + '\treturn buf;\n}\n'
        yield '%s|%s|%s' % (bt, en, tn), s
