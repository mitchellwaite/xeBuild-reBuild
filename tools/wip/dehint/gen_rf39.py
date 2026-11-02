"""Attempt 3: same readFileIn as the gen_rf38 match, calling readFileTo itself, with readFileTo's return/local types varied:
a cast in the return block should block the early split while `size_t ret` keeps the PHI arg uncast."""
import importlib.util, itertools, os


def load(n):
    spec = importlib.util.spec_from_file_location(n, os.path.join(os.path.dirname(__file__), n + '.py'))
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


g37 = load('gen_rf37')


def variants():
    for rt, lt, (sn, sh), dn, cast in itertools.product(['int', 'long', 'size_t', 'uint32_t', 'unsigned long', 'int32_t', 'ssize_t'], ['size_t', 'uint32_t', 'unsigned', 'unsigned long', 'long', 'int'], g37.SH.items(), ['d1', 'd2'], ['', '(size_t)']):
        rep = [('size_t readFileTo(const char *name', rt + ' readFileTo(const char *name'), ('	int ret = 0;\n\n	if (name && buf && size)', '	' + lt + ' ret = 0;\n\n	if (name && buf && size)')]
        d = g37.DIR[dn].replace('RD', cast + 'readFileTo(path, buf, size) == size')
        yield '|'.join([rt, lt, sn, dn, cast]), g37.wrap('', sh, d), [], rep
