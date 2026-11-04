# attempt 24, pin_t: a second over-long table with its loop in a hotter block than the arm's, sized so its head passes the page loop's 10000 and rescales imgAdd's frequencies (F = 900 * 10000 / hottest). Arithmetic says t >= partial's flag at F 659 (big or small arm, n = 2), 677 (type > 1, big, n = 3), 753 (s[8], small, n = 4).
# `IWB=build/iw/a24/np.c python tools/wip/dehint/iw16sweep.py tools/wip/dehint/gen_iw305.py -n 40 -t 4`
def tab(lhs, val, n, ty='uint32_t', ind='				'):
    return ind + '{\n' + ind + '	' + ty + ' part[%d] = { %s };\n' % (n, val) + ind + '	' + ty + ' sum = 0;\n' + ind + '	int j;\n\n' + ind + '	for (j = 0; j < %d; j++)\n' % n + ind + '		sum += part[j];\n' + ind + '	' + lhs + ' = sum;\n' + ind + '}\n'
FO = [('', [])]
BIG = '				((struct spb *)s)->b2lo = (start + b) >> 8;\n'
SM = '				((struct sps *)s)->b1lo = BLK >> 8;\n'
TY = '					((struct spt *)s)->type = type;\n					if (type != 0x2a && type != 0x2c) {\n'
S8 = "						s[8] = len >> 8;\n						s[7] = len;\n					}\n				}\n			}\n		}\n"
for n in (2, 3, 4, 6):
    FO.append(('B%d' % n, [(BIG, tab('((struct spb *)s)->b2lo', '(start + b) >> 8', n))]))
    FO.append(('S%d' % n, [(SM, tab('((struct sps *)s)->b1lo', 'BLK >> 8', n))]))
for n in (3, 4, 6):
    FO.append(('T%d' % n, [(TY, tab('((struct spt *)s)->type', 'type', n, 'int', '					') + '					if (type != 0x2a && type != 0x2c) {\n')]))
for n in (4, 5, 7):
    FO.append(('U%d' % n, [(S8, tab('s[8]', 'len >> 8', n, 'uint32_t', '						') + S8[S8.index('						s[7]'):])]))
AXES = [FO]
