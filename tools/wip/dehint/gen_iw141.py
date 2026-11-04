# attempt 8: from n7: pages' spelling and place in each arm.  In the type-0 clones the arms' pages is dead, so its statements only move the free list until DCE.
import os
FLAGS = []
BASE = os.environ.get('IWB', 'build/iw/a8/n7.c')
FOCUS = ['_imgAdd', '_imgAdd.constprop.1', '_imgAdd.constprop.2', '_imgAdd.constprop.4', '_imgAddFile', '_writeInitialHeader']
B0 = '						pages = len % 512 ? len / 512 + 1 : len / 512;\n						left = pages;\n'
S0 = '			} else {\n				pages = len % 512 ? len / 512 + 1 : len / 512;\n				((struct sps *)s)->b1lo = BLK >> 8;\n				((struct sps *)s)->b5 = 0xff;\n				s[0] = BLK;\n'
Q = '						'
SPELL = {
 't': 'pages = len % 512 ? len / 512 + 1 : len / 512;\n',
 'i': 'pages = len / 512;\nif (len % 512)\n\tpages++;\n',
 'e': 'if (len % 512)\n\tpages = len / 512 + 1;\nelse\n\tpages = len / 512;\n',
 'a': 'pages = len / 512 + (len % 512 != 0);\n',
 'r': 'pages = (len + 511) / 512;\n',
 'x': 'if (len % 512)\n\tpages = (len + 512) / 512;\nelse\n\tpages = len / 512;\n',
}


def ind(s, n):
    return ''.join('\t' * n + l + '\n' for l in s.rstrip('\n').split('\n'))


BF = [('B' + k, [(B0, ind(v, 6) + '						left = pages;\n')]) for k, v in SPELL.items()]
ST = '				((struct sps *)s)->b1lo = BLK >> 8;\n				((struct sps *)s)->b5 = 0xff;\n				s[0] = BLK;\n'
SF = []
for k, v in SPELL.items():
    SF.append(('S' + k, [(S0, '			} else {\n' + ind(v, 4) + ST)]))
    SF.append(('Z' + k, [(S0, '			} else {\n' + ST + ind(v, 4))]))
AXES = [BF, SF]
