"""getImageSmc, no hints: at profile_estimate `a != x && a != y` on a local is one test (`_1 & _2`, gimplify), so no opcode prediction: P(size bad) 50%, P(bad addr) 29%.  On the header field itself (a load) the && stays two tests until FRE: 2 x nonequal = 52%, inside bb-reorder's and ce3's window for the size test.  Axes: which tests read the field."""
import gen_ir80 as g
FOCUS = ['_getImageSmc']
BASE = 'src/image_read.c'
OLD, TAIL, NS, BAD, S800, S000 = g.OLD, g.TAIL, g.NS, g.BAD, g.S800, g.S000
AM = 'SWAP32(h->smcBootAddr)'
SM = 'SWAP32(h->smcBootSize)'
Z = {'zv': '!addr', 'zm': '!' + AM, 'zr': '!h->smcBootAddr'}
A = {'av': 'addr != 0x800 && addr != 0x1000',
     'am': f'{AM} != 0x800 && {AM} != 0x1000',
     'am2': f'addr != 0x800 && {AM} != 0x1000',
     }
S = {'sv': 'size != 0x3000 && size != 0x3800',
     'sm': f'{SM} != 0x3000 && {SM} != 0x3800',
     'sm2': f'size != 0x3000 && {SM} != 0x3800',
     }
CH = {'c': lambda z, a: f'if ({z}) {{\n{BAD}}}\nif ({a}) {{\n{BAD}}}\n',
      'e': lambda z, a: f'if ({z}) {{\n{BAD}}} else if ({a}) {{\n{BAD}}}\n',
      }
L = {'lt': f'if (addr < 528 * xb.dumpPages) {{\n{TAIL}}} else {{\n{NS}}}\n',
     'ge': f'if (addr >= 528 * xb.dumpPages) {{\n{NS}}} else {{\n{TAIL}}}\n',
     }
D = {'ii': g.D['ii'], 'uu': g.D['uu']}
AX = []
for dk, d in D.items():
    for zk, z in Z.items():
        for ak, a in A.items():
            for sk, s in S.items():
                for ck, c in CH.items():
                    for lk, l in L.items():
                        b = f'if ({s}) {{\nif (addr == 0x800) {{\n{S800}}} else {{\n{S000}}}\n}}\n'
                        body = 'void getImageSmc(void)\n{\n	struct flashhdr *h = (struct flashhdr *)xb.dump;\n	' + d + '\n	' + c(z, a) + b + l + '}\n'
                        AX.append(('.'.join((dk, zk, ak, sk, ck, lk)), [(OLD, body)]))
AXES = [AX]
