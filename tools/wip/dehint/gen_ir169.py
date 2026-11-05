"""getImageSmc from attempt 10's draft: an `ok` flag on the zero test (73 + call: P(zero) 13) that also feeds the sane test, in place of both dead tests (h, t).  Left at first: `cmp eax,ebx` operand order (names)."""
FOCUS = ['_getImageSmc']
BASE = 'tools/wip/dehint/drafts/image_read_attempt10.c'
src = open(BASE, newline='').read().replace('\r\n', '\n')
A3 = '__attribute__((optimize("no-if-conversion", "no-if-conversion2", "no-tree-tail-merge"))) void getImageSmc(void)'
i = src.index(A3)
j = src.index('void getImageKv(void)')
OLD = src[i:j]
LOG = 'log_printf(1, "smc.bin should not be at 0x%x, trying 0x1000\\n", addr);\n addr = 0x1000;\n'
k = OLD.index('if (h) {')
e = OLD.index('unsigned t = addr;')
Z0 = OLD[k:e]
LIM = 'addr < 528 * xb.dumpPages'
X0 = f'if (t && {LIM})'
assert X0 in OLD
HEAD_OLD = 'int size = SWAP32(h->smcBootSize);\n'
assert HEAD_OLD in OLD
Z = {
 'le1': ('', f'int ok = addr != 0; if (ok <= 0) {{ {LOG} ok = 1; }}\n'),
 'le2': ('int ok;\n', f'ok = addr != 0; if (ok <= 0) {{ {LOG} ok = 1; }}\n'),
 'le3': ('int ok = addr != 0;\n', f'if (ok <= 0) {{ {LOG} ok = 1; }}\n'),
 'lt': ('', f'int ok = addr != 0; if (ok < 1) {{ {LOG} ok = 1; }}\n'),
 'gt': ('', f'int ok = addr != 0; if (ok > 0) {{ }} else {{ {LOG} ok = 1; }}\n'),
 'ld': ('', f'int ok = addr != 0; if (ok <= 0) {{ {LOG} ok = addr; }}\n'),
 'lf': ('', f'int ok = addr != 0; if (ok <= 0) {{ {LOG} ok = addr != 0; }}\n'),
}
X = {
 'x1': f'if (ok && {LIM})',
 'x2': f'if (ok != 0 && {LIM})',
 'x3': f'if ({LIM} && ok)',
 'x4': f'if (ok > 0 && {LIM})',
 'x5': f'if (ok && (unsigned)addr < 528 * xb.dumpPages)',
 'x6': f'if (ok && t < 528 * xb.dumpPages)',
 'x7': f'if (ok && 528 * xb.dumpPages > addr)',
}
def at(*o):
    return '__attribute__((optimize(%s))) ' % ', '.join('"%s"' % x for x in o) if o else ''
I1, I2, TM = 'no-if-conversion', 'no-if-conversion2', 'no-tree-tail-merge'
ATTRS = {'a0': at(), 'a3': at(I1, I2, TM)}
AX = []
for kz, (h, z) in Z.items():
    for kx, x in X.items():
        for kq, q in ATTRS.items():
            AX.append(('.'.join((kz, kx, kq)), [(OLD, q + OLD.replace(A3, 'void getImageSmc(void)').replace(HEAD_OLD, HEAD_OLD + h).replace(Z0, z).replace(X0, x))]))
AXES = [AX]
