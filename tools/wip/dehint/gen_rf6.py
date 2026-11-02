"""DIAGNOSTIC ONLY (hints are not a MATCH): can branch frequencies alone give the
reference's registers, with no pin?  Puts __builtin_expect on every branch of the
function, across probabilities.  If nothing reaches size=edi/buf=ebx the registers
aren't a frequency question."""
import itertools

HEAD = 'void *readFileIn(const char *dir, const char *name, size_t *psize, size_t align)\n{\n\tchar path[1024];\n'


def body(ea, eb, es, er, ed):
    def E(c, v):
        return c if v is None else '__builtin_expect(%s, %d)' % (c, v)
    return HEAD + '''	void *buf = NULL;
	size_t size, alloc;

	if (%s) {
		sprintf(path, "%%s%%s", dir, name);
		size = getFileSizeName(path);
		alloc = size;
		if (%s) {
			alloc = size + align - 1;
			alloc &= -align;
		}
		buf = calloc(alloc, 1);
		if (%s) {
			log_printf(1, "unable to allocate file buffer of 0x%%x size!\\n", alloc);
			if (psize)
				*psize = 0;
		} else if (%s && %s) {
			if (psize)
				*psize = 0;
			free(buf);
			buf = NULL;
		} else if (psize)
			*psize = alloc;
	}
	return buf;
}
''' % (E('dir && name', ed), E('align != 0', ea), E('buf == NULL', eb), E('size != 0', es), E('readFileTo(path, buf, size) != size', er))


def variants():
    V = [None, 0, 1]
    for ed, ea, eb, es, er, p in itertools.product(V, V, V, V, V, [55, 65, 80, 95]):
        yield 'd=%s a=%s b=%s s=%s r=%s p=%d' % (ed, ea, eb, es, er, p), body(ea, eb, es, er, ed), ['--param', 'builtin-expect-probability=%d' % p]
