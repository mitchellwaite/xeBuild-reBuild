# break ifcombine on the post-loop (mode && arg) test so opcode/pointer heuristics fire separately
P = '\tif (!(mode && arg)) {'
A = '({ __asm__(""); 0; })'
VARS = [
 ('sx_eq',   [(P, '\tif (!mode || %s || !arg) {' % A)]),
 ('sx_le',   [(P, '\tif (mode <= 0 || %s || !arg) {' % A)]),
 ('sx_lt1',  [(P, '\tif (mode < 1 || %s || !arg) {' % A)]),
 ('sx_ar1',  [(P, '\tif (!arg || %s || !mode) {' % A)]),
 ('sx_ar2',  [(P, '\tif (!arg || %s || mode <= 0) {' % A)]),
 ('sv_eq',   [(P, '\tif (!mode || ({ __asm__ volatile(""); 0; }) || !arg) {')]),
]
