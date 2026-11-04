# attempt 9: near8's constprop.1 compare.  dce2 releases its dead statements backwards, so the lowest name dead at dce2 is on top of the free list and is what
# unswitch and ivcanon pop.  near8's only dead-at-dce2 statements are the small arm's pages (95..), src's are pages at the loop's top (53..): a statement that
# survives ccp2 in the type-0 clones with a low name (used only under `type > 1`, computed from len) should do it.  Named `len >> 8` and `(uint8_t)len` before the arms.
import os
FLAGS = []
BASE = os.environ.get('IWB', 'tools/wip/dehint/drafts/image_write_near8.c')
FOCUS = ['_imgAdd', '_imgAdd.constprop.1', '_imgAdd.constprop.2', '_imgAdd.constprop.4', '_imgAddFile', '_writeInitialHeader']
USEB = '						s[8] = len >> 8;\n						s[7] = len;\n'
USES = '						s[8] = len >> 8;\n						s[7] = len;\n'
FOR_B = '	for (b = 0; b < blocks; b++) {\n		blk = start + b;\n'
FOR_P = '		for (end = p + npages; p < end; p++) {\n'
MEMS = '			memset(s, 0, 16);\n			if (xb.bigBlock) {\n'
DECL = '	uint32_t b, blk;\n'
places = {'bT': (FOR_B, FOR_B + '%s'), 'bF': (FOR_B, '%s' + FOR_B), 'pP': (FOR_P, '%s' + FOR_P), 'iT': (FOR_P, FOR_P + '%s'), 'iM': (MEMS, '%s' + MEMS)}
ind = {'bT': '\t\t', 'bF': '\t', 'pP': '\t\t', 'iT': '\t\t\t', 'iM': '\t\t\t'}
hi = [('', [])]
for k, (a, b) in places.items():
    hi.append(('hi' + k, [(DECL, DECL + '	uint32_t hi;\n'), (a, b % (ind[k] + 'hi = len >> 8;\n')), (USEB, USEB.replace('len >> 8', 'hi'))]))
    hi.append(('h8' + k, [(DECL, DECL + '	uint8_t hi;\n'), (a, b % (ind[k] + 'hi = len >> 8;\n')), (USEB, USEB.replace('len >> 8', 'hi'))]))
    hi.append(('q' + k, [(DECL, DECL + '	uint32_t pg0;\n'), (a, b % (ind[k] + 'pg0 = len / 512;\n')), ('						pages = len / 512;\n', '						pages = pg0;\n')]))
AXES = [hi]
