"""opn.py: noecdremap through optIniBoolG with optN's dead entry test moved to the call site
(optN dropped), several spellings, scored with optlib."""
import os, sys
from concurrent.futures import ThreadPoolExecutor
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import optlib, opmerge

CALL = '	if (!(xb.bootFlags & 0x80000000)) optN("noecdremap", 0x80000000, 0, 0);\n'
EN = '__builtin_expect(__builtin_constant_p(xb.bootFlags + 2), 0)'
G = 'optIniBoolG("noecdremap", 0x80000000, 0, 0);'
V = {
    'and': '	if (!(xb.bootFlags & 0x80000000) && !%s) %s\n' % (EN, G),
    'nest': '	if (!(xb.bootFlags & 0x80000000)) {\n		if (!%s)\n			%s\n	}\n' % (EN, G),
    'else': '	if (!(xb.bootFlags & 0x80000000)) {\n		if (%s)\n			;\n		else\n			%s\n	}\n' % (EN, G),
    'goto': '	if (!(xb.bootFlags & 0x80000000)) {\n		if (%s)\n			goto n;\n		%s\n	}\nn:\n' % (EN, G),
    'plain': '	if (!(xb.bootFlags & 0x80000000)) %s\n' % G,
}


def make(n):
    t = optlib.read_src(optlib.SRC)
    assert CALL in t
    t = opmerge.drop_def(t, 'optN')
    return t.replace(CALL, V[n])


if __name__ == '__main__':
    def one(n):
        return n, optlib.score_text(make(n))
    with ThreadPoolExecutor(6) as p:
        for n, r in p.map(one, V):
            print('%-6s %s' % (n, optlib.fmt(r)))
