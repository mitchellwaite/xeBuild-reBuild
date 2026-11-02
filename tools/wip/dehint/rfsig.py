"""Which readFileTo spellings keep readFileTo and readFileInTo matching.  Writes survivors to build/rf/rfsig.json as
[(tag, replacement text)], for use by generators."""
import concurrent.futures as cf, itertools, json, os, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
FNCMP = os.path.join(ROOT, 'tools', 're', 'fncmp.py')
BASE = open(os.path.join(ROOT, 'src', 'fileutil.c')).read()
A = BASE.index('size_t readFileTo(')
B = BASE.index('/*\n * readFileIn:')
OLD = BASE[A:B]
OUT = os.path.join(ROOT, 'build', 'rf', 'rfsig')
os.makedirs(OUT, exist_ok=True)

BODIES = {
 'ret': '''	FILE *f;
	RV ret = 0;

	if (name && buf && size) {
		f = fopen(name, "rb");
		if (f) {
			if (CMP) {
				fread(buf, size, 1, f);
				fclose(f);
				ret = size;
			}
		}
	}
	return ret;
''',
 'early': '''	FILE *f;

	if (name && buf && size) {
		f = fopen(name, "rb");
		if (f) {
			if (CMP) {
				fread(buf, size, 1, f);
				fclose(f);
				return size;
			}
		}
	}
	return 0;
''',
 'guard': '''	FILE *f;

	if (name == NULL || buf == NULL || size == 0)
		return 0;
	f = fopen(name, "rb");
	if (f == NULL)
		return 0;
	if (CMP) {
		fread(buf, size, 1, f);
		fclose(f);
		return size;
	}
	return 0;
''',
}
CMPS = {'a': 'size <= (size_t)getFileSize(f)', 'b': '(size_t)getFileSize(f) >= size', 'c': 'getFileSize(f) >= size'}
INTO = {'keep': 'uint32_t readFileInTo(const char *dir, const char *name, void *buf, int size)',
        'st': 'uint32_t readFileInTo(const char *dir, const char *name, void *buf, size_t size)',
        'r': 'size_t readFileInTo(const char *dir, const char *name, void *buf, size_t size)',
        'ri': 'int readFileInTo(const char *dir, const char *name, void *buf, int size)'}


def items():
    for rt, pt, (bn, b), rv, (cn, c), (ina, ins) in itertools.product(
            ['size_t', 'int', 'uint32_t', 'long'], ['size_t', 'int', 'uint32_t', 'long'], BODIES.items(),
            ['int', 'size_t', 'long'], CMPS.items(), INTO.items()):
        if bn != 'ret' and rv != 'int':
            continue
        body = b.replace('RV', rv).replace('CMP', c)
        text = '%s readFileTo(const char *name, void *buf, %s size)\n{\n%s}\n\n' % (rt, pt, body)
        idx = BASE.index('uint32_t readFileInTo(')
        tail = OLD[OLD.index('uint32_t readFileInTo('):].replace(INTO['keep'], ins)
        yield '|'.join([rt, pt, bn, rv, cn, ina]), text + tail


def run(a):
    i, (tag, text) = a
    p = os.path.join(OUT, 'v%d.c' % i)
    open(p, 'w', newline='\n').write(BASE[:A] + text + BASE[B:])
    for fn in ('readFileTo', 'readFileInTo'):
        r = subprocess.run([sys.executable, FNCMP, p, fn, '-O3', '-I', os.path.join(ROOT, 'src')], capture_output=True, text=True, cwd=ROOT)
        if (r.stdout + r.stderr).strip() != 'MATCH':
            os.remove(p)
            return None
    os.remove(p)
    return tag, text


def main():
    with cf.ThreadPoolExecutor(os.cpu_count() or 4) as ex:
        res = [r for r in ex.map(run, enumerate(items())) if r]
    json.dump({'old': OLD, 'sigs': res}, open(os.path.join(ROOT, 'build', 'rf', 'rfsig.json'), 'w'))
    print(len(res), 'survive')
    for t, _ in res:
        print(t)


main()
