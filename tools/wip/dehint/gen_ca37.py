"""Attempt 3: the landed shape with single parts replaced: the accessor by a named local (named SSA versions come
after gimplifier temporaries, so i + 1, a temporary, stays the first operand), the cast, `sent`, the head's tests."""
import itertools, os, re

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
T = open(os.path.join(ROOT, 'build', 'ca', 'a3', 'landed_part.c')).read()
TESTS = {
    'acc': ('static int itemsDone(int i)\n{\n\treturn i >= manifest.count;\n}\n\n', '', 'if (itemsDone(i)) {'),
    'nbody': ('', '', 'int n = manifest.count;\n\n\t\t\t\tif (i >= n) {'),
    'nfn': ('', '\tint n;\n', 'n = manifest.count;\n\t\t\t\tif (i >= n) {'),
    'nfnr': ('', '\tint n;\n', 'n = manifest.count;\n\t\t\t\tif (n <= i) {'),
    'plain': ('', '', 'if (i >= manifest.count) {'),
    'scoped': ('', '', '{ int n = manifest.count;\n\t\t\t\tif (i >= n) {'),
}
IDX = {
    'cast': ('e = &manifest.e[(size_t)i];', 'i + 1'),
    'plain': ('e = &manifest.e[i];', 'i + 1'),
    'u32': ('e = &manifest.e[(uint32_t)i];', 'i + 1'),
    'num': ('e = &manifest.e[i];\nnum = i + 1;', 'num'),
    'numb': ('num = i + 1;\ne = &manifest.e[i];', 'num'),
    'plus': ('e = manifest.e + i;', 'i + 1'),
}
SENT = {'sent': None, 'sentl': 'scoped'}


def variants():
    for t, x in itertools.product(TESTS, IDX):
        h, d, test = TESTS[t]
        ix, n = IDX[x]
        s = T
        s = s.replace('static int itemsDone(int i)\n{\n\treturn i >= manifest.count;\n}\n\n', h)
        s = s.replace('\tint i, sent;\n', '\tint i, sent;\n' + d + ('\tint num;\n' if 'num' in ix else ''))
        s = s.replace('if (itemsDone(i)) {', test)
        s = s.replace('e = &manifest.e[(size_t)i];', ix)
        s = s.replace('bytes, %s\\n", i + 1,', 'bytes, %%s\\n", %s,' % n)
        if t == 'scoped':
            s = s.replace('if (!ret)\n\t\t\t\t\tgoto out;\n\t\t\t\tgoto send_item;', '}\n\t\t\t\tif (!ret)\n\t\t\t\t\tgoto out;\n\t\t\t\tgoto send_item;')
        yield '%s|%s' % (t, x), s
