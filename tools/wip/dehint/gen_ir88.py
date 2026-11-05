"""getImageSmc, no hints: nested tests get opcode predictions (2 x nonequal = 52% for the size test) but VRP puts constants in the join's PHI, so ifcombine won't merge them.  Tested on another variable of the other signedness (no assert on the PHI's name), they can merge.  Axes: which variable the tests use, nested or &&, and the address the same way."""
import gen_ir80 as g
FOCUS = ['_getImageSmc']
BASE = 'src/image_read.c'
OLD, TAIL, NS, BAD, S800, S000 = g.OLD, g.TAIL, g.NS, g.BAD, g.S800, g.S000
AD = {
    'a.i': ('int addr = SWAP32(h->smcBootAddr);\n', 'addr'),
    'a.u': ('uint32_t a = SWAP32(h->smcBootAddr);\n	int addr = a;\n', 'a'),
    'a.i2': ('int a = SWAP32(h->smcBootAddr);\n	uint32_t addr = a;\n', 'a'),
    'a.uu': ('uint32_t addr = SWAP32(h->smcBootAddr);\n', 'addr'),
}
SD = {
    's.i': ('int size = SWAP32(h->smcBootSize);\n', 'size'),
    's.u': ('uint32_t s = SWAP32(h->smcBootSize);\n	int size = s;\n', 's'),
    's.i2': ('int s = SWAP32(h->smcBootSize);\n	uint32_t size = s;\n', 's'),
}
def TA(v):
    return {'an': (f'if ({v} != 0x800 && {v} != 0x1000) {{\n', '}\n'),
            'nn': (f'if ({v} != 0x800) {{\nif ({v} != 0x1000) {{\n', '}\n}\n')}
def TS(v):
    return {'an': (f'if ({v} != 0x3000 && {v} != 0x3800) {{\n', '}\n'),
            'nn': (f'if ({v} != 0x3000) {{\nif ({v} != 0x3800) {{\n', '}\n}\n')}
L = {'lt': f'if (addr < 528 * xb.dumpPages) {{\n{TAIL}}} else {{\n{NS}}}\n',
     'ge': f'if (addr >= 528 * xb.dumpPages) {{\n{NS}}} else {{\n{TAIL}}}\n'}
Z = {'zv': lambda v: f'if (!{v}) {{\n{BAD}}}\n', 'zad': lambda v: f'if (!addr) {{\n{BAD}}}\n'}
AX = []
for ak, (ad, av) in AD.items():
    for sk, (sd, sv) in SD.items():
        for tak, (ta0, ta1) in TA(av).items():
            for tsk, (ts0, ts1) in TS(sv).items():
                for lk, l in L.items():
                    for zk, z in Z.items():
                        if zk == 'zad' and av == 'addr':
                            continue
                        body = ('void getImageSmc(void)\n{\n	struct flashhdr *h = (struct flashhdr *)xb.dump;\n	' + ad + '	' + sd + '\n	' +
                                z(av) + ta0 + BAD + ta1 + ts0 + f'if (addr == 0x800) {{\n{S800}}} else {{\n{S000}}}\n' + ts1 + l + '}\n')
                        AX.append(('+'.join((ak, sk, tak, tsk, lk, zk)), [(OLD, body)]))
AXES = [AX]
