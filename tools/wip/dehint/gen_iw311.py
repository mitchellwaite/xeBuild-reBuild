# attempt 25, pin_t: what's needed from gen_iw310: t's two tests split on the FIRST test's probability (a1: 50, so 450 + 450, imgAdd clean), imgAddFile only sees the SECOND (needs >= 56; `partial > 0` is 73). a1 folds `partial > 0` to `!= 0` before profile_estimate and a2 keeps it but makes the first test 73 too. Looking for 50 then 73.
# `IWB=tools/wip/dehint/drafts/image_write_a24.c python tools/wip/dehint/iw25fr.py tools/wip/dehint/gen_iw311.py`
B = 'partial = small && len < 0x4000;\n\t\tif (partial > 0) {'
E = '\t\t} else\n\t\t\tnpages = 32;\n\t\tp = 0;'
ARM = '\t\t\tif (len % 512)\n\t\t\t\tnpages = (len + 512) / 512;\n\t\t\telse\n\t\t\t\tnpages = len / 512;\n'
OLDARM = ARM + E
S = "small = type != 0 && type != '0';\n"
IS = [('\t_Bool small;\n', '\tint small;\n')]
P = 'partial = len < 0x4000;\n\t\t'
AXES = [[
    ('', []),
    ('n1', [(B + '\n' + OLDARM, 'npages = 32;\n\t\tif (small) {\n\t\t\tpartial = len < 0x4000;\n\t\t\tif (partial > 0) {\n' + ARM.replace('\t\t\t', '\t\t\t\t') + '\t\t\t}\n\t\t}\n\t\tp = 0;')]),
    ('n2', [(B + '\n' + OLDARM, P + 'npages = 32;\n\t\tif (small) {\n\t\t\tif (partial > 0) {\n' + ARM.replace('\t\t\t', '\t\t\t\t') + '\t\t\t}\n\t\t}\n\t\tp = 0;')]),
    ('n3', [(B + '\n' + OLDARM, P + 'if (small)\n\t\t\tif (partial > 0) {\n' + ARM.replace('\t\t\t', '\t\t\t\t') + '\t\t\t} else\n\t\t\t\tnpages = 32;\n\t\telse\n\t\t\tnpages = 32;\n\t\tp = 0;')]),
    ('n4', [(B + '\n' + OLDARM, 'if (small) {\n\t\t\tpartial = len < 0x4000;\n\t\t\tif (partial > 0) {\n' + ARM.replace('\t\t\t', '\t\t\t\t') + '\t\t\t} else\n\t\t\t\tnpages = 32;\n\t\t} else\n\t\t\tnpages = 32;\n\t\tp = 0;')]),
    ('n5', [(B + '\n' + OLDARM, P + 'if (!small)\n\t\t\tnpages = 32;\n\t\telse if (partial > 0) {\n' + ARM + '\t\t} else\n\t\t\tnpages = 32;\n\t\tp = 0;')]),
    ('i1', IS + [(B, P + 'if (small && partial > 0) {')]),
    ('i2', [('\t_Bool small;\n', '\tuint8_t small;\n'), (B, P + 'if (small && partial > 0) {')]),
    ('i3', [('\t_Bool small;\n', '\tuint32_t small;\n'), (B, P + 'if (small && partial > 0) {')]),
    ('i4', [(B, 'partial = len < 0x4000 ? 1 : 0;\n\t\tif (small && partial > 0) {')]),
    ('i5', [(B, 'partial = len < 0x4000;\n\t\tif (small != 0 && partial > 0) {')]),
    ('i6', [(B, 'partial = (int)(len < 0x4000);\n\t\tif (small == 1 && partial > 0) {')]),
    ('i7', [(B, 'if (small && (int)(len < 0x4000) > 0) {')]),
    ('i8', [(B, 'if (small && (len < 0x4000) > 0) {')]),
    ('i9', [(B, 'partial = small ? len < 0x4000 : 0;\n\t\tif (partial > 0) {')]),
    ('j1', [(B, 'partial = 0;\n\t\tif (small)\n\t\t\tpartial = len < 0x4000;\n\t\tif (partial > 0) {')]),
    ('j2', [(B, 'partial = 0;\n\t\tif (small && len < 0x4000)\n\t\t\tpartial = 1;\n\t\tif (partial > 0) {')]),
    ('j3', [(B, 'partial = len < 0x4000;\n\t\tif (!small)\n\t\t\tpartial = 0;\n\t\tif (partial > 0) {')]),
    ('j4', [(B, 'partial = small;\n\t\tif (partial)\n\t\t\tpartial = len < 0x4000;\n\t\tif (partial > 0) {')]),
    ('j5', [(B, 'partial = len < 0x4000;\n\t\tpartial = small ? partial : 0;\n\t\tif (partial > 0) {')]),
    ('j6', [(B, 'partial = len < 0x4000;\n\t\tpartial &= small;\n\t\tif (partial > 0) {')]),
    ('j7', [(B, 'partial = (len < 0x4000) & small;\n\t\tif (partial > 0) {')]),
    ('j8', [(B, 'partial = small & (len < 0x4000);\n\t\tif (partial) {')]),
]]
