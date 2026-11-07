import os
BASE = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..', '..', 'src', 'build.c')
T10 = ('} else if (__builtin_expect(type == 10, 0)) {', '} else if (type == 10) {')
PR = ('if (__builtin_expect(r != 0, 0))\n', 'if (r != 0)\n')
BAR = ('\t\t\t\t__asm__ __volatile__("");\n', '')
NONE = ('\tif ((uint32_t)xb.nFiles <= 1)\n\t\tgoto none;\n', '')
NONE2 = ('none: __attribute__((cold));\n\treturn 0;\n', '')
DEV = ('if (__builtin_expect(xb.type == BUILD_DEVGL || xb.type == BUILD_DEVGL16, 0))', 'if (xb.type == BUILD_DEVGL || xb.type == BUILD_DEVGL16)')
PIN = ('\t\t__asm__("" : "+b"(size));\n', '')
V = {
 'm1': [],
 't10': [T10], 'pr': [PR], 'bar': [BAR], 'none': [NONE, NONE2], 'dev': [DEV], 'pin': [PIN],
 't10pr': [T10, PR], 'prbar': [PR, BAR], 't10prbar': [T10, PR, BAR], 't10bar': [T10, BAR],
}
