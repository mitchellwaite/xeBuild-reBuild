"""Flag forms x combined tails (psize before free), unconditional readFileTo."""
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
FLAG = {
 'nf': ('ok = 0', '	if (buf == NULL)\n		LOG\n	else if (RD == size)\n		ok = 1;\n'),
 'bf': ('ok = 0', '	if (buf) {\n		if (RD == size)\n			ok = 1;\n	} else\n		LOG\n'),
 'i1': ('ok = 1', '	if (buf == NULL) {\n		LOG\n		ok = 0;\n	} else if (RD != size)\n		ok = 0;\n'),
 'i1b': ('ok = 1', '	if (buf) {\n		if (RD != size)\n			ok = 0;\n	} else {\n		LOG\n		ok = 0;\n	}\n'),
 'as': ('ok = 0', '	if (buf == NULL)\n		LOG\n	else\n		ok = RD == size;\n'),
 'asb': ('ok = 0', '	if (buf)\n		ok = RD == size;\n	else\n		LOG\n'),
 'as2': ('ok', '	if (buf == NULL) {\n		LOG\n		ok = 0;\n	} else\n		ok = RD == size;\n'),
 'bn': ('ok = buf != NULL', ''),
 'o1': ('ok = 0', '	if (buf) {\n		ok = 1;\n		if (RD != size)\n			ok = 0;\n	} else\n		LOG\n'),
 'o2': ('ok = 0', '	if (buf == NULL)\n		LOG\n	else {\n		ok = 1;\n		if (RD != size)\n			ok = 0;\n	}\n'),
 'err': ('err = 0', '	if (buf == NULL) {\n		LOG\n		err = 1;\n	} else if (RD != size)\n		err = 1;\n'),
 'errb': ('err = 1', '	if (buf == NULL)\n		LOG\n	else if (RD == size)\n		err = 0;\n'),
}
TAIL = {
 'sep': '	if (psize) {\n		if (ok)\n			*psize = alloc;\n		else\n			*psize = 0;\n	}\n	if (!ok && buf) {\n		free(buf);\n		buf = NULL;\n	}\n',
 'sepn': '	if (psize) {\n		if (!ok)\n			*psize = 0;\n		else\n			*psize = alloc;\n	}\n	if (buf && !ok) {\n		free(buf);\n		buf = NULL;\n	}\n',
 'cond': '	if (psize)\n		*psize = ok ? alloc : 0;\n	if (!ok && buf) {\n		free(buf);\n		buf = NULL;\n	}\n',
 'comb': '	if (ok) {\n		if (psize)\n			*psize = alloc;\n	} else {\n		if (psize)\n			*psize = 0;\n		if (buf) {\n			free(buf);\n			buf = NULL;\n		}\n	}\n',
 'combn': '	if (!ok) {\n		if (psize)\n			*psize = 0;\n		if (buf) {\n			free(buf);\n			buf = NULL;\n		}\n	} else if (psize)\n		*psize = alloc;\n',
 'combr': '	if (ok) {\n		if (psize)\n			*psize = alloc;\n		return buf;\n	}\n	if (psize)\n		*psize = 0;\n	if (buf) {\n		free(buf);\n		buf = NULL;\n	}\n',
 'combnf': '	if (!ok) {\n		if (psize)\n			*psize = 0;\n		if (buf)\n			free(buf);\n		return NULL;\n	}\n	if (psize)\n		*psize = alloc;\n',
 'mul': '	if (psize)\n		*psize = ok ? alloc : 0;\n	if (!ok) {\n		if (buf)\n			free(buf);\n		buf = NULL;\n	}\n',
 'mul2': '	if (!ok)\n		alloc = 0;\n	if (psize)\n		*psize = alloc;\n	if (!ok && buf) {\n		free(buf);\n		buf = NULL;\n	}\n',
}
ENTRY = {
 'nest': ('	if (dir && name) {\n', '	}\n'),
 'or': ('	if (dir == NULL || name == NULL)\n		return NULL;\n', ''),
}


def variants():
    for (en, (eo, ec)), (fn, (init, fl)), (tn, t), ty in itertools.product(ENTRY.items(), FLAG.items(), TAIL.items(), ['int', 'char', 'size_t']):
        tt = t
        if fn.startswith('err'):
            tt = tt.replace('!ok', 'err#').replace('ok', '!err').replace('err#', 'err')
        pre = PREP
        body = fl
        if fn == 'bn':
            decl = '\tvoid *buf;\n\tsize_t size, alloc;\n\t%s ok;\n\n' % ty
            buf = '	ok = buf != NULL;\n	if (!ok)\n		LOG\n	else if (RD != size)\n		ok = 0;\n'
            body = buf
            s = HEAD + decl.replace('void *buf;', 'void *buf = NULL;') + eo + pre + body.replace('LOG', LOG).replace('RD', RD) + tt + ec + '\treturn buf;\n}\n'
        else:
            decl = '\tvoid *buf = NULL;\n\tsize_t size, alloc;\n\t%s %s;\n\n' % (ty, init)
            s = HEAD + decl + eo + pre + body.replace('LOG', LOG).replace('RD', RD) + tt + ec + '\treturn buf;\n}\n'
        yield '|'.join([en, fn, tn, ty]), s
