# attempt 25, pin_t: gen_iw312's `&&` forms fold `partial > 0` to != 0, but nested ifs keep it (gen_iw311 n2). Outer `partial > 0` on the len test (73, what imgAddFile sees), inner test on small (50, what imgAdd's merged test keeps).
# `IWB=tools/wip/dehint/drafts/image_write_a24.c python tools/wip/dehint/iw25fr.py tools/wip/dehint/gen_iw313.py`
B = '\t\tpartial = small && len < 0x4000;\n\t\tif (partial > 0) {\n'
ARM = '\t\t\tif (len % 512)\n\t\t\t\tnpages = (len + 512) / 512;\n\t\t\telse\n\t\t\t\tnpages = len / 512;\n'
ARM2 = ARM.replace('\t\t\t', '\t\t\t\t')
E = '\t\t} else\n\t\t\tnpages = 32;\n\t\tp = 0;'
O = B + ARM + E
P = '\t\tpartial = len < 0x4000;\n'
AXES = [[
    ('', []),
    ('q1', [(O, P + '\t\tif (partial > 0) {\n\t\t\tif (small) {\n' + ARM2 + '\t\t\t} else\n\t\t\t\tnpages = 32;\n' + E)]),
    ('q2', [(O, P + '\t\tnpages = 32;\n\t\tif (partial > 0) {\n\t\t\tif (small) {\n' + ARM2 + '\t\t\t}\n\t\t}\n\t\tp = 0;')]),
    ('q3', [(O, P + '\t\tif (partial > 0) {\n\t\t\tif (!small)\n\t\t\t\tnpages = 32;\n\t\t\telse {\n' + ARM2 + '\t\t\t}\n' + E)]),
    ('q4', [(O, P + '\t\tif (partial <= 0)\n\t\t\tnpages = 32;\n\t\telse if (small) {\n' + ARM + '\t\t} else\n\t\t\tnpages = 32;\n\t\tp = 0;')]),
    ('q5', [(O, P + '\t\tif (partial > 0 && small > 0) {\n' + ARM + E)]),
    ('q6', [(O, P + '\t\tif (partial > 0)\n\t\t\tpartial = small;\n\t\tif (partial > 0) {\n' + ARM + E)]),
    ('q7', [(O, P + '\t\tif (partial > 0)\n\t\t\tpartial = small;\n\t\tif (partial) {\n' + ARM + E)]),
    ('q8', [(O, P + '\t\tnpages = 32;\n\t\tif (partial > 0)\n\t\t\tif (small)\n\t\t\t\tnpages = len % 512 ? (len + 512) / 512 : len / 512;\n\t\tp = 0;')]),
]]
