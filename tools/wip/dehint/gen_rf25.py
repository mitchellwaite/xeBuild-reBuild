"""gen_rf14's flag forms x tails under the scoped path, plus comb forms that were dead before (0B forwarders can no longer merge with dir-null's)."""
import importlib.util, itertools, os


def load(n):
    spec = importlib.util.spec_from_file_location(n, os.path.join(os.path.dirname(__file__), n + '.py'))
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


g = load('gen_rf14')
g19 = load('gen_rf19')
SIG = 'void *readFileIn(const char *dir, const char *name, size_t *psize, size_t align)\n{\n'
TAILS = dict(g.TAIL)
for p, f in itertools.product(g19.PS.items(), g19.FREE.items()):
    TAILS[p[0] + f[0]] = p[1] + f[1]


def variants():
    for (fn, (init, fl)), (tn, t) in itertools.product(g.FLAG.items(), TAILS.items()):
        tt = t
        if fn.startswith('err'):
            tt = tt.replace('!ok', 'err#').replace('ok', '!err').replace('err#', 'err')
        if fn == 'bn':
            continue
        s = SIG + '\tvoid *buf = NULL;\n\tsize_t size, alloc;\n\tint %s;\n\n' % init + '\tif (dir && name) {\n\t\tchar path[1024];\n\n' + g.PREP + fl.replace('LOG', g.LOG).replace('RD', g.RD) + tt + '\t}\n\treturn buf;\n}\n'
        yield '|'.join([fn, tn]), s
