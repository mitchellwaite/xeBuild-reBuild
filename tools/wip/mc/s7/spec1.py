# s7: entry-guard shapes that might give usage(2) a small nonzero frequency (~3) instead of 4.28 or 0
L = '\tfor (i = 0; i < argc; i++) {'
P = '\tif (!(mode && arg)) {'
D = '\tif (E(!(mode && arg))) {'
G = {
 'g_e':   '\tif (E(argc < 1)) client_usage(2, NULL);\n',
 'g_ee':  '\tif (E(argc < 1) && E(!reboot)) client_usage(2, NULL);\n',
 'g_lt':  '\tif (argc < 1 && !promptEnter) client_usage(2, NULL);\n',
 'g_ptr': '\tif (!argv) client_usage(2, NULL);\n',
}
VARS = []
for k, g in G.items():
    for dn, d in (('p', P), ('d', D)):
        VARS.append((k + '_' + dn, [(L, g + L), (P, d)]))
VARS.append(('loopE', [(L, '\tfor (i = 0; E(i < argc); i++) {'), (P, D)]))
VARS.append(('loopNE', [(L, '\tfor (i = 0; __builtin_expect(i < argc, 1); i++) {')]))
