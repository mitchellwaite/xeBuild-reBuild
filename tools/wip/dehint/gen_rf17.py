"""gen_rf14's flag forms x the type of size/alloc in readFileIn.  With a signed `size`, `(size_t)ret == (size_t)size` can fold to
`ret == size`, so vrp1 can thread read-ok together with size==0 while readFileTo keeps `int ret` (no early split)."""
import itertools, importlib.util, os


def load(n):
    spec = importlib.util.spec_from_file_location(n, os.path.join(os.path.dirname(__file__), n + '.py'))
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


g = load('gen_rf14')
TY = ['int', 'long', 'unsigned long']
ATY = ['size_t', 'int', 'long']


def variants():
    for (en, (eo, ec)), (fn, (init, fl)), (tn, t) in itertools.product(g.ENTRY.items(), g.FLAG.items(), g.TAIL.items()):
        if fn in ('err', 'errb', 'bn'):
            continue
        for sty, aty in itertools.product(TY, ATY):
            decl = '\tvoid *buf = NULL;\n\t%s size;\n\t%s alloc;\n\tint %s;\n\n' % (sty, aty, init)
            s = g.HEAD + decl + eo + g.PREP + fl.replace('LOG', g.LOG).replace('RD', g.RD) + t + ec + '\treturn buf;\n}\n'
            yield '|'.join([en, fn, tn, sty, aty]), s
