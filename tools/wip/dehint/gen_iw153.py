# attempt 9: gen_iw47's hdr load orders (a hdr local read before spare swaps the pseudo tie) on the expect-75 stand-in for head freq >= 350,
# wanted: IDENTICAL or only load order left.
import importlib.util, os, re
s = importlib.util.spec_from_file_location('g47', os.path.join(os.path.dirname(os.path.abspath(__file__)), 'gen_iw47.py'))
g = importlib.util.module_from_spec(s)
s.loader.exec_module(g)
OLD = g.OLD.replace('			__asm__("" :: "a"(xb.hdr));\n', '')
OLD = OLD.replace('if (!pageErased(xb.hdr + (b * 32 + p) * 512, xb.spare + (b * 32 + p) * 16))', 'if (__builtin_expect(!pageErased(xb.hdr + (b * 32 + p) * 512, xb.spare + (b * 32 + p) * 16), 0))')
def ex(f):
    return re.sub(r'if \(!pageErased\((.*?)\)\)\n', lambda m: 'if (__builtin_expect(!pageErased(%s), 0))\n' % m.group(1), f)
AXES = [[(n + '+' + t, [(OLD, ex(f) + tf)]) for n, f in g.HEADS.items() if not n.startswith('h9') for t, tf in g.TAILS.items()]]
BASE = 'build/iw/a9/ex.c'
FLAGS = ['--param', 'builtin-expect-probability=75']
FOCUS = ['_finalizeImage']
