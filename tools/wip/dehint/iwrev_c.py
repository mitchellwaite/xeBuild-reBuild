# imgAdd: `(int)pages` casts and `len >> 9` next to `len % 512`
I6 = '\t\t\t\t\t\t'
SH = I6 + 'pages = len >> 9;\n'
C = I6 + 'if ((int)pages & 3)\n' + I6 + '\tpages = ((int)pages + 4) & ~3;\n'
S9 = I6 + 's[9] = (left - pages) >> 2;\n'
D = '\tuint32_t x, first, rem, tail, blocks, start, p, end, npages, pages;\n'
SM = '\t\t\t\tpages = len % 512 ? len / 512 + 1 : len / 512;\n'
NC = I6 + 'if (pages & 3)\n' + I6 + '\tpages = (pages + 4) & ~3;\n'
V = [
    ('base', []),
    ('nocast', [(C, NC)]),
    ('div', [(SH, I6 + 'pages = len / 512;\n')]),
    ('both', [(C, NC), (SH, I6 + 'pages = len / 512;\n')]),
    ('cast1', [(C, I6 + 'if ((int)pages & 3)\n' + I6 + '\tpages = (pages + 4) & ~3;\n')]),
    ('cast2', [(C, I6 + 'if (pages & 3)\n' + I6 + '\tpages = ((int)pages + 4) & ~3;\n')]),
    ('round3', [(C, I6 + 'pages = (pages + 3) & ~3;\n')]),
    # pages as int for the whole function
    ('ipages', [(D, '\tuint32_t x, first, rem, tail, blocks, start, p, end, npages;\n\tint pages;\n'), (C, NC)]),
    ('ipagesdiv', [(D, '\tuint32_t x, first, rem, tail, blocks, start, p, end, npages;\n\tint pages;\n'), (C, NC), (SH, I6 + 'pages = len / 512;\n')]),
    # a local int for this arm's count
    ('loc', [(SH, I6 + 'int n = len >> 9;\n\n' + I6 + 'if (len % 512)\n' + I6 + '\tn++;\n' + I6 + 'pages = n;\n')]),
    ('pdiv', [(SH + I6 + 'if (len % 512)\n' + I6 + '\tpages++;\n',
               I6 + 'pages = len % 512 ? len / 512 + 1 : len / 512;\n')]),
    ('pdivc', [(SH + I6 + 'if (len % 512)\n' + I6 + '\tpages++;\n',
                I6 + 'pages = len % 512 ? len / 512 + 1 : len / 512;\n'), (C, NC)]),
    ('and511', [(SH + I6 + 'if (len % 512)\n', SH + I6 + 'if (len & 511)\n')]),
    ('and511c', [(SH + I6 + 'if (len % 512)\n', SH + I6 + 'if (len & 511)\n'), (C, NC)]),
    ('pm3', [(C, I6 + 'if (pages % 4)\n' + I6 + '\tpages = (pages + 4) & ~3;\n')]),
    ('pm3d', [(C, I6 + 'if (pages % 4)\n' + I6 + '\tpages = (pages + 4) & ~3;\n'), (SH, I6 + 'pages = len / 512;\n')]),
]
