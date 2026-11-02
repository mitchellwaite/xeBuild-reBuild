"""Separate `*psize = 0` per failure (no flag), unconditional readFileTo: nothing to thread on the
failure paths, so the log path can't merge with the read failure at GIMPLE level."""
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
P0 = '		if (psize)\n			*psize = 0;\n'
FRE = '		free(buf);\n		buf = NULL;\n'
FRR = '		free(buf);\n		return NULL;\n'
OKP = 'if (psize)\n			*psize = alloc;\n'
TAIL = {
 'a': '	if (buf == NULL) {\n		LOG\n' + P0 + '	} else if (readFileTo(path, buf, size) != size) {\n' + P0 + FRE + '	} else if (psize)\n		*psize = alloc;\n',
 'b': '	if (buf == NULL) {\n		LOG\n' + P0 + '	} else if (readFileTo(path, buf, size) == size) {\n		' + OKP + '	} else {\n' + P0 + FRE + '	}\n',
 'c': '	if (buf) {\n		if (readFileTo(path, buf, size) == size) {\n		' + OKP + '		} else {\n' + P0 + FRE + '		}\n	} else {\n		LOG\n' + P0 + '	}\n',
 'd': '	if (buf) {\n		if (readFileTo(path, buf, size) != size) {\n' + P0 + FRE + '		} else if (psize)\n			*psize = alloc;\n	} else {\n		LOG\n' + P0 + '	}\n',
 'e': '	if (buf == NULL) {\n		LOG\n' + P0 + '		return buf;\n	}\n	if (readFileTo(path, buf, size) != size) {\n' + P0 + FRE + '		return buf;\n	}\n	if (psize)\n		*psize = alloc;\n',
 'f': '	if (buf == NULL) {\n		LOG\n' + P0 + '		return NULL;\n	}\n	if (readFileTo(path, buf, size) != size) {\n' + P0 + FRR + '	}\n	if (psize)\n		*psize = alloc;\n',
 'g': '	if (buf == NULL) {\n		LOG\n' + P0 + '		return buf;\n	}\n	if (readFileTo(path, buf, size) == size) {\n		' + OKP + '		return buf;\n	}\n' + P0 + FRE,
 'h': '	if (buf == NULL) {\n		LOG\n' + P0 + '	} else {\n		if (readFileTo(path, buf, size) != size) {\n' + P0 + FRE + '			goto done;\n		}\n		' + OKP + '	}\ndone:\n',
 'i': '	if (buf == NULL) {\n		LOG\n		goto fail;\n	}\n	if (readFileTo(path, buf, size) == size) {\n		' + OKP + '		return buf;\n	}\n' + P0 + '	free(buf);\n	return NULL;\nfail:\n' + P0,
 'j': '	if (buf != NULL) {\n		if (readFileTo(path, buf, size) == size) {\n		' + OKP + '			return buf;\n		}\n' + P0 + FRE + '		return buf;\n	}\n	LOG\n' + P0,
 'k': '	if (buf == NULL)\n		LOG\n	else if (readFileTo(path, buf, size) == size) {\n		' + OKP + '		return buf;\n	} else {\n		free(buf);\n		buf = NULL;\n	}\n' + P0,
 'l': '	if (buf == NULL)\n		LOG\n	else {\n		if (readFileTo(path, buf, size) == size) {\n		' + OKP + '			return buf;\n		}\n		alloc = 0;\n	}\n' + P0 + '	if (buf) {\n		free(buf);\n		buf = NULL;\n	}\n',
}
OLD = '''size_t readFileTo(const char *name, void *buf, size_t size)
{
	FILE *f;
	int ret = 0;
'''


def variants():
    for (en, (eo, ec)), (tn, t), bt, ret in itertools.product(ENTRY.items(), TAIL.items(), ['void', 'unsigned char'], ['int', 'size_t']):
        s = HEAD + '\t%s *buf = NULL;\n\tsize_t size, alloc;\n\n' % bt + eo + PREP + t.replace('LOG', LOG) + ec + '\treturn buf;\n}\n'
        rep = [] if ret == 'int' else [(OLD, OLD.replace('int ret = 0', ret + ' ret = 0'))]
        yield '|'.join([bt, en, tn, ret]), s, [], rep
