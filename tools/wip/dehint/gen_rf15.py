"""No flag: read-ok writes *psize and returns; every failure falls into one common tail
(`if (psize) *psize = 0; if (buf) { free }`), which threading then splits, as in the reference."""
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
RD = 'readFileTo(path, buf, size)'
OK = 'if (psize)\n\t\t\t*psize = alloc;\n\t\treturn buf;\n'
ENTRY = {
 'nest': ('	if (dir && name) {\n', '	}\n'),
 'or': ('	if (dir == NULL || name == NULL)\n		return NULL;\n', ''),
 'ifn': ('	if (dir == NULL)\n		return NULL;\n	if (name == NULL)\n		return NULL;\n', ''),
}
BODY = {
 'a': '	if (buf) {\n		if (RD == size) {\n		OK		}\n	} else\n		LOG\n',
 'b': '	if (buf == NULL)\n		LOG\n	else if (RD == size) {\n		OK	}\n',
 'c': '	if (buf == NULL) {\n		LOG\n		goto fail;\n	}\n	if (RD == size) {\n		OK	}\nfail:\n',
 'd': '	if (buf) {\n		if (RD != size)\n			goto fail;\n		OK	}\n	LOG\nfail:\n',
 'e': '	if (buf == NULL)\n		LOG\n	else {\n		if (RD != size)\n			goto fail;\n		OK	}\nfail:\n',
}
TAIL = {
 'p': '	if (psize)\n		*psize = 0;\n	if (buf) {\n		free(buf);\n		buf = NULL;\n	}\n',
 'r': '	if (psize)\n		*psize = 0;\n	if (buf)\n		free(buf);\n	return NULL;\n',
 'n': '	if (psize)\n		*psize = 0;\n	if (buf != NULL) {\n		free(buf);\n		return NULL;\n	}\n',
}
OLD = '''size_t readFileTo(const char *name, void *buf, size_t size)
{
	FILE *f;
	int ret = 0;
'''


def variants():
    for (en, (eo, ec)), (bn, b), (tn, t), bt, ret in itertools.product(ENTRY.items(), BODY.items(), TAIL.items(), ['void', 'unsigned char'], ['int', 'size_t']):
        s = HEAD + '\t%s *buf = NULL;\n\tsize_t size, alloc;\n\n' % bt + eo + PREP + b.replace('LOG', LOG).replace('RD', RD).replace('OK', OK) + t + ec + '\treturn buf;\n}\n'
        rep = [] if ret == 'int' else [(OLD, OLD.replace('int ret = 0', ret + ' ret = 0'))]
        yield '|'.join([bt, en, bn, tn, ret]), s, [], rep
