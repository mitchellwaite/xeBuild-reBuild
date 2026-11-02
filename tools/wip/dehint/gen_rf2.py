"""Types x align spelling x tail shape."""
import itertools

HEAD = 'void *readFileIn(const char *dir, const char *name, size_t *psize, size_t align)\n{\n\tchar path[1024];\n'
LOG = 'log_printf(1, "unable to allocate file buffer of 0x%x size!\\n", alloc);'

SIZE_T = ['size_t', 'long', 'int', 'unsigned int', 'uint32_t', 'unsigned long']
ALLOC_T = ['size_t', 'long', 'int']
CAST = ['', '(size_t)']

ALIGN = {
 'twostep': '''alloc = size;
	if (align) {
		alloc = size + align - 1;
		alloc &= -align;
	}''',
 'oneexpr': '''alloc = size;
	if (align)
		alloc = (size + align - 1) & -align;''',
 'mask': '''alloc = size;
	if (align)
		alloc = (size + (align - 1)) & ~(align - 1);''',
 'pluseq': '''alloc = size;
	if (align) {
		alloc += align - 1;
		alloc &= -align;
	}''',
 'cond': '''alloc = align ? (size + align - 1) & -align : size;''',
 'ifelse': '''if (align)
		alloc = (size + align - 1) & -align;
	else
		alloc = size;''',
}

TAIL = {
 'chain': '''	if (buf == NULL) {
		%s
		if (psize)
			*psize = 0;
	} else if (size && readFileTo(path, buf, size) != size) {
		if (psize)
			*psize = 0;
		free(buf);
		buf = NULL;
	} else if (psize)
		*psize = alloc;
''' % LOG,
 'zero': '''	if (buf == NULL) {
		%s
		alloc = 0;
	} else if (size && readFileTo(path, buf, size) != size) {
		if (psize)
			*psize = 0;
		free(buf);
		return NULL;
	}
	if (psize)
		*psize = alloc;
''' % LOG,
 'ok': '''	if (buf == NULL)
		%s
	else if (size == 0 || readFileTo(path, buf, size) == size)
		ok = 1;
	if (psize)
		*psize = ok ? alloc : 0;
	if (!ok && buf) {
		free(buf);
		buf = NULL;
	}
''' % LOG,
}

ENTRY = {
 'nest': ('	if (dir && name) {\n', '	}\n'),
 'early': ('	if (dir == NULL || name == NULL)\n		return NULL;\n', ''),
}


def variants():
    for st, at, c, (an, a), (tn, t), (en, (eo, ec)) in itertools.product(
            SIZE_T, ALLOC_T, CAST, ALIGN.items(), TAIL.items(), ENTRY.items()):
        decl = '\tvoid *buf = NULL;\n'
        if st == at:
            decl += '\t%s size, alloc;\n' % st
        else:
            decl += '\t%s size;\n\t%s alloc;\n' % (st, at)
        if tn == 'ok':
            decl += '\tint ok = 0;\n'
        body = ('	sprintf(path, "%%s%%s", dir, name);\n	size = %sgetFileSizeName(path);\n	%s\n	buf = calloc(alloc, 1);\n' % (c, a)) + t
        yield '%s|%s|%s|%s|%s|%s' % (st, at, c, an, tn, en), HEAD + decl + '\n' + eo + body + ec + '\treturn buf;\n}\n'
