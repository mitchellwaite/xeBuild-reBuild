"""getImageSmc: addr and size address-taken until IPA inlines a reader helper, so scope clobbers exist at profile_estimate (the fsGetFile lever),
and they're memory for early passes (a different shape for PRE and the prologue?).  Body forms x pin x attribute (attempt 13)."""
import os
FOCUS = ['_getImageSmc']
BASE = 'tools/wip/dehint/drafts/image_read_attempt13.c'
R = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..')
src = open(os.path.join(R, BASE), newline='').read().replace('\r\n', '\n')
a = src.index('__attribute__((optimize("no-if-conversion", "no-if-conversion2", "no-tree-tail-merge"))) void getImageSmc(void)')
b = src.index('void getImageKv(void)')
OLD = src[a:b]
ATT = {'a3': '__attribute__((optimize("no-if-conversion", "no-if-conversion2", "no-tree-tail-merge"))) ', 'a0': ''}
PIN = {'p': ' else { __asm__("" : "+D"(addr)); }', 'n': ''}
READ1 = '''static void smcArea(int *addr, int *size)
{
	struct flashhdr *h = (struct flashhdr *)xb.dump;

	*addr = SWAP32(h->smcBootAddr);
	*size = SWAP32(h->smcBootSize);
}

'''
READ2 = '''static int smcArea(int *size)
{
	struct flashhdr *h = (struct flashhdr *)xb.dump;

	*size = SWAP32(h->smcBootSize);
	return SWAP32(h->smcBootAddr);
}

'''
READ3 = '''static void smcArea(int *size, int *addr)
{
	struct flashhdr *h = (struct flashhdr *)xb.dump;

	*addr = SWAP32(h->smcBootAddr);
	*size = SWAP32(h->smcBootSize);
}

'''
PRO = {
 'L': ('', 'struct flashhdr *h = (struct flashhdr *)xb.dump;\nint addr = SWAP32(h->smcBootAddr);\nint size = SWAP32(h->smcBootSize);\n'),
 'R1': (READ1, 'int addr, size;\nsmcArea(&addr, &size);\n'),
 'R2': (READ2, 'int size;\nint addr = smcArea(&size);\n'),
 'R3': (READ3, 'int addr, size;\nsmcArea(&size, &addr);\n'),
}
ZERO = 'int ok = addr != 0;\nunsigned t;\nint bad, o;\nif (ok <= 0) { log_printf(1, "smc.bin should not be at 0x%x, trying 0x1000\\n", addr); addr = 0x1000; @@ }\n'
SIZEF = 'bad = size != 0x3000 && size != 0x3800;\nif (bad > 0) { o = addr != 0x800; if (o <= 0) { size = 0x3800; log_printf(1, "smc.bin should not be 0x%%x bytes, using 0x3800\\n", size); } else { size = 0x3000; log_printf(1, "smc.bin should not be 0x%%x bytes, using 0x3000\\n", size); } }%s\n'
BAD = 'log_printf(1, "smc.bin should not be at 0x%x, trying 0x1000\\n", addr);\naddr = 0x1000;\n'
NS = 'log_printf(1, "SMC at 0x%x of size 0x%x is not sane, skipping smc.bin in NAND image\\n", addr, size);\n'


def body(k, pin):
    sz = SIZEF % pin
    if k == 'cur':
        return ZERO.replace('@@', 'ok = 1;') + 't = addr; if (t != 0x1000) { if (t != 0x800) goto badAddr; }\nfixSize:\n' + sz + 'if (ok && addr < 528 * xb.dumpPages) loadSmc(addr, size); else ' + NS + 'return;\nbadAddr:\n' + BAD + 'goto fixSize;\n'
    if k == 'plain':
        return ZERO.replace('@@', '') + 't = addr; if (t != 0x1000) { if (t != 0x800) goto badAddr; }\nfixSize:\n' + sz + 'if (addr < 528 * xb.dumpPages) loadSmc(addr, size); else ' + NS + 'return;\nbadAddr:\n' + BAD + 'goto fixSize;\n'
    if k == 's2':
        return ZERO.replace('@@', '') + 't = addr; if (t != 0x1000) { if (t != 0x800) goto badAddr; }\nfixSize:\n' + sz + '{ int out = addr >= 528 * xb.dumpPages; if (out <= 0) { loadSmc(addr, size); return; } }\n' + NS + 'goto end;\nbadAddr:\n' + BAD + 'goto fixSize;\nend: ;\n'
    if k == 's4':
        return ZERO.replace('@@', '') + 't = addr; if (t != 0x1000) { if (t != 0x800) { ' + BAD + ' } }\n' + sz + '{ int out = addr >= 528 * xb.dumpPages; if (out <= 0) { loadSmc(addr, size); return; } }\n' + NS
    if k == 's5':
        return ZERO.replace('@@', '') + 't = addr; if (t != 0x1000) { if (t != 0x800) { ' + BAD + ' } }\n' + sz + 'if (addr < 528 * xb.dumpPages) loadSmc(addr, size); else ' + NS
    raise KeyError(k)


V = {}
for at, atx in ATT.items():
    for pn, pnx in PIN.items():
        for pr, (helper, decl) in PRO.items():
            for sc in ('f', 'b'):  # function scope or one inner block (clobbers on its exits)
                for bk in ('cur', 'plain', 's2', 's4', 's5'):
                    if sc == 'b' and pr == 'L':
                        continue
                    B = decl + body(bk, pnx)
                    if sc == 'b':
                        B = '{\n' + B + '}\n'
                    V['.'.join((at, pn, pr, sc, bk))] = helper + atx + 'void getImageSmc(void)\n{\n' + B + '}\n\n'
AXES = [[(k, [(OLD, v)]) for k, v in V.items()]]
