# attempt 9: near8's constprop.1 compare.  Position x spelling of pages per arm, cross product (gen_iw138 only had one spelling, gen_iw141 only one position).
# A `pages` at an arm's top survives ccp2 in the type-0 clones and dies at dce2, so its names are what unswitch and ivcanon pop; inside `type > 1` it's gone at ccp2.
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
BTOP = '				((struct spb *)s)->b2lo = blk >> 8;\n'
BT1 = '''				s[1] = BLK;
				if (type > 1) {
					s[12] = (s[12] & 0xc0) | (type & 0x3f);
					if (type != 0x2a && type != 0x2c) {
'''
BT0 = '''				s[1] = BLK;
				if (type > 1) {
'''
ST1 = '''				s[0] = BLK;
				if (type > 1) {
'''
STOP = '				((struct sps *)s)->b1lo = BLK >> 8;\n'
big = []
small = []
for k, v in SP.items():
    big.append(('Bin' + k, [(BIGP, ind(v, 6))]))
    big.append(('Btop' + k, [(BIGP, ''), (BTOP, ind(v, 4) + BTOP)]))
    big.append(('Bt1' + k, [(BIGP, ''), (BT0, BT0 + ind(v, 5))]))
    small.append(('Stop' + k, [(SMP, ''), (STOP, ind(v, 4) + STOP)]))
    small.append(('St1' + k, [(SMP, ''), (ST1, ST1 + ind(v, 5))]))
    small.append(('Sz' + k, [(SMP, ''), ('					s[9] = 32 - pages;\n', ind(v, 5) + '					s[9] = 32 - pages;\n')]))
AXES = [big, small]
