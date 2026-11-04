# attempt 9: near8's constprop.1 compare.  Traced: the split-paths copy reuses ivcanon's ivtmp name, which ivcanon pops from the names released at dce2 of
# the small arm's dead `pages ?:` (iftmp.20_95, _96).  In src the same iftmp is at the top of the inner loop (iftmp.17_54, _55), below ivopts' 82.
# So the iftmp must get a name below about 82: spell or place the small arm's pages so that it's numbered before the big arm, or invert the arms' test.
import os
FLAGS = []
BASE = os.environ.get('IWB', 'tools/wip/dehint/drafts/image_write_near8.c')
FOCUS = ['_imgAdd', '_imgAdd.constprop.1', '_imgAdd.constprop.2', '_imgAdd.constprop.4', '_imgAddFile', '_writeInitialHeader']
BIGP = '						pages = len / 512;\n						if (len % 512)\n							pages++;\n'
SMP = '				pages = len % 512 ? len / 512 + 1 : len / 512;\n'
SP = {
 't': 'pages = len % 512 ? len / 512 + 1 : len / 512;\n',
 'i': 'pages = len / 512;\nif (len % 512)\n\tpages++;\n',
 'e': 'if (len % 512)\n\tpages = len / 512 + 1;\nelse\n\tpages = len / 512;\n',
}
def ind(s, n):
    return ''.join('\t' * n + l + '\n' for l in s.rstrip('\n').split('\n'))
FOR_B = '	for (b = 0; b < blocks; b++) {\n		blk = start + b;\n'
FOR_P = '		for (end = p + npages; p < end; p++) {\n'
MEMS = '			memset(s, 0, 16);\n			if (xb.bigBlock) {\n'
places = [('', [])]
# one pages for both arms, placed outside the page loop
for k, v in SP.items():
    places.append(('out' + k, [(BIGP, ''), (SMP, ''), (FOR_B, ind(v, 1) + FOR_B)]))
    places.append(('blk' + k, [(BIGP, ''), (SMP, ''), (FOR_B, FOR_B + ind(v, 2))]))
    places.append(('pre' + k, [(BIGP, ''), (SMP, ''), (FOR_P, ind(v, 2) + FOR_P)]))
# the small arm's own pages ahead of the arms, only used there
for k, v in SP.items():
    places.append(('sA' + k, [(SMP, ''), (MEMS, ind(v, 3) + MEMS)]))
    places.append(('sB' + k, [(SMP, ''), (FOR_B, FOR_B + ind(v, 2))]))
    places.append(('sO' + k, [(SMP, ''), (FOR_B, ind(v, 1) + FOR_B)]))
    places.append(('bO' + k, [(BIGP, ''), (FOR_B, ind(v, 1) + FOR_B)]))
AXES = [places]
