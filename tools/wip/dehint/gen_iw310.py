# attempt 25, pin_t: two tests that ifcombine merges. In imgAddFile `small` is known, so the partial arm's probability there is the len test's alone: `len < 0x4000` has no heuristic (50), which is the P floor. Give the len test the opcode heuristic through an int flag, 73.
# `IWB=tools/wip/dehint/drafts/image_write_a24.c python tools/wip/dehint/iw16sweep.py tools/wip/dehint/gen_iw310.py -n 30 -t 4`
B = 'partial = small && len < 0x4000;\n\t\tif (partial > 0) {'
P = 'partial = len < 0x4000;\n\t\t'
AXES = [[
    ('', []),
    ('a1', [(B, P + 'if (small && partial > 0) {')]),
    ('a2', [(B, P + 'if (small > 0 && partial > 0) {')]),
    ('a3', [(B, P + 'if (partial > 0 && small) {')]),
    ('a4', [(B, P + 'if (partial > 0 && small > 0) {')]),
    ('a5', [(B, P + 'if (small)\n\t\t\tpartial = partial > 0;\n\t\telse\n\t\t\tpartial = 0;\n\t\tif (partial) {')]),
    ('a6', [(B, P + 'if (!small || partial <= 0)\n\t\t\tnpages = 32;\n\t\telse {'), ('\t\t} else\n\t\t\tnpages = 32;\n\t\tp = 0;', '\t\t}\n\t\tp = 0;')]),
    ('a7', [(B, P + 'if (type != 0 && type != \'0\' && partial > 0) {')]),
    ('a8', [(B, P + 'if ((type != 0) > 0 && type != \'0\' && partial > 0) {')]),
    ('a9', [(B, 'partial = small;\n\t\tif (partial > 0 && len < 0x4000) {')]),
    ('b1', [(B, 'if ((void *)(len < 0x4000) && small) {')]),
    ('b2', [(B, 'if (small && (void *)(len < 0x4000)) {')]),
    ('b3', [(B, 'if (small > 0 && (void *)(len < 0x4000)) {')]),
    ('b4', [(B, 'partial = small;\n\t\tif (partial > 0 && (void *)(len < 0x4000)) {')]),
]]
