# attempt 10: lnp2 gone, on build/iw/a10/l1.c (pages at the inner loop's top).  Stop writeInitialHeader's inline by moving len's other statements out of the block loop:
# partial, npages computed once ahead of it, which is also just the natural place.  Compare with near8: imgAddFile and writeFsTable are the rest.
import os
PA = "		partial = (len < 0x4000) & (type != 0) & (type != '0');\n"
TT = "		t = type - '1';\n"
NP = '''		if (partial > 0) {
			if (len % 512)
				npages = (len + 512) / 512;
			else
				npages = len / 512;
		} else
			npages = 32;
'''
FORB = '	for (b = 0; b < blocks; b++) {\n'
OUT = {
 '': [],
 'P': [(PA, ''), (FORB, PA[1:] + FORB)],
 'N': [(NP, ''), (PA + TT, TT), (FORB, PA[1:] + ''.join(l[1:] + '\n' for l in NP.split('\n')[:-1]) + FORB)],
 'T': [(TT, ''), (FORB, TT[1:] + FORB)],
 'PT': [(PA + TT, ''), (FORB, PA[1:] + TT[1:] + FORB)],
 'NT': [(NP, ''), (PA + TT, ''), (FORB, PA[1:] + TT[1:] + ''.join(l[1:] + '\n' for l in NP.split('\n')[:-1]) + FORB)],
}
NF = {
 '': [],
 'n1': [('			if (len % 512)\n				npages = (len + 512) / 512;\n			else\n				npages = len / 512;\n', '			npages = len % 512 ? (len + 512) / 512 : len / 512;\n')],
 'n2': [('			if (len % 512)\n				npages = (len + 512) / 512;\n			else\n				npages = len / 512;\n', '			npages = len / 512;\n			if (len % 512)\n				npages++;\n')],
 'n3': [('			if (len % 512)\n				npages = (len + 512) / 512;\n			else\n				npages = len / 512;\n', '			npages = len % 512 ? len / 512 + 1 : len / 512;\n')],
}
AXES = [
 [(k, v) for k, v in NF.items()],
 [(k, v) for k, v in OUT.items()],
]
BASE = os.environ.get('IWB', 'build/iw/a10/l1.c')
FLAGS = []
