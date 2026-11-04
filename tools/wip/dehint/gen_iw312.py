# attempt 25, pin_t: after ifcombine the merged test keeps the INNER test's probability (gen_iw311: 50 then 73 gives 657 at the optimized dump; a3, inner 50, gives 450 + 450, imgAdd clean), while imgAddFile, where `small` is known, sees only the test on len. So: outer test on a value holding the len test at 73, inner test at 50. `(int)(len < 0x4000) > 0` alone folds to != 0 before profile_estimate; `(int)(x & y) > 0` doesn't. type != '0' can sit in the outer value and type != 0 (no heuristic) be the inner test.
# `IWB=tools/wip/dehint/drafts/image_write_a24.c python tools/wip/dehint/iw25fr.py tools/wip/dehint/gen_iw312.py`
B = 'partial = small && len < 0x4000;\n\t\tif (partial > 0) {'
S = "\t\tsmall = type != 0 && type != '0';\n"
AXES = [[
    ('', []),
    ('k1', [(S + '\t\t' + B, "\t\tpartial = type != '0' && len < 0x4000;\n\t\tif (partial > 0 && type) {")]),
    ('k2', [(S + '\t\t' + B, "\t\tpartial = len < 0x4000 && type != '0';\n\t\tif (partial > 0 && type) {")]),
    ('k3', [(S + '\t\t' + B, "\t\tpartial = (type != '0') & (len < 0x4000);\n\t\tif (partial > 0 && type) {")]),
    ('k4', [(S + '\t\t' + B, "\t\tpartial = (len < 0x4000) & (type != '0');\n\t\tif (partial > 0 && type) {")]),
    ('k5', [(S + '\t\t' + B, "\t\tpartial = type != '0' && len < 0x4000;\n\t\tif (partial > 0 && type != 0) {")]),
    ('k6', [(S + '\t\t' + B, "\t\tsmall = type != '0' && len < 0x4000;\n\t\tpartial = small;\n\t\tif (partial > 0 && type) {")]),
    ('k7', [(S + '\t\t' + B, "\t\tpartial = type != '0' && len < 0x4000;\n\t\tif (partial > 0)\n\t\t\tpartial = type != 0;\n\t\tif (partial) {")]),
    ('m1', [(S + '\t\t' + B, "\t\tpartial = type != 0 && len < 0x4000;\n\t\tif (partial > 0 && type != '0') {")]),
    ('m2', [(S + '\t\t' + B, "\t\tpartial = type && len < 0x4000;\n\t\tif (partial > 0 && type != '0') {")]),
    ('m3', [(S + '\t\t' + B, "\t\tpartial = type != 0 && type != '0';\n\t\tif (partial > 0 && len < 0x4000) {")]),
]]
