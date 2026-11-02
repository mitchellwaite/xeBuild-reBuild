"""Entry check x tail, with goto/return forms (PRED_GOTO, PRED_TREE_EARLY_RETURN)."""
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
 'two': ('	if (dir == NULL)\n		return NULL;\n	if (name == NULL)\n		return NULL;\n', ''),
 'orbuf': ('	if (dir == NULL || name == NULL)\n		return buf;\n', ''),
 'gotoout': ('	if (dir == NULL || name == NULL)\n		goto out;\n', '	out:\n'),
 'notand': ('	if (!(dir && name))\n		return NULL;\n', ''),
}

TAIL = {
 'chain': '''	if (buf == NULL) {
		LOG
		if (psize)
			*psize = 0;
	} else if (size && readFileTo(path, buf, size) != size) {
		if (psize)
			*psize = 0;
		free(buf);
		buf = NULL;
	} else if (psize)
		*psize = alloc;
''',
 'chainret': '''	if (buf == NULL) {
		LOG
		if (psize)
			*psize = 0;
		return NULL;
	}
	if (size && readFileTo(path, buf, size) != size) {
		if (psize)
			*psize = 0;
		free(buf);
		return NULL;
	}
	if (psize)
		*psize = alloc;
''',
 'nestif': '''	if (buf) {
		if (size) {
			if (readFileTo(path, buf, size) != size) {
				if (psize)
					*psize = 0;
				free(buf);
				return NULL;
			}
		}
		if (psize)
			*psize = alloc;
	} else {
		LOG
		if (psize)
			*psize = 0;
	}
''',
 'nestif2': '''	if (buf == NULL) {
		LOG
		if (psize)
			*psize = 0;
	} else {
		if (size) {
			if (readFileTo(path, buf, size) != size) {
				if (psize)
					*psize = 0;
				free(buf);
				buf = NULL;
				goto done;
			}
		}
		if (psize)
			*psize = alloc;
	}
	done:
''',
 'gotofail': '''	if (buf == NULL) {
		LOG
		goto fail;
	}
	if (size && readFileTo(path, buf, size) != size)
		goto fail;
	if (psize)
		*psize = alloc;
	return buf;
fail:
	if (psize)
		*psize = 0;
	if (buf) {
		free(buf);
		buf = NULL;
	}
''',
 'gotofail2': '''	if (buf == NULL) {
		LOG
		goto fail;
	}
	if (size) {
		if (readFileTo(path, buf, size) != size)
			goto fail;
	}
	if (psize)
		*psize = alloc;
	return buf;
fail:
	if (psize)
		*psize = 0;
	free(buf);
	return NULL;
''',
 'nosize': '''	if (buf == NULL) {
		LOG
		alloc = 0;
		goto out2;
	}
	if (size && readFileTo(path, buf, size) != size) {
		alloc = 0;
		free(buf);
		buf = NULL;
	}
out2:
	if (psize)
		*psize = alloc;
''',
 'pfirst': '''	if (buf == NULL)
		LOG
	else {
		if (size == 0 || readFileTo(path, buf, size) == size) {
			if (psize)
				*psize = alloc;
			return buf;
		}
		if (psize)
			*psize = 0;
		free(buf);
		return NULL;
	}
	if (psize)
		*psize = 0;
''',
 'gotook': '''	if (buf == NULL) {
		LOG
		if (psize)
			*psize = 0;
		return buf;
	}
	if (size == 0)
		goto ok;
	if (readFileTo(path, buf, size) == size) {
ok:
		if (psize)
			*psize = alloc;
		return buf;
	}
	if (psize)
		*psize = 0;
	free(buf);
	buf = NULL;
''',
}


def variants():
    for (en, (eo, ec)), (tn, t) in itertools.product(ENTRY.items(), TAIL.items()):
        decl = '\tvoid *buf = NULL;\n\tsize_t size, alloc;\n\n'
        if en == 'gotoout':
            ec = '\tout:\n'
        yield '%s|%s' % (en, tn), HEAD + decl + eo + PREP + t.replace('LOG', LOG) + ec + '\treturn buf;\n}\n'
