"""loadFileCrc with an error variable: each of the four early exits either returns or sets r and nests the rest (checkBl's lesson).  Hints off: no expect, no pin."""
import itertools


def ind(x, n=1):
    return ''.join('\t' * n + l + '\n' if l else '\n' for l in x.split('\n')[:-1])


def gate(cond, code, val, mode, rest):
    """cond true means failure"""
    if mode == 'ret':
        return '\tif (%s) {\n' % cond + ind(code) + '\t\treturn %s;\n\t}\n' % val + rest if code else '\tif (%s)\n\t\treturn %s;\n' % (cond, val) + rest
    return '\tif (%s) {\n' % cond + ind(code) + '\t\tr = %s;\n\t} else {\n' % val + ind(rest) + '\t}\n' if code else '\tif (%s)\n\t\tr = %s;\n\telse {\n' % (cond, val) + ind(rest) + '\t}\n'


VERB = {
    'n': '\tif (verbose) {\n\t\tif (size != e->size)\n\t\t\tlog_printf(1, "reading %s (0x%x b pad 0x%x b)", name, size, (size + 15) & ~15);\n\t\telse\n\t\t\tlog_printf(1, "reading %s (0x%x bytes)", name, size);\n\t}\n',
    'p': '\tif (pad && (size & 15)) {\n\t\tif (verbose)\n\t\t\tlog_printf(1, "reading %s (0x%x b pad 0x%x b)", name, size, (size + 15) & ~15);\n\t} else if (verbose)\n\t\tlog_printf(1, "reading %s (0x%x bytes)", name, size);\n',
}


def body(mf, mz, ma, mc, v, cl):
    tail = '\t\tc = crc32(e->data, size);\n\t\tlog_printf(1, " (crc32: 0x%08x ini: 0x%08x)\\n", c, crc);\n\t\tif (crc != c) {\n\t\t\tlog_printf(0, "\\n******WARNING: \'%s\' crc32: 0x%08x expected: 0x%08x\\n", name, c, crc);\n'
    tail += '\t\t\treturn 1;\n' if mc == 'ret' else '\t\t\tr = 1;\n'
    tail += '\t\t}\n'
    s = '\tfread(e->data, size, 1, f);\n\tfclose(f);\n\tif (crc) {\n' + tail + '\t} else\n\t\tlog_printf(1, "\\n");\n'
    s = gate('!e->data', '', '-2', ma, s)
    s = '\te->size = size;\n\tif (pad && (size & 15))\n\t\te->size = (size + 15) & ~15;\n' + VERB[v] + '\te->data = calloc(e->size + 0x10000, 1);\n' + s
    s = gate('!size', '\tfclose(f);\n\tlog_printf(0, "\\n******WARNING: \'%s\' is a 0 byte file, loading skipped!\\n", name);\n', '1', mz, s)
    s = '\tif (e->data)\n\t\tfree(e->data);\n\tsize = getFileSize(f);\n' + s
    s = gate('!f', '', '-1', mf, s)
    return '\tf = fopen(name, "rb");\n' + s


def CASES(base):
    a = base.index('int loadFileCrc(const char *name, struct fileent *e, int verbose, int pad, uint32_t crc)\n{')
    b = base.index('int readMetaFile(const char *name, uint8_t *meta)\n{')
    out = []
    M = ('ret', 'r')
    for mf, mz, ma, mc, v in itertools.product(M, M, M, M, VERB):
        s = 'int loadFileCrc(const char *name, struct fileent *e, int verbose, int pad, uint32_t crc)\n{\n\tFILE *f;\n\tsize_t size;\n\tuint32_t c;\n\tint r = 0;\n\n'
        s += body(mf, mz, ma, mc, v, 0) + '\treturn r;\n}\n\n'
        if (mf, mz, ma, mc) == ('ret',) * 4:
            s = s.replace('\tint r = 0;\n', '').replace('return r;', 'return 0;')
        out.append(('%s %s %s %s %s' % (mf, mz, ma, mc, v), base[:a] + s + base[b:]))
    return out
