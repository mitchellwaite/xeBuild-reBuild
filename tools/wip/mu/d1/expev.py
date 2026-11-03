"""expev.py DUMP OUT: event file for fast.c"""
import sys, dsim
M = dsim.load(sys.argv[1])


def wr(f, e):
    if e[0] == 'round':
        f.write('0 %d 0 0\n' % e[1])
    elif e[0] == 'get':
        f.write('1 %d 0 0\n' % e[1])
    elif e[0] == 'visit':
        f.write('2 %d 0 0\n' % e[1])
    elif e[0] == 'ins':
        f.write('3 %d %d %d\n' % (e[2], e[1] == 'this', e[3]))
    elif e[0] == 'push':
        f.write('4 %d 0 %d\n' % (e[1], e[2]))
    elif e[0] == 'chg':
        f.write('5 %d 0 %d\n' % (e[1], e[2]))


with open(sys.argv[2], 'w', newline='\n') as f:
    f.write('W ' + ' '.join(map(str, dsim.WANT)) + ' -1\nF ' + ' '.join(map(str, dsim.FLEX)) + ' -1\nPRE\n')
    for e in M['pre']:
        wr(f, e)
    for b, g in M['g3'].items():
        f.write('G3 %d\n' % b)
        for e in g:
            wr(f, e)
    for b, g in M['g4'].items():
        f.write('G4 %d\n' % b)
        for e in g:
            wr(f, e)
