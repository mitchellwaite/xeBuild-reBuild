# attempt 25, pin_t: P 70 from the pointer heuristic. 900 * 70% lands on the grid (630 + 270), and 70 >= 56 for imgAddFile, but the flag has to be tested as a pointer at profile_estimate. Attempt 20 only had this as an untested remark.
# `IWB=tools/wip/dehint/drafts/image_write_a24.c python tools/wip/dehint/iw16sweep.py tools/wip/dehint/gen_iw309.py -n 20 -t 4`
A = 'int partial;\n'
B = 'partial = small && len < 0x4000;\n\t\tif (partial > 0) {'
AXES = [[
    ('', []),
    ('c1', [(B, 'partial = small && len < 0x4000;\n\t\tif ((void *)partial) {')]),
    ('c2', [(B, 'partial = small && len < 0x4000;\n\t\tif ((const uint8_t *)partial != 0) {')]),
    ('c3', [(A, 'const void *partial;\n'), (B, 'partial = (const void *)(small && len < 0x4000);\n\t\tif (partial) {')]),
    ('c4', [(A, 'const void *partial;\n'), (B, 'partial = (const void *)(uintptr_t)(small && len < 0x4000);\n\t\tif (partial != 0) {')]),
    ('c5', [(A, 'const void *partial;\n'), (B, 'partial = small && len < 0x4000 ? src : 0;\n\t\tif (partial) {')]),
    ('c6', [(A, 'const void *partial;\n'), (B, 'partial = small && len < 0x4000 ? (const void *)1 : 0;\n\t\tif (partial) {')]),
    ('c7', [(A, 'const void *partial;\n'), (B, 'partial = 0;\n\t\tif (small && len < 0x4000)\n\t\t\tpartial = src;\n\t\tif (partial) {')]),
    ('c8', [(A, 'const void *partial;\n'), (B, 'partial = small && len < 0x4000 ? &xb : 0;\n\t\tif (partial) {')]),
    ('c9', [(B, 'partial = small && len < 0x4000;\n\t\tif ((char *)0 + partial) {')]),
]]
