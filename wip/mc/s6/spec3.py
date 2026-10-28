O = '\tif (!(mode && arg)) {'
L = '\tfor (i = 0; i < argc; i++) {'
U = '\t\t} else\n\t\t\tclient_usage(2, NULL);'
G = {'g0': None, 'gn': '\tif (argc < 1)\n\t\tclient_usage(2, NULL);\n' + L,
     'gl': '\tif (argc < 1) {\n\t\tlog_set_name("client");\n\t}\n' + L}
P = {'pd': None, 'pm': '!(E(mode) && arg)', 'pe': 'E(!(mode && arg))', 'pa': '!(mode && E(arg))'}
R = {'r0': None, 'rE': '\t\t} else if (E(1))\n\t\t\tclient_usage(2, NULL);', 'rh': '\t\t} else {\n\t\t\tu2: __attribute__((hot));\n\t\t\tclient_usage(2, NULL);\n\t\t}'}
VARS = []
for gk, g in G.items():
    for pk, p in P.items():
        for rk, r in R.items():
            reps = []
            if g: reps.append((L, g))
            if p: reps.append((O, '\tif (%s) {' % p))
            if r: reps.append((U, r))
            VARS.append(('%s_%s_%s' % (gk, pk, rk), reps))
