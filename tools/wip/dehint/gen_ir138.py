"""getImageSmc 2-hint form: A again: spellings of size's byte swap (term order, + or |, masks), with a0 or tm."""
import itertools
FOCUS = ['_getImageSmc']
BASE = 'tools/wip/dehint/drafts/image_read_attempt6.c'
src = open(BASE, newline='').read().replace('\r\n', '\n')
i = src.index('__attribute__((optimize("no-if-conversion", "no-if-conversion2", "no-tree-tail-merge"))) void getImageSmc')
j = src.index('void getImageKv(void)')
OLD = src[i:j]
LL = 'log_printf(1, "smc.bin should not be at 0x%x, trying 0x1000\\n", addr);\n addr = 0x1000;\n'
S38 = 'log_printf(1, "smc.bin should not be 0x%x bytes, using 0x3800\\n", size);\n'
S30 = 'log_printf(1, "smc.bin should not be 0x%x bytes, using 0x3000\\n", size);\n'
ARM = f'if (addr == 0x800) {{ size = 0x3800; {S38} }} else {{ size = 0x3000; {S30} }}'
REST = OLD[OLD.index('if (__builtin_expect(addr < 528 * xb.dumpPages, 0)) {'):]
REST = REST[:REST.index('	return;\nbad:')]
def at(*o):
    return '__attribute__((optimize(%s))) ' % ', '.join('"%s"' % x for x in o) if o else ''
TM = 'no-tree-tail-merge'
ATTRS = {'a0': at(), 'tm': at(TM)}
PIN = '__asm__("" : "+D"(addr));'
Z = f'if (!addr) {{ {LL} }}\n'
T = 'unsigned t = addr;\n if (t != 0x1000) { if (t != 0x800) goto bad; }\nbback:\n'
X = 'h->smcBootSize'
TERMS = [f'({X} << 24)', f'(({X} << 8) & 0xff0000)', f'(({X} >> 8) & 0xff00)', f'({X} >> 24)']
AX = []
tail = f'return;\nbad:\n{LL}goto bback;\n}}\n\n'
SW = {}
for p in itertools.permutations(range(4)):
    k = ''.join(map(str, p))
    SW['p' + k] = ' + '.join(TERMS[q] for q in p)
    SW['o' + k] = ' | '.join(TERMS[q] for q in p)
for k, e in SW.items():
    for kt, ta in ATTRS.items():
        AX.append((k + '.' + kt, [(OLD, ta + 'void getImageSmc(void)\n{\n struct flashhdr *h = (struct flashhdr *)xb.dump;\n int addr = SWAP32(h->smcBootAddr);\n int size = ' + e + ';\n' + Z + T + f'if (size != 0x3000 && size != 0x3800) {{ {ARM} }} else {{ {PIN} }}\n' + REST + tail)]))
AXES = [AX]
