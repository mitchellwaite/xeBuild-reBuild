# imgAdd: the (int) casts, on top of `if (len & 511)`
I6 = '\t\t\t\t\t\t'
SH = I6 + 'pages = len >> 9;\n' + I6 + 'if (len % 512)\n'
SHA = I6 + 'pages = len >> 9;\n' + I6 + 'if (len & 511)\n'
C = I6 + 'if ((int)pages & 3)\n' + I6 + '\tpages = ((int)pages + 4) & ~3;\n'
S9 = I6 + 's[9] = (left - pages) >> 2;\n'
D = '\tuint32_t x, first, rem, tail, blocks, start, p, end, npages, pages;\n'
B = [(SH, SHA)]


def c(t, s9=None):
    r = B + [(C, t)]
    if s9:
        r.append((S9, s9))
    return r


V = [
    ('base', B),
    ('r', c(I6 + '{\n' + I6 + '\tint r = pages & 3;\n\n' + I6 + '\tif (r)\n' + I6 + '\t\tpages = (pages + 4) & ~3;\n' + I6 + '}\n')),
    ('ci', c(I6 + 'if (pages & 3)\n' + I6 + '\tpages = (int)(pages + 4) & ~3;\n')),
    ('cond', c(I6 + 'pages = (pages & 3) ? (pages + 4) & ~3 : pages;\n')),
    ('condi', c(I6 + 'pages = ((int)pages & 3) ? ((int)pages + 4) & ~3 : pages;\n')),
    ('add', c(I6 + 'if (pages & 3)\n' + I6 + '\tpages += 4 - (pages & 3);\n')),
    ('addi', c(I6 + 'if (pages % 4)\n' + I6 + '\tpages += 4 - pages % 4;\n')),
    ('s9i', c(I6 + 'if (pages & 3)\n' + I6 + '\tpages = (pages + 4) & ~3;\n', I6 + 's[9] = (left - (int)pages) >> 2;\n')),
    ('lp', c(I6 + 'if (pages & 3)\n' + I6 + '\tpages = (pages + 4) & ~3;\n', I6 + 'left -= pages;\n' + I6 + 's[9] = left >> 2;\n')),
    ('np', c(I6 + 'if (pages & 3)\n' + I6 + '\tpages = (pages + 4) & ~3;\n', I6 + 's[9] = (left - (int)pages) / 4;\n')),
    ('u3', c(I6 + 'if (pages & 3)\n' + I6 + '\tpages = (pages + 4) & ~3u;\n')),
    ('m4', c(I6 + 'if (pages & 3)\n' + I6 + '\tpages = (pages + 4) & -4;\n')),
    ('ip', [(SH + I6 + '\tpages++;\n', I6 + '{\n' + I6 + '\tint n = len >> 9;\n\n' + I6 + '\tif (len & 511)\n' + I6 + '\t\tn++;\n' + I6 + '\tif (n & 3)\n' + I6 + '\t\tn = (n + 4) & ~3;\n' + I6 + '\tpages = n;\n' + I6 + '}\n'), (C, '')]),
]
