"""Product around gen_rf9's ok_if: no size test in the caller."""
import itertools

HEAD = 'void *readFileIn(const char *dir, const char *name, size_t *psize, size_t align)\n{\n\tchar path[1024];\n'
LOG = 'log_printf(1, "unable to allocate file buffer of 0x%x size!\\n", alloc);'
PREP = '''	sprintf(path, "%s%s", dir, name);
	size = getFileSizeName(path);
	alloc = size;
	if (align) {
		alloc = size + align - 1;
		alloc &= -align;
	}
	buf = calloc(alloc, 1);
'''
ENTRY = {
 'nest': ('	if (dir && name) {\n', '	}\n'),
 'or': ('	if (dir == NULL || name == NULL)\n		return NULL;\n', ''),
}
READ = {
 'nullfirst': (0, '''	if (buf == NULL)
		LOG
	else if (readFileTo(path, buf, size) == size)
		ok = 1;
'''),
 'buffirst': (0, '''	if (buf) {
		if (readFileTo(path, buf, size) == size)
			ok = 1;
	} else
		LOG
'''),
 'init1': (1, '''	if (buf == NULL) {
		LOG
		ok = 0;
	} else if (readFileTo(path, buf, size) != size)
		ok = 0;
'''),
 'init1b': (1, '''	if (buf) {
		if (readFileTo(path, buf, size) != size)
			ok = 0;
	} else {
		LOG
		ok = 0;
	}
'''),
 'assign': (0, '''	if (buf == NULL)
		LOG
	else
		ok = readFileTo(path, buf, size) == size;
'''),
 'assign2': (2, '''	if (buf == NULL) {
		LOG
		ok = 0;
	} else
		ok = readFileTo(path, buf, size) == size;
'''),
 'got': (3, '''	if (buf == NULL)
		LOG
	else
		got = readFileTo(path, buf, size);
	ok = buf && got == size;
'''),
}
PSIZE = {
 'cond': '	if (psize)\n		*psize = ok ? alloc : 0;\n',
 'ifelse': '	if (psize) {\n		if (ok)\n			*psize = alloc;\n		else\n			*psize = 0;\n	}\n',
 'okelse': '	if (psize) {\n		if (!ok)\n			*psize = 0;\n		else\n			*psize = alloc;\n	}\n',
 'mul': '	if (!ok)\n		alloc = 0;\n	if (psize)\n		*psize = alloc;\n',
 'two': '	if (psize && ok)\n		*psize = alloc;\n	else if (psize)\n		*psize = 0;\n',
}
FREE = {
 'okbuf': '	if (!ok && buf) {\n		free(buf);\n		buf = NULL;\n	}\n',
 'bufok': '	if (buf && !ok) {\n		free(buf);\n		buf = NULL;\n	}\n',
 'nest': '	if (!ok) {\n		if (buf) {\n			free(buf);\n			buf = NULL;\n		}\n	}\n',
 'nest2': '	if (buf) {\n		if (!ok) {\n			free(buf);\n			buf = NULL;\n		}\n	}\n',
 'nob': '	if (!ok) {\n		free(buf);\n		buf = NULL;\n	}\n',
}


def variants():
    for (en, (eo, ec)), (rn, (init, r)), (pn, p), (fn, f), bt, order in itertools.product(
            ENTRY.items(), READ.items(), PSIZE.items(), FREE.items(), ['void', 'unsigned char'], ['pf', 'fp']):
        d = {0: '\tint ok = 0;\n', 1: '\tint ok = 1;\n', 2: '\tint ok;\n', 3: '\tint ok;\n\tsize_t got = 0;\n'}[init]
        tail = p + f if order == 'pf' else f + p
        s = HEAD + '\t%s *buf = NULL;\n\tsize_t size, alloc;\n%s\n' % (bt, d) + eo + PREP + r.replace('LOG', LOG) + tail + ec + '\treturn buf;\n}\n'
        yield '|'.join([bt, en, rn, pn, fn, order]), s
