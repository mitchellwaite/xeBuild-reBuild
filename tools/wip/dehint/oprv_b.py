# oprv.py variants: the product of natural spellings for parseOption's four borderline slots
# (cputemp/gpufan arms, the bool arm, the unknown-with-value test, macid's last five bytes),
# against 98a0eba6's src/options.c.  Labels: c<k>b<k>v<k>m<k>.
import itertools
import os

exec(open(os.path.join(os.path.dirname(__file__), 'oprv_a.py')).read())

LOOP1 = '''					for (i = 1; i < 6; i++) {
						log_printf(1, ":");
						xb.macid[i] = myatox8(val);
						val += 2;
						log_printf(1, "%02x", xb.macid[i]);
					}
'''

CPU = [('0', []), ('1', [(CPU_OLD, CPU_NEW), (GPU_OLD, GPU_NEW)])]
BOOL = [('0', []),
        ('1', boolf('setBoolOption(opt, val) == 1', '\n\tif (val) {\n')),
        ('2', boolf('setBoolOption(opt, val)', '\n\tif (val) {\n'))]
VLEN = [('0', []), ('1', [('\tif (val && vlen) {\n', '\tif (vlen) {\n')]),
        ('2', [('\tif (val && vlen) {\n', '\tif (vlen > 0) {\n')])]
MAC = [('0', []),
       ('1', [(MAC_OLD, '''					xb.macid[0] = myatox8(val);
					val += 2;
					log_printf(1, "%02x", xb.macid[0]);
''' + LOOP1)]),
       # the length in vlen, the loop bound from it (unknown until VRP)
       ('2', [('''			if (strlen(val) == 12) {
				if (validateString(val)) {''', '''			vlen = strlen(val);
			if (vlen == 12) {
				if (validateString(val)) {'''),
              (MAC_OLD, '''					xb.macid[0] = myatox8(val);
					val += 2;
					log_printf(1, "%02x", xb.macid[0]);
					for (i = 1; i < vlen / 2; i++) {
						log_printf(1, ":");
						xb.macid[i] = myatox8(val);
						val += 2;
						log_printf(1, "%02x", xb.macid[i]);
					}
''')]),
       ('3', [('''			if (strlen(val) == 12) {
				if (validateString(val)) {''', '''			vlen = strlen(val);
			if (vlen == 12) {
				if (validateString(val)) {'''),
              (MAC_OLD, '''					xb.macid[0] = myatox8(val);
					log_printf(1, "%02x", xb.macid[0]);
					for (i = 2; i < vlen; i += 2) {
						log_printf(1, ":");
						xb.macid[i / 2] = myatox8(val + i);
						log_printf(1, "%02x", xb.macid[i / 2]);
					}
''')]),
       ('4', [('''			if (strlen(val) == 12) {
				if (validateString(val)) {''', '''			len = strlen(val);
			if (len == 12) {
				if (validateString(val)) {'''),
              (MAC_OLD, '''					xb.macid[0] = myatox8(val);
					val += 2;
					log_printf(1, "%02x", xb.macid[0]);
					for (i = 1; i < len / 2; i++) {
						log_printf(1, ":");
						xb.macid[i] = myatox8(val);
						val += 2;
						log_printf(1, "%02x", xb.macid[i]);
					}
''')]),
       ]

V = []
for (c, cr), (b, br), (v, vr), (m, mr) in itertools.product(CPU, BOOL, VLEN, MAC):
    V.append(('c%sb%sv%sm%s' % (c, b, v, m), cr + br + vr + mr))
