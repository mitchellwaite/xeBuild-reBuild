"""Read-ok writes *psize and returns (one `if (psize)` for size==0 and read-ok); failures share a tail, and the free
is guarded by a flag or a compound test, so the return PHI keeps buf (not 0B) on the log path."""
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
}
# (flag init, body); F is the flag's set statement
BODY = {
 'a0': ('fail = 0', '	if (buf) {\n		if (RD == size) {\n		OK		}\n		fail = 1;\n	} else\n		LOG\n'),
 'b0': ('fail = 0', '	if (buf == NULL)\n		LOG\n	else {\n		if (RD == size) {\n		OK		}\n		fail = 1;\n	}\n'),
 'c0': ('fail = 0', '	if (buf == NULL)\n		LOG\n	else if (RD == size) {\n		OK	} else\n		fail = 1;\n'),
 'd0': ('fail = 0', '	if (buf) {\n		if (RD != size)\n			fail = 1;\n		else {\n		OK		}\n	} else\n		LOG\n'),
 'e1': ('fail = 1', '	if (buf == NULL) {\n		LOG\n		fail = 0;\n	} else if (RD == size) {\n		OK	}\n'),
 'f1': ('fail = 1', '	if (buf) {\n		if (RD == size) {\n		OK		}\n	} else {\n		LOG\n		fail = 0;\n	}\n'),
 'g':  ('fail', '	fail = buf != NULL;\n	if (fail) {\n		if (RD == size) {\n		OK		}\n	} else\n		LOG\n'),
 'h':  ('fail', '	fail = buf != NULL;\n	if (buf) {\n		if (RD == size) {\n		OK		}\n	} else\n		LOG\n'),
}
TAIL = {
 'f': '	if (psize)\n		*psize = 0;\n	if (fail) {\n		free(buf);\n		buf = NULL;\n	}\n',
 'fb': '	if (psize)\n		*psize = 0;\n	if (fail && buf) {\n		free(buf);\n		buf = NULL;\n	}\n',
 'bf': '	if (psize)\n		*psize = 0;\n	if (buf && fail) {\n		free(buf);\n		buf = NULL;\n	}\n',
 'fr': '	if (psize)\n		*psize = 0;\n	if (fail) {\n		free(buf);\n		return NULL;\n	}\n',
}


def variants():
    for (en, (eo, ec)), (bn, (init, b)), (tn, t), ty in itertools.product(ENTRY.items(), BODY.items(), TAIL.items(), ['int', 'char']):
        s = HEAD + '\tvoid *buf = NULL;\n\tsize_t size, alloc;\n\t%s %s;\n\n' % (ty, init) + eo + PREP + b.replace('LOG', LOG).replace('RD', RD).replace('OK', OK) + t + ec + '\treturn buf;\n}\n'
        yield '|'.join([en, bn, tn, ty]), s
