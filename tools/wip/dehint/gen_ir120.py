"""measurement: gen_ir119's best forms with attribute options (what decides `mov edi,ebx` and `mov ebx,edi`)."""
import importlib.util, os
spec = importlib.util.spec_from_file_location('g', os.path.join(os.path.dirname(os.path.abspath(__file__)), 'gen_ir119.py'))
g = importlib.util.module_from_spec(spec)
spec.loader.exec_module(g)
FOCUS = g.FOCUS
BASE = g.BASE
OPTS = {'o0': '', 'if1': '"no-if-conversion"', 'if2': '"no-if-conversion2"', 'tm': '"no-tree-tail-merge"',
        'cj': '"no-crossjumping"', 'pre': '"no-tree-pre"', 'sink': '"no-tree-sink"', 'cf': '"no-if-conversion", "no-if-conversion2", "no-tree-tail-merge"',
        'g': '"no-gcse"', 'cse': '"no-cse-follow-jumps"', 's2': '"no-schedule-insns2"', 'ter': '"no-tree-ter"', 'cpr': '"no-cprop-registers"', 'rr': '"no-rerun-cse-after-loop"'}
AX = []
for k, ed in g.AX:
    if k not in ('d1.t6.k3.a', 'd1.t6.k7.a'):
        continue
    old, new = ed[0]
    for ko, o in OPTS.items():
        AX.append((k + '.' + ko, [(old, new.replace('void getImageSmc', ('__attribute__((optimize(%s))) ' % o if o else '') + 'void getImageSmc'))]))
AXES = [AX]
