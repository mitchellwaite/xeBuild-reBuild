"""`char path[1024]` scoped inside `if (dir && name)`: its clobber sits between the inner join and the return, so the free arm's NULL is an arg of an inner PHI.
apply_return_prediction only looks at the return PHI's own args, so null-return stops applying to the free test (call alone, 29%, f>=1000)."""
import importlib.util, itertools, os


def load(n):
    spec = importlib.util.spec_from_file_location(n, os.path.join(os.path.dirname(__file__), n + '.py'))
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


g = load('gen_rf14')
g20 = load('gen_rf20')
g21 = load('gen_rf21')
SIG = 'void *readFileIn(const char *dir, const char *name, size_t *psize, size_t align)\n{\n'
FREE = {
 'ob': '		if (!ok && buf) {\n			free(buf);\n			buf = NULL;\n		}\n',
 'bo': '		if (buf && !ok) {\n			free(buf);\n			buf = NULL;\n		}\n',
}
DECLS = {
 'in': ('\tvoid *buf = NULL;\n\n', '\tif (dir && name) {\n\t\tchar path[1024];\n\t\tsize_t size, alloc;\n\t\tint ok = 0;\n\n'),
 'mid': ('\tvoid *buf = NULL;\n\tsize_t size, alloc;\n\tint ok = 0;\n\n', '\tif (dir && name) {\n\t\tchar path[1024];\n\n'),
}


def variants():
    for (bn, b), (fn, f), (dn, (d1, d2)) in itertools.product(g21.B.items(), FREE.items(), DECLS.items()):
        body = b.replace('LOG', g.LOG).replace('RD', g.RD).replace('OK', g20.OK1).replace('P0', g20.P0)
        s = SIG + d1 + d2 + g.PREP + body + f + '\t}\n\treturn buf;\n}\n'
        yield '|'.join([bn, fn, dn]), s
