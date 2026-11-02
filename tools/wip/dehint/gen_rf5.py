"""ok-flag family: the one that gets the comparison order and epilogue copies right."""
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

# how ok gets its value: (initial value, code)
READ = {
 'and0': (0, '''	if (buf) {
		if (size == 0 || readFileTo(path, buf, size) == size)
			ok = 1;
	} else
		LOG
'''),
 'nullfirst': (0, '''	if (buf == NULL)
		LOG
	else if (size == 0 || readFileTo(path, buf, size) == size)
		ok = 1;
'''),
 'nested': (0, '''	if (buf == NULL)
		LOG
	else {
		if (size) {
			if (readFileTo(path, buf, size) == size)
				ok = 1;
		} else
			ok = 1;
	}
'''),
 'nested0': (0, '''	if (buf == NULL)
		LOG
	else {
		if (size == 0)
			ok = 1;
		else if (readFileTo(path, buf, size) == size)
			ok = 1;
	}
'''),
 'init1': (1, '''	if (buf == NULL) {
		LOG
		ok = 0;
	} else if (size && readFileTo(path, buf, size) != size)
		ok = 0;
'''),
 'init1b': (1, '''	if (buf) {
		if (size && readFileTo(path, buf, size) != size)
			ok = 0;
	} else {
		LOG
		ok = 0;
	}
'''),
 'assign': (0, '''	if (buf == NULL)
		LOG
	else
		ok = (size == 0 || readFileTo(path, buf, size) == size);
'''),
 'assign2': (2, '''	if (buf == NULL) {
		LOG
		ok = 0;
	} else
		ok = (size == 0 || readFileTo(path, buf, size) == size);
'''),
 'rd': (0, '''	if (buf == NULL)
		LOG
	else {
		ok = 1;
		if (size)
			ok = readFileTo(path, buf, size) == size;
	}
'''),
}

PSIZE = {
 'cond': '	if (psize)\n		*psize = ok ? alloc : 0;\n',
 'ifelse': '	if (psize) {\n		if (ok)\n			*psize = alloc;\n		else\n			*psize = 0;\n	}\n',
 'mul': '	if (!ok)\n		alloc = 0;\n	if (psize)\n		*psize = alloc;\n',
 'okelse': '	if (psize) {\n		if (!ok)\n			*psize = 0;\n		else\n			*psize = alloc;\n	}\n',
}

FREE = {
 'okbuf': '	if (!ok && buf) {\n		free(buf);\n		buf = NULL;\n	}\n',
 'bufok': '	if (buf && !ok) {\n		free(buf);\n		buf = NULL;\n	}\n',
 'nest': '	if (!ok) {\n		if (buf) {\n			free(buf);\n			buf = NULL;\n		}\n	}\n',
 'nest2': '	if (buf) {\n		if (!ok) {\n			free(buf);\n			buf = NULL;\n		}\n	}\n',
 'nob': '	if (!ok) {\n		free(buf);\n		buf = NULL;\n	}\n',
}


def variants():
    for (en, (eo, ec)), (rn, (init, r)), (pn, p), (fn, f), ty in itertools.product(
            ENTRY.items(), READ.items(), PSIZE.items(), FREE.items(), ['int', 'BOOL']):
        decl = '\tvoid *buf = NULL;\n\tsize_t size, alloc;\n'
        decl += '\t%s ok = %d;\n\n' % (ty, init) if init != 2 else '\t%s ok;\n\n' % ty
        yield '%s|%s|%s|%s|%s' % (en, rn, pn, fn, ty), HEAD + decl + eo + PREP + r.replace('LOG', LOG) + p + f + ec + '\treturn buf;\n}\n'
