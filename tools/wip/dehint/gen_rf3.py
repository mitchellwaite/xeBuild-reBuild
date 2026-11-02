"""Diagnostics only (hints allowed): which hint fixes which part of the chain shape's diff."""
import itertools

BODY = '''	void *buf = NULL;
	size_t size, alloc;

	if (dir && name) {
		sprintf(path, "%%s%%s", dir, name);
		size = getFileSizeName(path);
		alloc = size;
		if (align) {
			alloc = size + align - 1;
			alloc &= -align;
		}
		buf = calloc(alloc, 1);
		if (buf == NULL) {
			log_printf(1, "unable to allocate file buffer of 0x%%x size!\\n", alloc);
			if (psize)
				*psize = 0;
		} else if (%s && readFileTo(path, buf, size) != size) {
			if (psize)
				*psize = 0;
			free(buf);
			buf = NULL;
		} else if (psize)
			*psize = alloc;
	}
	return buf;
'''


def variants():
    for noei, exp in itertools.product([0, 1], [0, 1]):
        s = ''
        if noei:
            s += '__attribute__((optimize("no-early-inlining")))\n'
        s += 'void *readFileIn(const char *dir, const char *name, size_t *psize, size_t align)\n{\n\tchar path[1024];\n'
        s += BODY % ('__builtin_expect(size != 0, 0)' if exp else 'size')
        yield 'noei=%d exp=%d' % (noei, exp), s + '}\n'
