"""Attempt 3: static helper with size_t ret and folded tests above size."""
import importlib.util, itertools, os


def load(n):
    spec = importlib.util.spec_from_file_location(n, os.path.join(os.path.dirname(__file__), n + '.py'))
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


g37 = load('gen_rf37')
BODY = '''	FILE *f;
	size_t ret = 0;

	if (COND) {
		f = fopen(name, "rb");
		if (f) {
			if (size <= (size_t)getFileSize(f)) {
				fread(buf, size, 1, f);
				fclose(f);
				ret = size;
			}
		}
	}
	return ret;
}

'''
HEAD = 'static size_t readData(const char *name, void *buf, size_t size)\n{\n'
CONDS = ['name && buf && size', 'buf && size', 'name && size', 'buf && name && size', 'size && name && buf', 'size && buf', 'name && size && buf', 'buf && size && name']


def variants():
    for c, (sn, sh) in itertools.product(CONDS, g37.SH.items()):
        h = HEAD + BODY.replace('COND', c)
        rd = 'readData(path, buf, size) == size'
        for dn, d in g37.DIR.items():
            yield '|'.join([c, sn, dn]), g37.wrap(h, sh, d.replace('RD', rd))
        for (fn, fl), (pn, p) in itertools.product(g37.FL.items(), g37.PS.items()):
            yield '|'.join([c, sn, fn, pn]), g37.wrap(h, sh, fl.replace('RD', rd) + p + g37.FR)
