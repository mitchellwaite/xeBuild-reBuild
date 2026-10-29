O = '\tif (!(mode && arg)) {'
ROK = '\t\t\trok: __attribute__((cold));\n'
FAIL = 'fail: __attribute__((cold));'
NC1 = '\t\t\tif (netConnect(ip)) {\n\t\t\trok:'
NC2 = '\t\tif (netConnect(ip)) {\n\t\t\tcinfo = netGetInfo();\n\t\t\tswitch'
conds = {'d': None, 'e': 'E(!(mode && arg))', 'm': '!(E(mode) && arg)', 'a': '!(mode && E(arg))'}
mods = {'0': [], 'r': [(ROK, '\t\t\trok:\n')], 'f': [(FAIL, 'fail:')], 'rf': [(ROK, '\t\t\trok:\n'), (FAIL, 'fail:')],
        'n1': [(NC1, '\t\t\tif (E(netConnect(ip))) {\n\t\t\trok:')], 'n2': [(NC2, NC2.replace('if (netConnect(ip))', 'if (E(netConnect(ip)))'))],
        'n12': [(NC1, '\t\t\tif (E(netConnect(ip))) {\n\t\t\trok:'), (NC2, NC2.replace('if (netConnect(ip))', 'if (E(netConnect(ip)))'))],
        'rn2': [(ROK, '\t\t\trok:\n'), (NC2, NC2.replace('if (netConnect(ip))', 'if (E(netConnect(ip)))'))],
        'u': [('\t\t} else\n\t\t\tclient_usage(2, NULL);', '\t\t} else {\n\t\t\tu2: __attribute__((cold));\n\t\t\tclient_usage(2, NULL);\n\t\t}')]}
VARS = []
for ck, c in conds.items():
    for mk, m in mods.items():
        VARS.append((ck + '_' + mk, ([(O, '\tif (%s) {' % c)] if c else []) + m))
