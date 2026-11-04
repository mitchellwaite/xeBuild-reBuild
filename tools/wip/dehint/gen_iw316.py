# attempt 25: can the match (iw25pairs on sn.c, gen_iw234 f3 + gen_iw233 bm) lose its odd spellings? Base: build/iw/a25/pa_sn_0.c
# `IWB=build/iw/a25/pa_sn_0.c python tools/wip/dehint/iw16sweep.py tools/wip/dehint/gen_iw316.py -n 40 -t 4`
A = '\t\t\t\t\t\tif ((int)pages & 3)\n\t\t\t\t\t\t\tpages = ((int)pages + 4) & ~3;\n'
AXES = [
    [('', []),
     ('c0', [(A, '\t\t\t\t\t\tif (pages & 3)\n\t\t\t\t\t\t\tpages = (pages + 4) & ~3;\n')]),
     ('c1', [(A, '\t\t\t\t\t\tif (pages & 3)\n\t\t\t\t\t\t\tpages = ((int)pages + 4) & ~3;\n')]),
     ('c2', [(A, '\t\t\t\t\t\tif ((int)pages & 3)\n\t\t\t\t\t\t\tpages = (pages + 4) & ~3;\n')])],
    [('', []),
     ('l0', [('pages = len >> 9;\n\t\t\t\t\t\tif (len & 511)', 'pages = len / 512;\n\t\t\t\t\t\tif (len % 512)')]),
     ('l1', [('pages = len >> 9;', 'pages = len / 512;')]),
     ('l2', [('if (len & 511)', 'if (len % 512)')])],
    [('', []),
     ('d0', [('\tuint32_t pg;\n', '')])],
]
