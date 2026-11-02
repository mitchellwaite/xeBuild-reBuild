"""gen0.py OUT.c: profile-free base from src/options.c (pragmas and aio_never dead edges removed, OPT as written)."""
import sys, os
ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..', '..'))
t = open(ROOT + '/src/options.c', newline='').read()
for l in ['#pragma GCC push_options\n', '#pragma GCC pop_options\n',
          '#pragma GCC optimize ("no-branch-probabilities", "no-reorder-functions")\n']:
    if '--keep-pragmas' not in sys.argv: t = t.replace(l, '')
t = t.replace('parseButtonI(getIniValue("xellbutton2"), aio_never)', 'parseButtonI(getIniValue("xellbutton2"), 0)')
def cut(t, a, b):
    i = t.index(a); j = t.index(b, i) + len(b)
    return t[:i], t[j:]
h, r = cut(t, '\t\t/* OPT("olddvd", 0, 4) with dead edges', '\t\t} while (0);\n')
t = h + '\t\tOPT("olddvd", 0, 4);\n' + r
h, r = cut(t, '\t} else if (aio_never) {', '\t\tgoto tail;\n\t}\n')
t = h + '\t}\n' + r
t = t.replace('blsuffix:\n', '')
h, r = cut(t, '\t/* a dead cycle through the blSuffix test', '\t\tgoto blsuffix;\n')
t = h + r
t = t.replace('static int aio_never, aio_never2, aio_never3, aio_never4;\n', '')
open(sys.argv[1], 'w', newline='\n').write(t)
