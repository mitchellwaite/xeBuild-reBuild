"""Attempt 6: the plain for loop with the frame around it varied, for the free-list number PRE gives the inlined freeManifest's count. gen_ca84 found
`uint32_t r ... r = createSysexDirs(); return r` flips it, but that prepSysex can't match standalone. Axes: ret init x prepSysex call x loadManifest test x ver x
prepSysex spelling x body."""
import itertools, os
from importlib import util

here = os.path.dirname(os.path.abspath(__file__))


def load(n):
    s = util.spec_from_file_location(n, os.path.join(here, n + '.py'))
    m = util.module_from_spec(s)
    s.loader.exec_module(m)
    return m


g = load('gen_ca80')
g10 = load('gen_ca10')
LOOPS = {
    'F1': 'n = manifest.count;\nfor (i = 0; i < n; i++) {\n@I@@L@\n@S@\nif (!ret) {\n@F@\ni = n;\n} else\nn = manifest.count;\n}\n',
    'G': 'for (i = 0; i < manifest.count; i++) {\n@I@@L@\n@S@\nif (!ret) {\n@F@\ni = manifest.count;\n}\n}\n',
}
RET = ('r0', 'r1')
CALL = {
    'p0': ('if (prepSysex()) {', ''),
    'p1': ('ok = prepSysex();\n\t\tif (ok) {', '\tint ok;\n'),
    'p2': ('ok = prepSysex();\n\t\tif (ok) {', '\tuint32_t ok;\n'),
    'p3': ('ok = prepSysex();\n\t\tif (ok) {', '\tlong ok;\n'),
    'p4': ('if (prepSysex() != 0) {', ''),
}
LM = {
    'l0': ('if (loadManifest(dir, ver)) {', ''),
    'l1': ('ok2 = loadManifest(dir, ver);\n\tif (ok2) {', '\tuint32_t ok2;\n'),
    'l2': ('ok2 = loadManifest(dir, ver);\n\tif (ok2) {', '\tint ok2;\n'),
}
VER = {
    'v0': ('ver &= ~0xf;\n', ''),
    'v1': ('ver = ver & 0xfffffff0;\n', ''),
}
PREPS = ['h9d', 'h5d', 'h7d', 'h6d', 'h1d', 'h13d', 'h9f', 'h10d']
ITEM = {'x': 'manifest.e[i].', 'e': 'e->'}


def prep(p):
    return 'int prepSysex(void)\n{\n' + g10.HEADS[p[:-1]] + g10.TAIL[p[-1]] + '\n}\n\n'


def variants():
    for l, r, c, m, v, p, it in itertools.product(LOOPS, RET, CALL, LM, VER, PREPS, ITEM):
        decl = '' if it == 'x' else 'struct manifestItem *e = &manifest.e[i];\n'
        loop = LOOPS[l].replace('@I@', decl).replace('@L@', g.LOG.replace('e->', ITEM[it])).replace('@S@', g.SEND.replace('e->', ITEM[it])).replace('@F@', g.FAIL.replace('e->', ITEM[it]))
        tail = 'if (ret) {\n' + g.MFS + '\n' + g.ARMS + '}\n'
        src = g.FRAME.replace('@LOOP@', loop).replace('@TAIL@', tail)
        src = src.replace('if (prepSysex()) {', CALL[c][0]).replace('if (loadManifest(dir, ver)) {', LM[m][0]).replace('ver &= ~0xf;\n', VER[v][0])
        src = src.replace('\tint n;\n', '\tint n;\n' + CALL[c][1] + LM[m][1])
        if r == 'r1':
            src = src.replace('\tlong ret;\n', '\tlong ret = 1;\n').replace('\t\tret = 1;\n', '').replace('\t\tret = 1;\n', '')
        yield '|'.join((l, r, c, m, v, p, it)), prep(p) + src
