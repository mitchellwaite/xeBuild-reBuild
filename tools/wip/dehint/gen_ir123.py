"""getImageSmc on gen_ir118 t6.and.k3.ex: addr's partition must number below a's, as in the hinted source (cse canonicalises to the lower pseudo, so
the bad arm's log uses addr's pseudo and find_moveable_pseudos leaves its def in T).  Partition numbers follow the root's SSA version: addr needs a PHI at the final
join from into-SSA, that is, an assignment to addr in the size test's arms."""
FOCUS = ['_getImageSmc']
BASE = 'tools/wip/dehint/drafts/image_read_attempt6.c'
src = open(BASE, newline='').read().replace('\r\n', '\n')
i = src.index('__attribute__((optimize("no-if-conversion", "no-if-conversion2", "no-tree-tail-merge"))) void getImageSmc')
j = src.index('void getImageKv(void)')
OLD = src[i:j]
L = 'log_printf(1, "smc.bin should not be at 0x%x, trying 0x1000\\n", addr);\n addr = 0x1000;\n'
Z = f'if (!addr) {{ {L} }}\n'
S3800 = 'log_printf(1, "smc.bin should not be 0x%x bytes, using 0x3800\\n", size);\n'
S3000 = 'log_printf(1, "smc.bin should not be 0x%x bytes, using 0x3000\\n", size);\n'
REST = OLD[OLD.index('if (__builtin_expect(addr < 528 * xb.dumpPages, 0)) {'):]
REST = REST[:REST.index('	return;\nbad:')] + '}\n\n'
def rest(ex, v):
    r = REST.replace('xb.dump + addr', 'xb.dump + ' + v)
    c = v + ' < 528 * xb.dumpPages'
    return r.replace('__builtin_expect(addr < 528 * xb.dumpPages, 0)', ('__builtin_expect(%s, 0)' % c) if ex else c)
H = '''void getImageSmc(void)
{
	struct flashhdr *h = (struct flashhdr *)xb.dump;
	int addr = SWAP32(h->smcBootAddr);
	int size = SWAP32(h->smcBootSize);
	uint32_t a;

'''
HT = H.replace('uint32_t a;', 'uint32_t a;\n\tunsigned t;')
AA = Z + f'unsigned t = addr;\n if (t != 0x1000) {{ if (t != 0x800) {{ {L} }} }}\n'
ARM = f'if (addr == 0x800) {{ size = 0x3800; {S3800} }} else {{ size = 0x3000; {S3000} }}'
ARMA = f'if (a == 0x800) {{ size = 0x3800; {S3800} }} else {{ size = 0x3000; {S3000} }}'
T = 'if (size != 0x3000 && size != 0x3800) {%s} else {%s}\n'
SZ = {
    'e1': T % (ARM + ' a = addr;', 'a = addr; addr = a;'),
    'e2': T % (ARM + ' a = addr; addr = a;', 'a = addr;'),
    'e3': T % (ARM + ' a = addr; addr = a;', 'a = addr; addr = a;'),
    'e4': 'a = addr;\n' + T % (ARMA, 'addr = a;'),
    'e5': 'a = addr;\n' + T % (ARMA + ' addr = a;', 'addr = a;'),
    'e6': T % (ARM + ' a = addr;', 'addr = a = addr;'),
    'e7': T % ('a = addr; ' + ARMA, 'addr = a = addr;'),
    'e8': T % ('a = addr; ' + ARMA, 'a = addr; addr = a;'),
    'e9': T % ('a = addr; ' + ARMA + ' addr = a;', 'a = addr; addr = a;'),
    'f1': T % (ARM + ' a = addr;', 'a = addr; addr = (int)a;'),
    'f2': 'a = addr;\n' + T % (ARMA, 'addr = (int)a;'),
    'g1': T % (ARM.replace('size = 0x3800;', 'size = 0x3800; addr = 0x800;') + ' a = addr;', 'a = addr;'),
    'g2': T % (ARM.replace(S3800, S3800 + 'addr = 0x800;') + ' a = addr;', 'a = addr;'),
    'g4': T % ('a = addr; ' + ARMA.replace('size = 0x3800;', 'size = 0x3800; addr = 0x800;'), 'a = addr;'),
    'g5': T % (ARM.replace('size = 0x3800;', 'addr = a = 0x800; size = 0x3800;').replace('size = 0x3000;', 'a = addr; size = 0x3000;'), 'a = addr;'),
    'g6': T % (ARM.replace('size = 0x3800;', 'a = addr = 0x800; size = 0x3800;').replace(S3000, S3000 + ' a = addr;'), 'a = addr;'),
    'g7': T % (ARM.replace('size = 0x3800;', 'addr = 0x800; size = 0x3800;').replace('size = 0x3000;', 'addr = 0x1000 * (addr == 0x1000) + addr * (addr != 0x1000); size = 0x3000;') + ' a = addr;', 'a = addr;'),
}
AX = []
for ks, s in SZ.items():
    for kr, v in (('a', 'a'), ('u', '(uint32_t)addr')):
        for ex in (1, 0):
            AX.append(('.'.join((ks, kr, 'ex' if ex else 'e0')), [(OLD, H + AA + s + rest(ex, v))]))
AXES = [AX]
