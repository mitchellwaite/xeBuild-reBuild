"""getImageSmc, no hints: size nested on `int s` (52%, merges).  Bad address: with no call in the arm's first block its test isn't call-predicted.  Dead or live first statements in the arm, zero test forms, last test."""
import gen_ir80 as g
FOCUS = ['_getImageSmc']
BASE = 'src/image_read.c'
OLD, TAIL, NS, BAD, S800, S000 = g.OLD, g.TAIL, g.NS, g.BAD, g.S800, g.S000
ARM = {
    'plain': BAD,
    'dz': 'if (addr)\n' + 'log_printf(1, "smc.bin should not be at 0x%x, trying 0x1000\\n", addr);\n		addr = 0x1000;\n',
    'dz2': 'if (addr) {\n' + BAD + '}\n',
}
TA = {
    'an': lambda arm: f'if (addr != 0x800 && addr != 0x1000) {{\n{arm}}}\n',
    'nn': lambda arm: f'if (addr != 0x800) {{\nif (addr != 0x1000) {{\n{arm}}}\n}}\n',
}
DA = {
    'a.i': 'int addr = SWAP32(h->smcBootAddr);\n',
    'a.2': 'int a = SWAP32(h->smcBootAddr);\n	uint32_t addr = a;\n',
    'a.3': 'uint32_t a = SWAP32(h->smcBootAddr);\n	int addr = a;\n',
}
DS = {
    's.2': 'int s = SWAP32(h->smcBootSize);\n	uint32_t size = s;\n',
    's.3': 'uint32_t s = SWAP32(h->smcBootSize);\n	int size = s;\n',
}
Z = {'zs': lambda rest: f'if (!addr) {{\n{BAD}}}\n{rest}', 'ze': lambda rest: f'if (!addr) {{\n{BAD}}} else {{\n{rest}}}\n'}
TS = 'if (s != 0x3000) {\nif (s != 0x3800) {\n' + f'if (addr == 0x800) {{\n{S800}}} else {{\n{S000}}}\n' + '}\n}\n'
L = {'lt': f'if (addr < 528 * xb.dumpPages) {{\n{TAIL}}} else {{\n{NS}}}\n',
     'ge': f'if (addr >= 528 * xb.dumpPages) {{\n{NS}}} else {{\n{TAIL}}}\n'}
AX = []
for ak, ad in DA.items():
    for sk, sd in DS.items():
        for tk, t in TA.items():
            for rk, r in ARM.items():
                for zk, z in Z.items():
                    for lk, l in L.items():
                        vv = t(r)
                        if ak != 'a.i':
                            vv = vv.replace('addr != 0x800', 'a != 0x800').replace('addr != 0x1000', 'a != 0x1000')
                        body = ('void getImageSmc(void)\n{\n	struct flashhdr *h = (struct flashhdr *)xb.dump;\n	' + ad + '	' + sd + '\n	' +
                                z(vv) + TS + l + '}\n')
                        AX.append(('+'.join((ak, sk, tk, rk, zk, lk)), [(OLD, body)]))
AXES = [AX]
