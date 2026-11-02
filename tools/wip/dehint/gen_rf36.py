"""Attempt 3: read code written in readFileIn itself (no folded name/buf tests, so no ghost frequency on the fread block)."""
import importlib.util, itertools, os


def load(n):
    spec = importlib.util.spec_from_file_location(n, os.path.join(os.path.dirname(__file__), n + '.py'))
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


g = load('gen_rf14')
g31 = load('gen_rf31')
g35 = load('gen_rf35')
SIG, P0, FRE = g31.SIG, g31.P0, g31.FRE
PS = dict(g35.PS)
READ = '''if (size <= (size_t)getFileSize(f)) {
				fread(buf, size, 1, f);
				fclose(f);
				SET
			}
'''
RS = {
 'got0': ('FILE *f;\nsize_t got = 0;\n', 'if (size) {\n f = fopen(path, "rb");\n if (f) {\n' + READ.replace('SET', 'got = size;') + '}\n}\nint ok = got == size;\n'),
 'got1': ('FILE *f;\nsize_t got = 0;\n', 'if (size) {\n f = fopen(path, "rb");\n if (f) {\n' + READ.replace('SET', 'got = size;') + '}\n}\nint ok = 0;\nif (got == size)\n ok = 1;\n'),
 'one': ('FILE *f;\nint ok = 1;\n', 'if (size) {\n ok = 0;\n f = fopen(path, "rb");\n if (f) {\n' + READ.replace('SET', 'ok = 1;') + '}\n}\n'),
 'zero': ('FILE *f;\nint ok = 0;\n', 'if (size) {\n f = fopen(path, "rb");\n if (f) {\n' + READ.replace('SET', 'ok = 1;') + '}\n} else\n ok = 1;\n'),
 'zero2': ('FILE *f;\nint ok = 0;\n', 'if (size == 0)\n ok = 1;\nelse {\n f = fopen(path, "rb");\n if (f) {\n' + READ.replace('SET', 'ok = 1;') + '}\n}\n'),
 'nosz': ('FILE *f;\nint ok = !size;\n', 'if (size) {\n f = fopen(path, "rb");\n if (f) {\n' + READ.replace('SET', 'ok = 1;') + '}\n}\n'),
}
FR = {'if': '		if (!ok) {\n' + FRE + '		}\n'}
SH = {
 'nf': '	if (buf == NULL) {\n		LOG\nP0	} else {\n		BODY	}\n',
 'bf': '	if (buf) {\n		BODY	} else {\n		LOG\nP0	}\n',
}


def variants():
    for (sn, sh), (rn, (decl, rd)), (pn, p) in itertools.product(SH.items(), RS.items(), PS.items()):
        body = decl + rd + p + FR['if']
        b = sh.replace('LOG', g.LOG).replace('P0', P0).replace('BODY', body)
        s = SIG + '\tvoid *buf = NULL;\n\tsize_t size, alloc;\n\n\tif (dir && name) {\n\t\tchar path[1024];\n\n' + g.PREP + b + '\t}\n\treturn buf;\n}\n'
        yield '|'.join([sn, rn, pn]), s
    # flagless with goto
    for (sn, sh), (pn, tail) in itertools.product(SH.items(), {
      'g1': 'if (psize)\n *psize = alloc;\nreturn buf;\nfail:\nif (psize)\n *psize = 0;\nfree(buf);\nbuf = NULL;\n',
      'g2': 'if (psize)\n *psize = alloc;\ngoto done;\nfail:\nif (psize)\n *psize = 0;\nfree(buf);\nbuf = NULL;\ndone:;\n',
      'g3': 'if (psize)\n *psize = alloc;\nif (0) {\nfail:\nif (psize)\n *psize = 0;\nfree(buf);\nbuf = NULL;\n}\n',
    }.items()):
        rd = 'FILE *f;\nif (size) {\n f = fopen(path, "rb");\n if (f == NULL)\n goto fail;\n if (size > (size_t)getFileSize(f))\n goto fail;\n fread(buf, size, 1, f);\n fclose(f);\n}\n'
        b = sh.replace('LOG', g.LOG).replace('P0', P0).replace('BODY', rd + tail)
        s = SIG + '\tvoid *buf = NULL;\n\tsize_t size, alloc;\n\n\tif (dir && name) {\n\t\tchar path[1024];\n\n' + g.PREP + b + '\t}\n\treturn buf;\n}\n'
        yield '|'.join([sn, 'goto', pn]), s
