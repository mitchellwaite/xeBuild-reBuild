"""No size test in readFileIn: readFileTo already checks size, and returns 0 for 0 (== size).
The size test then comes from the inlined callee, and the buf != NULL arm holds a call at
profile_estimate, which is what rf_hint faked."""
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

# (decls, code)
TAIL = {
 'ok_null': ('\tint ok = 0;\n', '''	if (buf == NULL)
		LOG
	else if (readFileTo(path, buf, size) == size)
		ok = 1;
	if (psize)
		*psize = ok ? alloc : 0;
	if (!ok && buf) {
		free(buf);
		buf = NULL;
	}
'''),
 'ok_if': ('\tint ok = 0;\n', '''	if (buf == NULL)
		LOG
	else if (readFileTo(path, buf, size) == size)
		ok = 1;
	if (psize) {
		if (ok)
			*psize = alloc;
		else
			*psize = 0;
	}
	if (!ok && buf) {
		free(buf);
		buf = NULL;
	}
'''),
 'chain': ('', '''	if (buf == NULL) {
		LOG
		if (psize)
			*psize = 0;
	} else if (readFileTo(path, buf, size) != size) {
		if (psize)
			*psize = 0;
		free(buf);
		buf = NULL;
	} else if (psize)
		*psize = alloc;
'''),
 'chain2': ('', '''	if (buf == NULL) {
		LOG
		if (psize)
			*psize = 0;
	} else {
		if (readFileTo(path, buf, size) == size) {
			if (psize)
				*psize = alloc;
		} else {
			if (psize)
				*psize = 0;
			free(buf);
			buf = NULL;
		}
	}
'''),
 'zero': ('', '''	if (buf == NULL) {
		LOG
		alloc = 0;
	} else if (readFileTo(path, buf, size) != size) {
		alloc = 0;
		free(buf);
		buf = NULL;
	}
	if (psize)
		*psize = alloc;
'''),
 'zero2': ('', '''	if (buf) {
		if (readFileTo(path, buf, size) != size) {
			free(buf);
			buf = NULL;
			alloc = 0;
		}
	} else {
		LOG
		alloc = 0;
	}
	if (psize)
		*psize = alloc;
'''),
 'got': ('\tsize_t got = 0;\n', '''	if (buf == NULL) {
		LOG
		size = 1;
	} else
		got = readFileTo(path, buf, size);
	if (psize)
		*psize = got == size ? alloc : 0;
	if (buf && got != size) {
		free(buf);
		buf = NULL;
	}
'''),
 'ok_assign': ('\tint ok = 0;\n', '''	if (buf == NULL)
		LOG
	else
		ok = readFileTo(path, buf, size) == size;
	if (psize)
		*psize = ok ? alloc : 0;
	if (!ok && buf) {
		free(buf);
		buf = NULL;
	}
'''),
 'ok_nofree2': ('\tint ok = 0;\n', '''	if (buf == NULL)
		LOG
	else if (readFileTo(path, buf, size) == size)
		ok = 1;
	if (!ok)
		alloc = 0;
	if (psize)
		*psize = alloc;
	if (!ok && buf) {
		free(buf);
		buf = NULL;
	}
'''),
 'ok_else': ('\tint ok = 0;\n', '''	if (buf == NULL)
		LOG
	else if (readFileTo(path, buf, size) == size)
		ok = 1;
	else {
		free(buf);
		buf = NULL;
	}
	if (psize)
		*psize = ok ? alloc : 0;
'''),
}


def variants():
    for (en, (eo, ec)), (tn, (d, t)), bt in itertools.product(ENTRY.items(), TAIL.items(), ['void', 'unsigned char']):
        s = HEAD + '\t%s *buf = NULL;\n\tsize_t size, alloc;\n%s\n' % (bt, d) + eo + PREP + t.replace('LOG', LOG) + ec + '\treturn buf;\n}\n'
        yield '%s|%s|%s' % (bt, en, tn), s
