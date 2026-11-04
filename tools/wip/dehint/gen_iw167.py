# attempt 10: lnp2 gone (near8 family).  constprop.1's compare wants a low name dead at dce2, which src gets from `pages` at the inner loop's top (iftmp 54, 55), but there
# it makes writeInitialHeader's call inline: saving 10.17% against a 10% limit, only about 7 time units over.  So: one `pages` statement placed early, in several spellings, with
# something else giving up those units (pg's place), or npages taken from it.  Good: constprop.1 0 with writeInitialHeader 0.
import os
B1 = '''						pages = len / 512;
						if (len % 512)
							pages++;
'''
S1 = '				pages = len % 512 ? len / 512 + 1 : len / 512;\n'
S = {
 'q': 'pages = len % 512 ? len / 512 + 1 : len / 512;\n',
 'i': 'pages = len / 512;\nTABif (len % 512)\nTAB	pages++;\n',
 'e': 'if (len % 512)\nTAB	pages = len / 512 + 1;\nTABelse\nTAB	pages = len / 512;\n',
}
def at(sp, tabs):
    t = '\t' * tabs
    return t + S[sp].replace('TAB', t)
I0 = '''			/* a statement of its own: computed from params alone, it's what makes
			   ipa-cp's off-0 clone (imgWriteStart) worth creating; reassoc folds it
			   back into the same code */
			pg = start * 32;
'''
MS = '			memset(s, 0, 16);\n'
BLK = '		blk = start + b;\n'
FORB = '	for (b = 0; b < blocks; b++) {\n'
NP = '''			if (len % 512)
				npages = (len + 512) / 512;
			else
				npages = len / 512;
'''
PL = {
 'I0': lambda sp: [(I0, at(sp, 3) + I0)],
 'I1': lambda sp: [(MS, at(sp, 3) + MS)],
 'O0': lambda sp: [(BLK, BLK + at(sp, 2))],
 'B0': lambda sp: [(FORB, at(sp, 1) + FORB)],
 'O0n': lambda sp: [(BLK, BLK + at(sp, 2)), (NP, '			npages = pages;\n')],
 'B0n': lambda sp: [(FORB, at(sp, 1) + FORB), (NP, '			npages = pages;\n')],
}
AXES = [
 [('rm', [(B1, ''), (S1, '')])],
 [(p + s, PL[p](s)) for p in PL for s in S],
 [('', []),
  ('g1', [(I0, ''), ('(pg + p + b * 32) * 16', '(start * 32 + p + b * 32) * 16')]),
  ('g2', [(I0, ''), (BLK, BLK + '		pg = start * 32;\n')]),
  ('g3', [(I0, ''), ('		for (end = p + npages; p < end; p++) {\n', '		pg = start * 32;\n		for (end = p + npages; p < end; p++) {\n')]),
 ],
]
BASE = os.environ.get('IWB', 'tools/wip/dehint/drafts/image_write_near8.c')
FLAGS = []
FOCUS = ['_imgAdd', '_imgAdd.constprop.1', '_imgAdd.constprop.2', '_imgAdd.constprop.4', '_imgAddFile', '_writeInitialHeader']
