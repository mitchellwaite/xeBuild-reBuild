O = '\tif (!(mode && arg)) {'
C = ['!(E(mode) && arg)', '!(mode && E(arg))', '!E(mode) || !arg', '!mode || !E(arg)', '!E(mode) || !E(arg)',
     '__builtin_expect(!mode, 0) || !arg', '!mode || __builtin_expect(!arg, 0)', 'E(!mode) || !arg', '!mode || E(!arg)',
     'mode <= 0 || !arg', '!(mode && arg)', 'E(!(mode && arg))']
VARS = [('c%d' % i, [(O, '\tif (%s) {' % c)]) for i, c in enumerate(C)]
