# attempt 10: lnp2 gone.  gen_iw167 rm+I0q (build/iw/a10/l1.c): `pages` at the top of the inner loop, imgAdd and every clone right, no hot label.  What's left is writeInitialHeader's
# off-0 call inlining: saved 368 of 3574.5 (`-fdump-ipa-inline-details`, 10.3%, limit 10%).  So take about 21 time units (callee scale) out of (op2 changed): fewer inner-loop statements on len.
import os
B = os.environ.get('IWB', 'build/iw/a10/l1.c')
Q = '			pages = len % 512 ? len / 512 + 1 : len / 512;\n'
BLK = '		blk = start + b;\n'
FORB = '	for (b = 0; b < blocks; b++) {\n'
NP = '''			if (len % 512)
				npages = (len + 512) / 512;
			else
				npages = len / 512;
'''
DECL = '	uint32_t pg;\n'
F = {
 'f1': [(Q, '			pages = len / 512 + (len % 512 != 0);\n')],
 'f2': [(Q, '			pages = len / 512 + !!(len % 512);\n')],
 'f3': [(Q, '			pages = len / 512;\n			pages += len % 512 ? 1 : 0;\n')],
 'f4': [(Q, '			pages = (len % 512 ? 1 : 0) + len / 512;\n')],
 'f5': [(Q, '			pages = len % 512 ? (len + 512) / 512 : len / 512;\n')],
 'f6': [(Q, '			pages = len / 512;\n			pages = len % 512 ? pages + 1 : pages;\n')],
 # rem, quot as locals outside the inner loop
 'r1': [(DECL, DECL + '	uint32_t rem512;\n'), (Q, '			pages = rem512 ? len / 512 + 1 : len / 512;\n'), (BLK, BLK + '		rem512 = len % 512;\n')],
 'r2': [(DECL, DECL + '	uint32_t rem512;\n'), (Q, '			pages = rem512 ? len / 512 + 1 : len / 512;\n'), (FORB, '	rem512 = len % 512;\n' + FORB)],
 'r3': [(DECL, DECL + '	uint32_t quot;\n'), (Q, '			pages = len % 512 ? quot + 1 : quot;\n'), (BLK, BLK + '		quot = len / 512;\n')],
 'r4': [(DECL, DECL + '	uint32_t quot;\n'), (Q, '			pages = len % 512 ? quot + 1 : quot;\n'), (FORB, '	quot = len / 512;\n' + FORB)],
 'r5': [(DECL, DECL + '	uint32_t quot, rem512;\n'), (Q, '			pages = rem512 ? quot + 1 : quot;\n'), (BLK, BLK + '		quot = len / 512;\n		rem512 = len % 512;\n')],
 'r6': [(DECL, DECL + '	uint32_t quot, rem512;\n'), (Q, '			pages = rem512 ? quot + 1 : quot;\n'), (FORB, '	quot = len / 512;\n	rem512 = len % 512;\n' + FORB)],
 'r7': [(DECL, DECL + '	uint32_t rem512;\n'), (Q, '			pages = rem512 ? len / 512 + 1 : len / 512;\n'), (BLK, BLK + '		rem512 = len % 512;\n'), (NP, '			if (rem512)\n				npages = (len + 512) / 512;\n			else\n				npages = len / 512;\n')],
 'r8': [(DECL, DECL + '	uint32_t rem512;\n'), (Q, '			pages = rem512 ? len / 512 + 1 : len / 512;\n'), (FORB, '	rem512 = len % 512;\n' + FORB), (NP, '			if (rem512)\n				npages = (len + 512) / 512;\n			else\n				npages = len / 512;\n')],
 'r9': [(DECL, DECL + '	uint32_t quot, rem512;\n'), (Q, '			pages = rem512 ? quot + 1 : quot;\n'), (FORB, '	quot = len / 512;\n	rem512 = len % 512;\n' + FORB), (NP, '			npages = rem512 ? quot + 1 : quot;\n')],
}
AXES = [
 [('', [])] + [(k, v) for k, v in F.items()],
]
BASE = B
FLAGS = []
FOCUS = ['_imgAdd', '_imgAdd.constprop.1', '_imgAdd.constprop.2', '_imgAdd.constprop.4', '_imgAddFile', '_writeInitialHeader']
