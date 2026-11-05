"""irwin3: detectController without pin_lo."""
FN = '_detectController'
REMOVE = [('					__asm__("" : : "a"(lo));\n', '')]
E = '__builtin_expect(!!(%s), 1)'
def W(c):
    return E % c
TESTS = {
 'n': ('for (i = 1; i < n; i++) {\n\t\t\tuint8_t *b = raw + i * 16896;', 'for (i = 1; ' + W('i < n') + '; i++) {\n\t\t\tuint8_t *b = raw + i * 16896;'),
 'skip': ('if (b[517] != 0xff || b[513] == 0xff)\n', 'if (' + W("b[517] != 0xff || b[513] == 0xff") + ')\n'),
 'a': ('if (b[517] != 0xff || b[513] == 0xff)\n', 'if (' + W("b[517] != 0xff") + ' || b[513] == 0xff)\n'),
 'b': ('if (b[517] != 0xff || b[513] == 0xff)\n', 'if (b[517] != 0xff || ' + W("b[513] == 0xff") + ')\n'),
 'first': ('if (hi + lo == i) {', 'if (' + W('hi + lo == i') + ') {'),
 'second': ('if (lo2 + (b[513] & 0xf) * 256 == i) {', 'if (' + W('lo2 + (b[513] & 0xf) * 256 == i') + ') {'),
 'r517': ('if (raw[517] == 0xff) {', 'if (' + W('raw[517] == 0xff') + ') {'),
}
