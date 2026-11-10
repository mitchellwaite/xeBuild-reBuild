"""Borderline review, net: netRecvVerbose's select arm, other stops than `size = got`.

The status flag on both arms is 4 lines off: only V's latch compare, `cmp ebx,esi; jge` for the
reference's `cmp esi,ebx; jle`.  gcc orders two SSA names by version (lower first), and the
unswitched copy's add takes a name off the free list, which the flag's threaded PHIs fill.
Axes: the select arm's stop and test, where status is declared and set to 1, and the recv test."""
from nbsweep import BASE, sub
import gen_nb4 as G

STOPS = {
    'size': ('size = got;', 'got >= size'),
    'st': ('status = 0;', 'status != 1'),
    'st-not': ('status = 0;', '!status'),
    'rr': ('', 'r == SOCKET_ERROR || r == 0'),
    'rle': ('', 'r <= 0'),
    'rlt': ('', 'r < 1'),
    'sz0': ('size = 0;', '!size'),
    'sz0ge': ('size = 0;', 'got >= size'),
}
INITS = ['decl', 'pre', 'block']
RECT = {'ne1': 'status != 1', 'not': '!status'}


def build(stop, init, rt):
    a, t = STOPS[stop]
    body = (G.SEL + ('\t\t\t\t' + a + '\n' if a else '') + '\t\t\t}\n\t\t\tif (' + t + ')\n\t\t\t\treturn NULL;\n' +
            G.RECV + '\t\t\t\tstatus = 0;\n\t\t\t}\n\t\t\tif (' + RECT[rt] + ')\n\t\t\t\tbreak;\n')
    text = BASE[:G.A] + G.loop('got < size', body) + BASE[G.B:]
    if init == 'pre':
        text = sub(text, '\tint status = 1;\n', '\tint status;\n')
        text = sub(text, '\t\tgot = 0;\n\t\twhile', '\t\tgot = 0;\n\t\tstatus = 1;\n\t\twhile')
    elif init == 'block':
        text = sub(text, '\tint status = 1;\n', '')
        text = sub(text, '\tif (size) {\n\t\tbuf = calloc', '\tif (size) {\n\t\tint status = 1;\n\n\t\tbuf = calloc')
    return text


def variants():
    for stop in STOPS:
        for init in INITS:
            for rt in RECT:
                yield '%s|%s|%s' % (stop, init, rt), build(stop, init, rt)
