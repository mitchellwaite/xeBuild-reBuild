"""Unconditional readFileTo with its result kept in a variable, tested afterwards.
Aim: the size==0 edge and the read-ok edge reach one `if (psize)` (as the hinted source's
two `ok = 1` do), while the buf arm keeps an unconditional call at profile_estimate."""
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
TEST = {
 'orA': '		if (got == size || size == 0)\n			ok = 1;\n',
 'orB': '		if (size == 0 || got == size)\n			ok = 1;\n',
 'nest': '		if (size) {\n			if (got == size)\n				ok = 1;\n		} else\n			ok = 1;\n',
 'nest0': '		if (size == 0)\n			ok = 1;\n		else if (got == size)\n			ok = 1;\n',
 'plain': '		if (got == size)\n			ok = 1;\n',
 'asg': '		ok = (got == size);\n',
 'asg2': '		ok = (size == 0 || got == size);\n',
 'asg3': '		ok = (got == size || size == 0);\n',
}
READ = {
 'nullfirst': '	if (buf == NULL)\n		LOG\n	else {\n		got = readFileTo(path, buf, size);\nTEST	}\n',
 'buffirst': '	if (buf) {\n		got = readFileTo(path, buf, size);\nTEST	} else\n		LOG\n',
}
PSIZE = {
 'cond': '	if (psize)\n		*psize = ok ? alloc : 0;\n',
 'ifelse': '	if (psize) {\n		if (ok)\n			*psize = alloc;\n		else\n			*psize = 0;\n	}\n',
 'okelse': '	if (psize) {\n		if (!ok)\n			*psize = 0;\n		else\n			*psize = alloc;\n	}\n',
}
FREE = {
 'okbuf': '	if (!ok && buf) {\n		free(buf);\n		buf = NULL;\n	}\n',
 'bufok': '	if (buf && !ok) {\n		free(buf);\n		buf = NULL;\n	}\n',
 'nest': '	if (!ok) {\n		if (buf) {\n			free(buf);\n			buf = NULL;\n		}\n	}\n',
 'nest2': '	if (buf) {\n		if (!ok) {\n			free(buf);\n			buf = NULL;\n		}\n	}\n',
}
OLD = '''size_t readFileTo(const char *name, void *buf, size_t size)
{
	FILE *f;
	int ret = 0;
'''
RET = ['int', 'size_t']
GOT = ['size_t', 'int']


def variants():
    for (en, (eo, ec)), (tn, t), (rn, r), (pn, p), (fn, f), ret, got in itertools.product(
            ENTRY.items(), TEST.items(), READ.items(), PSIZE.items(), FREE.items(), RET, GOT):
        decl = '\tvoid *buf = NULL;\n\tsize_t size, alloc;\n\t%s got;\n\tint ok = 0;\n\n' % got
        body = r.replace('TEST', t).replace('LOG', LOG)
        s = HEAD + decl + eo + PREP + body + p + f + ec + '\treturn buf;\n}\n'
        rep = [] if ret == 'int' else [(OLD, OLD.replace('int ret = 0', ret + ' ret = 0'))]
        yield '|'.join([en, tn, rn, pn, fn, ret, got]), s, [], rep
