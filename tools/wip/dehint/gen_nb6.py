"""Borderline review, net: netRecvVerbose with `size = 0` as the stop on the select arm (gen_nb5's
match) and on the recv arm too, so no status flag; and `buf = NULL` after the free as the stop.

recv arm: status (control), size = 0 then a test that breaks or returns, or no test (the loop's
own `got < size` ends it); post-loop test spellings for size."""
from nbsweep import BASE, sub
import gen_nb4 as G

SELS = {
    'sz0': ('size = 0;', '!size'),
    'sz0eq': ('size = 0;', 'size == 0'),
    'buf': ('buf = NULL;', '!buf'),
}
RECS = {
    'st': ('status = 0;', '!status', 'break;'),
    'szb': ('size = 0;', '!size', 'break;'),
    'szr': ('size = 0;', '!size', 'return NULL;'),
    'szn': ('size = 0;', None, None),
    'bufb': ('buf = NULL;', '!buf', 'break;'),
}
POSTS = {'st': 'status != 1', 'not': '!size', 'eq': 'size == 0', 'lt1': 'size < 1', 'le0': 'size <= 0', 'none': None, 'buf': '!buf'}


def build(s, rc, p):
    a, t = SELS[s]
    ra, rt, rx = RECS[rc]
    body = (G.SEL + '\t\t\t\t' + a + '\n\t\t\t}\n\t\t\tif (' + t + ')\n\t\t\t\treturn NULL;\n' +
            G.RECV + '\t\t\t\t' + ra + '\n\t\t\t}\n' + ('\t\t\tif (' + rt + ')\n\t\t\t\t' + rx + '\n' if rt else ''))
    lp = G.loop('got < size', body)
    post = POSTS[p]
    lp = sub(lp, G.POST, '\t\tif (' + post + ')\n\t\t\treturn NULL;\n' if post else '')
    text = BASE[:G.A] + lp + BASE[G.B:]
    if rc != 'st' and p != 'st':
        text = sub(text, '\tint status = 1;\n', '')
    return text


def variants():
    for s in SELS:
        for rc in RECS:
            for p in POSTS:
                if (p == 'st') != (rc == 'st'):
                    continue
                if rc == 'szr' and p != 'none':
                    continue
                if rc != 'szr' and p == 'none':
                    continue
                if (p == 'buf') != (rc == 'bufb'):
                    continue
                yield '%s|%s|%s' % (s, rc, p), build(s, rc, p)
