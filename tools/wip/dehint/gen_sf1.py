"""Copy-loop body forms: load order of c->blocks and c->data (a16's conflict with c),
fb before n, and locals for data/blocks.  Everything else natural."""
HEAD = '''int stfsGetFile(stfs_t *c, const char *name, uint8_t **out, uint32_t *len)
{
	int i = 0, done = 0;
	int j, n, fb;
	stfsEnt *e;
	uint8_t *buf;
%(decl)s
	while (!done) {
		if (checkZeros(c->fileTable + i * 64, 64))
			done = 1;
		else if (!stricmp(name, (char *)(c->fileTable + i * 64))) {
			e = (stfsEnt *)(c->fileTable + i * 64);
			if (e->contig) {
				buf = malloc((SWAP32(e->size) + 0xfff) & ~0xfff);
				if (buf)
					goto found;
			} else
				log_printf(0, "\\n\\n***** WARNING !!! file %%s is not contiguous and contents are being skipped!\\n\\n");
		}
		i++;
	}
	return 0;
found:
%(tail)s
	*out = buf;
	*len = SWAP32(e->size);
	return 1;
}
'''
ORDERS = {
    'nf': '\tn = LE24(e->ab);\n\tfb = LE24(e->fb);\n',
    'fn': '\tfb = LE24(e->fb);\n\tn = LE24(e->ab);\n',
}
LOOPS = {
    'plain': ('', '\tfor (j = 0; j < n; j++)\n\t\tmemcpy(buf + j * 0x1000, c->data + c->blocks[j + fb], 0x1000);\n'),
    'off': ('', '\tfor (j = 0; j < n; j++) {\n\t\tuint32_t off = c->blocks[j + fb];\n\t\tmemcpy(buf + j * 0x1000, c->data + off, 0x1000);\n\t}\n'),
    'off2': ('\tuint32_t off;\n', '\tfor (j = 0; j < n; j++) {\n\t\toff = c->blocks[j + fb];\n\t\tmemcpy(buf + j * 0x1000, c->data + off, 0x1000);\n\t}\n'),
    'revadd': ('', '\tfor (j = 0; j < n; j++)\n\t\tmemcpy(buf + j * 0x1000, c->blocks[j + fb] + c->data, 0x1000);\n'),
    'blkdata': ('', '\t{\n\t\tuint32_t *blocks = c->blocks;\n\t\tuint8_t *data = c->data;\n\t\tfor (j = 0; j < n; j++)\n\t\t\tmemcpy(buf + j * 0x1000, data + blocks[j + fb], 0x1000);\n\t}\n'),
    'datablk': ('', '\t{\n\t\tuint8_t *data = c->data;\n\t\tuint32_t *blocks = c->blocks;\n\t\tfor (j = 0; j < n; j++)\n\t\t\tmemcpy(buf + j * 0x1000, data + blocks[j + fb], 0x1000);\n\t}\n'),
    'ptrb': ('', '\t{\n\t\tuint32_t *b = c->blocks + fb;\n\t\tfor (j = 0; j < n; j++)\n\t\t\tmemcpy(buf + j * 0x1000, c->data + b[j], 0x1000);\n\t}\n'),
    'ptrb2': ('', '\t{\n\t\tuint32_t *b = &c->blocks[fb];\n\t\tuint8_t *d = c->data;\n\t\tfor (j = 0; j < n; j++)\n\t\t\tmemcpy(buf + j * 0x1000, d + b[j], 0x1000);\n\t}\n'),
    'kfb': ('', '\tfor (j = fb; j < fb + n; j++)\n\t\tmemcpy(buf + (j - fb) * 0x1000, c->data + c->blocks[j], 0x1000);\n'),
    'dest': ('', '\t{\n\t\tuint8_t *d = buf;\n\t\tfor (j = 0; j < n; j++, d += 0x1000)\n\t\t\tmemcpy(d, c->data + c->blocks[j + fb], 0x1000);\n\t}\n'),
}


def variants():
    for on, o in ORDERS.items():
        for ln, (d, l) in LOOPS.items():
            yield '%s|%s' % (on, ln), HEAD % {'decl': d, 'tail': o + l}
