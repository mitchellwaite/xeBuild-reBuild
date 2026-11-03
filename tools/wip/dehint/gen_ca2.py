"""What keeps the imul: access forms x index types x loop forms (guarded do-while)."""
import itertools

PREP = r'''
int prepSysex(void)
{
	if (netFormatSysex()) {
		if (netMount(SYSEX, "\\SEP"))
			return createSysexDirs();
		log_printf(0, "ERROR: unable to mount sysex partition!\n");
	} else
		log_printf(0, "ERROR: unable to format sysex partition!\n");
	return 0;
}
'''

HEAD = r'''
struct ent { void *data; uint32_t len; char path[1024]; };
long sendAvatarData(const char *dir, uint32_t ver)
{
	%(decl)s
	long ret;

	netTimerStart();
	log_printf(0, "loading avatar data...\n");
	ver &= ~0xf;
	addTitleId(ver);
	if (loadManifest(dir, ver)) {
		log_printf(0, "success!\nFormatting HDD partition...\n");
		ret = 1;
		if (prepSysex()) {
			log_printf(0, "success!\nSending avatar files to HDD partition...\n");
			log_printf(1, "sending %%d items to xbox\n", manifest.count);
			%(loop)s
			log_printf(1, "sending manifest to %%s\n", manifest.path);
			if (!netSendFile(manifest.path, manifest.data, manifest.size)) {
				ret = 0;
				log_printf(0, "aborting sending avatar data, failed to send %%s\n", manifest.path);
			} else {
				log_printf(0, "success! Avatar data is successfully sent to the console!\n");
				netTimerEnd();
				ret = 1;
			}
		}
out:
		netUnmount(SYSEX);
		freeManifest();
	} else {
		log_printf(0, "***** WARNING: avatar data skipped, unable to load data!\n");
		ret = 1;
	}
	return ret;
}
'''

# access: (pre-statements in the body, data, len, path)
ACC = {
    'idx': ('', 'manifest.e[%s].data', 'manifest.e[%s].len', 'manifest.e[%s].path'),
    'arith': ('', '(manifest.e + %s)->data', '(manifest.e + %s)->len', '(manifest.e + %s)->path'),
    'ptr': ('struct ent *e = (struct ent *)&manifest.e[%s];', 'e->data', 'e->len', 'e->path'),
    'ptr2': ('struct ent *e = (struct ent *)manifest.e + %s;', 'e->data', 'e->len', 'e->path'),
    'bytes': ('char *e = (char *)manifest.e + %s * sizeof(struct ent);', '*(void **)e', '*(uint32_t *)(e + 4)', 'e + 8'),
    'off': ('uint32_t off = %s * sizeof(struct ent);', '*(void **)((char *)manifest.e + off)', '*(uint32_t *)((char *)manifest.e + off + 4)', '(char *)manifest.e + off + 8'),
    'path': ('char *name = manifest.e[%s].path;', 'manifest.e[%s].data', 'manifest.e[%s].len', 'name'),
    'intaddr': ('uint32_t e = (uint32_t)manifest.e + %s * 1032;', '*(void **)e', '*(uint32_t *)(e + 4)', '(char *)(e + 8)'),
    'lenv': ('', 'manifest.e[%s].data', 'manifest.e[%s].len', 'manifest.e[%s].path'),
}

IDX = {
    'i': ('int i;', 'i', ''),
    'u': ('int i; uint32_t k;', 'k', 'k = i;'),
    'k': ('int i; int k;', 'k', 'k = i;'),
    'lk': ('int i; long k;', 'k', 'k = i;'),
    'llk': ('int i; long long k;', 'k', 'k = i;'),
    'sz': ('int i; size_t k;', 'k', 'k = i;'),
    'plus': ('int i;', '(i + 1 - 1)', ''),
}

LOOPS = {
    'do': ('if (manifest.count > 0) {\n i = 0;\n do {\n%s\n } while (++i < manifest.count);\n}'),
    'do2': ('i = 0;\n if (manifest.count > 0) do {\n%s\n i++;\n } while (i < manifest.count);'),
    'for': ('for (i = 0; i < manifest.count; i++) {\n%s\n}'),
    'wh': ('i = 0;\n while (i < manifest.count) {\n%s\n i++;\n}'),
    'forgd': ('if (manifest.count > 0) for (i = 0; i < manifest.count; i++) {\n%s\n}'),
    'inf': ('i = 0;\n if (manifest.count > 0) for (;;) {\n%s\n if (++i >= manifest.count) break;\n}'),
}


def body(acc, idx):
    pre, d, l, p = ACC[acc]
    _, x, kset = IDX[idx]
    f = lambda s: s % x if '%s' in s else s
    return r'''
	%s
	%s
	log_printf(1, "sending %%03d: 0x%%08x (%%d) bytes, %%s\n", i + 1, %s, %s, %s);
	ret = netSendFile(%s, %s, %s);
	if (!ret) {
		log_printf(0, "aborting sending avatar data, failed to send %%s\n", %s);
		goto out;
	}
''' % (kset, f(pre), f(l), f(l), f(p), f(p), f(d), f(l), f(p))


def variants():
    for acc, idx, lp in itertools.product(ACC, IDX, LOOPS):
        b = body(acc, idx).replace('%%', '%')
        src = PREP + HEAD % {'decl': IDX[idx][0], 'loop': (LOOPS[lp] % b.replace('%', '%%')).replace('%%', '%%')}
        yield '%s|%s|%s' % (acc, idx, lp), src
