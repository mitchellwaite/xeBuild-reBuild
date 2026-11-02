"""gen_rf10 x readFileTo's ret type: `int ret` puts casts between the PHI and the size compare,
so the read-ok edge threads a pass later than the size==0 edge and gets its own psize test."""
import importlib.util, os


def load(n):
    spec = importlib.util.spec_from_file_location(n, os.path.join(os.path.dirname(__file__), n + '.py'))
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


OLD = '''size_t readFileTo(const char *name, void *buf, size_t size)
{
	FILE *f;
	int ret = 0;
'''
RET = ['size_t', 'unsigned int', 'uint32_t', 'long']


def variants():
    for tag, s in load('gen_rf10').variants():
        if not tag.startswith('void') or '|nest|' not in tag:
            continue
        for r in RET:
            yield tag + '|ret=' + r, s, [], [(OLD, OLD.replace('int ret = 0', r + ' ret = 0'))]
