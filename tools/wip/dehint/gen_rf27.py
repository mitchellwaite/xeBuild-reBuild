"""Best shapes x readFileTo spellings that still match: the ghost in the compare block comes from the callee's `name && buf` estimate."""
import importlib.util, itertools, os


def load(n):
    spec = importlib.util.spec_from_file_location(n, os.path.join(os.path.dirname(__file__), n + '.py'))
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


OLD = '''	FILE *f;
	int ret = 0;

	if (name && buf && size) {
		f = fopen(name, "rb");
		if (f) {
			if (size <= (size_t)getFileSize(f)) {
				fread(buf, size, 1, f);
				fclose(f);
				ret = size;
			}
		}
	}
	return ret;
'''
CMP = 'size <= (size_t)getFileSize(f)'
READ = {
 'orig': OLD,
 'sz': '	FILE *f;\n	int ret = 0;\n\n	if (name && buf) {\n		if (size) {\n			f = fopen(name, "rb");\n			if (f && CMP) {\n				fread(buf, size, 1, f);\n				fclose(f);\n				ret = size;\n			}\n		}\n	}\n	return ret;\n',
 'sz2': '	FILE *f;\n	int ret = 0;\n\n	if (name && buf) {\n		if (size) {\n			f = fopen(name, "rb");\n			if (f) {\n				if (CMP) {\n					fread(buf, size, 1, f);\n					fclose(f);\n					ret = size;\n				}\n			}\n		}\n	}\n	return ret;\n',
 'and': '	FILE *f;\n	int ret = 0;\n\n	if (name && buf && size && (f = fopen(name, "rb")) != NULL) {\n		if (CMP) {\n			fread(buf, size, 1, f);\n			fclose(f);\n			ret = size;\n		}\n	}\n	return ret;\n',
 'and2': '	FILE *f;\n	int ret = 0;\n\n	if (name && buf && size && (f = fopen(name, "rb")) && CMP) {\n		fread(buf, size, 1, f);\n		fclose(f);\n		ret = size;\n	}\n	return ret;\n',
 'and3': '	FILE *f;\n	int ret = 0;\n\n	if (name && buf && size) {\n		f = fopen(name, "rb");\n		if (f && CMP) {\n			fread(buf, size, 1, f);\n			fclose(f);\n			ret = size;\n		}\n	}\n	return ret;\n',
}
G = {g: load(g) for g in ('gen_rf22', 'gen_rf23', 'gen_rf24', 'gen_rf25')}
PICK = [('gen_rf24', t) for t in ('a|mid|void', 'b|mid|void', 'i|mid|void')] + [('gen_rf23', t) for t in ('h2|1|ob|mid', 'h4|1|ob|mid', 'h5|1|ob|mid', 'h1n|1|ob|mid')] + [('gen_rf25', t) for t in ('bf|sep', 'err|sep', 'i1|sep', 'nf|sepn', 'asb|Aob', 'as|Dob', 'bf|Aob', 'nf|Aob', 'err|Aob', 'bf|Dob', 'nf|Dob', 'asb|sep', 'as|sep')] + [('gen_rf22', t) for t in ('c|ob|mid', 'd|ob|mid', 'e|ob|mid', 'g|ob|mid')]


def variants():
    srcs = {}
    for g, m in G.items():
        for v in m.variants():
            srcs[(g, v[0])] = v[1]
    for (g, t), (rn, r) in itertools.product(PICK, READ.items()):
        if (g, t) not in srcs:
            continue
        yield '|'.join([rn, g[-2:], t]), srcs[(g, t)], [], [(OLD, r.replace('CMP', CMP))]
