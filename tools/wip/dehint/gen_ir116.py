"""measurement: gen_ir115's best forms with attribute options, to see which parts of what's left each option decides."""
import importlib.util, os
spec = importlib.util.spec_from_file_location('g115', os.path.join(os.path.dirname(os.path.abspath(__file__)), 'gen_ir115.py'))
g = importlib.util.module_from_spec(spec)
spec.loader.exec_module(g)
FOCUS = g.FOCUS
BASE = g.BASE
OPTS = {'o0': '', 'if2': '__attribute__((optimize("no-if-conversion2"))) ', 'tm': '__attribute__((optimize("no-tree-tail-merge"))) ',
        'both': '__attribute__((optimize("no-if-conversion2", "no-tree-tail-merge"))) '}
AX = []
for k, ed in g.AX:
    if not k.endswith('.a.s1.ex'):
        continue
    old, new = ed[0]
    for ko, o in OPTS.items():
        AX.append((k + '.' + ko, [(old, new.replace('void getImageSmc', o + 'void getImageSmc'))]))
AXES = [AX]
