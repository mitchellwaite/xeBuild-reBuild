# separate tests; tune arg-test probability near 50% so the hot layout stays and d rises
P = '\tif (!(mode && arg)) {'
A = '({ __asm__(""); 0; })'
VARS = []
for mn, m in (('le', 'mode <= 0'), ('eq', '!mode'), ('lt', 'mode < 1')):
    for an, a in (('E', 'E(!arg)'), ('Ene', '!E(arg != 0)'), ('Eeq', 'E(arg == 0)'), ('neg', '!(arg != 0)'), ('cmpd', 'arg == (char *)0')):
        VARS.append(('%s_%s' % (mn, an), [(P, '\tif (%s || %s || %s) {' % (m, A, a))]))
