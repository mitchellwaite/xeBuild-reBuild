"""First pass: plausible author shapes (hand-listed, from FileToBuffer's style)."""

HEAD = 'void *readFileIn(const char *dir, const char *name, size_t *psize, size_t align)\n{\n\tchar path[1024];\n'
PREP = '''	sprintf(path, "%s%s", dir, name);
	size = getFileSizeName(path);
	alloc = size;
	if (align) {
		alloc = size + align - 1;
		alloc &= -align;
	}
	buf = calloc(alloc, 1);
'''
LOG = 'log_printf(1, "unable to allocate file buffer of 0x%x size!\\n", alloc);'

SHAPES = {
# current one without hints
'cur': '''	void *buf = NULL;
	size_t size, alloc;
	int ok = 0;

	if (dir == NULL || name == NULL)
		return NULL;
''' + PREP + '''	if (buf == NULL)
		''' + LOG + '''
	else {
		if (size != 0) {
			if (readFileTo(path, buf, size) == size)
				ok = 1;
		} else
			ok = 1;
	}
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
	return buf;
''',
# nested, psize at the end of the block
'nested_ok': '''	void *buf = NULL;
	size_t size, alloc;
	int ok = 0;

	if (dir && name) {
''' + PREP + '''		if (buf) {
			if (size == 0 || readFileTo(path, buf, size) == size)
				ok = 1;
		} else
			''' + LOG + '''
		if (psize)
			*psize = ok ? alloc : 0;
		if (!ok && buf) {
			free(buf);
			buf = NULL;
		}
	}
	return buf;
''',
# got compared with size
'got': '''	void *buf = NULL;
	size_t size, alloc, got = 0;

	if (dir && name) {
''' + PREP + '''		if (buf == NULL) {
			''' + LOG + '''
			alloc = 0;
		} else {
			if (size)
				got = readFileTo(path, buf, size);
			if (got != size) {
				alloc = 0;
			}
		}
		if (psize)
			*psize = alloc;
		if (buf && got != size) {
			free(buf);
			buf = NULL;
		}
	}
	return buf;
''',
# ok, then one if for the whole tail
'okif': '''	void *buf = NULL;
	size_t size, alloc;
	int ok = 1;

	if (dir && name) {
''' + PREP + '''		if (buf == NULL) {
			''' + LOG + '''
			ok = 0;
		} else if (size && readFileTo(path, buf, size) != size)
			ok = 0;
		if (ok) {
			if (psize)
				*psize = alloc;
		} else {
			if (psize)
				*psize = 0;
			if (buf) {
				free(buf);
				buf = NULL;
			}
		}
	}
	return buf;
''',
# bRead carries the result (FileToBuffer)
'bread': '''	void *buf = NULL;
	size_t size, alloc;
	size_t bRead = 0;

	if (dir && name) {
''' + PREP + '''		if (buf == NULL)
			''' + LOG + '''
		else if (size == 0 || readFileTo(path, buf, size) == size)
			bRead = alloc;
		else {
			if (psize)
				*psize = 0;
			free(buf);
			return NULL;
		}
		if (psize)
			*psize = bRead;
	}
	return buf;
''',
'gotofail': '''	void *buf = NULL;
	size_t size, alloc;

	if (dir && name) {
''' + PREP + '''		if (buf == NULL) {
			''' + LOG + '''
			if (psize)
				*psize = 0;
		} else if (size && readFileTo(path, buf, size) != size) {
			if (psize)
				*psize = 0;
			free(buf);
			buf = NULL;
		} else if (psize)
			*psize = alloc;
	}
	return buf;
''',
}


def variants():
    for k, body in SHAPES.items():
        yield k, HEAD + body + '}\n'
