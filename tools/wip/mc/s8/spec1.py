P = '\tif (!(mode && arg)) {'
C1 = '\t\t\tif (netConnect(ip)) {\n\t\t\trok'
C2 = '\t\tif (netConnect(ip)) {\n\t\t\tcinfo = netGetInfo();\n\t\t\tswitch'
VARS = [
 ('base', []),
 ('mgt', [(P, '\tif (!(mode > 0 && arg)) {')]),
 ('mge', [(P, '\tif (!(mode >= 1 && arg)) {')]),
 ('mlt', [(P, '\tif (mode <= 0 || !arg) {')]),
 ('swap', [(P, '\tif (!(arg && mode)) {')]),
 ('c2gt', [(C2, C2.replace('netConnect(ip)', 'netConnect(ip) > 0'))]),
 ('c1gt', [(C1, C1.replace('netConnect(ip)', 'netConnect(ip) > 0'))]),
 ('c12gt', [(C1, C1.replace('netConnect(ip)', 'netConnect(ip) > 0')), (C2, C2.replace('netConnect(ip)', 'netConnect(ip) > 0'))]),
 ('c2eq1', [(C2, C2.replace('netConnect(ip)', 'netConnect(ip) == 1'))]),
 ('c2ne0', [(C2, C2.replace('netConnect(ip)', 'netConnect(ip) != 0'))]),
 ('c2neg', [(C2, C2.replace('netConnect(ip)', 'netConnect(ip) >= 1'))]),
 ('mgt_c2gt', [(P, '\tif (!(mode > 0 && arg)) {'), (C2, C2.replace('netConnect(ip)', 'netConnect(ip) > 0'))]),
]
