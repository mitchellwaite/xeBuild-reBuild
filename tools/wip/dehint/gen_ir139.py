"""getImageSmc: no expect: the sane block must land at 18-22% of entry (exp_smc at 78-82 gives only `mov edi,ebx` left): outer test that VRP folds (64% if > 0, 50 otherwise) x call in the sane arm's first block (29%, the log's block has two predecessors).  Pin kept, attribute options."""
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
R0 = OLD[OLD.index('if (__builtin_expect(addr < 528 * xb.dumpPages, 0)) {'):]
R0 = R0[:R0.index('	return;\nbad:')]
SANE = R0[R0.index('{') + 1:R0.index('} else {\n\t\tlog_printf(1, "SMC at')]
NS = 'log_printf(1, "SMC at 0x%x of size 0x%x is not sane, skipping smc.bin in NAND image\\n", addr, size);\n'
def at(*o):
    return '__attribute__((optimize(%s))) ' % ', '.join('"%s"' % x for x in o) if o else ''
I2, TM = 'no-if-conversion2', 'no-tree-tail-merge'
ATTRS = {'a0': at(), 'tm': at(TM), 'tmi': at(TM, I2)}
PIN = '__asm__("" : "+D"(addr));'
Z = f'if (!addr) {{ {LL} }}\n'
T = 'unsigned t = addr;\n if (t != 0x1000) { if (t != 0x800) goto bad; }\nbback:\n'
C = 'addr < 528 * xb.dumpPages'
OUT = {'gt': 'addr > 0', 'ge': 'addr >= 0', 'ne': 'addr', 'sgt': 'size > 0', 'sne': 'size', 'sge': 'size >= 0', 'ng': 'addr != -1', 'le': 'addr <= 0x1000', 'ms': 'addr >= 0x800'}
AX = []
tail = f'return;\nbad:\n{LL}goto bback;\n}}\n\n'
for ko, o in OUT.items():
    for kf, f in (('gd', f'if ({o}) {{ if ({C}) {{ {SANE} goto done; }} }}\n {NS} done:;\n'),
                  ('rt', f'if ({o}) {{ if ({C}) {{ {SANE} return; }} }}\n {NS}'),
                  ('rv', f'if ({o}) {{ if ({C}) {{ {SANE} }} else goto ns; }} else {{ ns: {NS} }}\n')):
        for kt, ta in ATTRS.items():
            AX.append(('.'.join((ko, kf, kt)), [(OLD, ta + 'void getImageSmc(void)\n{\n struct flashhdr *h = (struct flashhdr *)xb.dump;\n int addr = SWAP32(h->smcBootAddr);\n int size = SWAP32(h->smcBootSize);\n' + Z + T + f'if (size != 0x3000 && size != 0x3800) {{ {ARM} }} else {{ {PIN} }}\n' + f + tail)]))
AXES = [AX]
