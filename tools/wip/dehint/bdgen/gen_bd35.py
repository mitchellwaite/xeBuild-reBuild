# patchSmcConfig: writing iniRangeOk out lowers a section's log block (348 -> 298).  The reference has gpu's first,
# so write out cpu's and leave gpu with the helper.  Also which of the two has the else-if tail nested.
REMOVE = ['nei_smc', 'cb1', 'cb2', 'cb3', 'cb4']
FOCUS = ['_patchSmcConfig']
L = '''log_printf(0, "Ini value %d for %s is out of range (%d-%d), not using\\n", xb.cpuFan, "cpufan", 40, 100);'''
W = '''log_printf(0, "***** WARNING: cpu fan speed %d override ignored, not between 40 and 100\\n", xb.cpuFan);'''
OLD = '''		if (iniRangeOk("cpufan", xb.cpuFan, 40, 100)) {
			smc[0x11] = xb.cpuFan | 0x80;
			patched = 1;
		} else if (xb.cpuFan)
			''' + W + '''
		else if (smc[0x11] != 0x7f) {
			smc[0x11] = 0x7f;
			patched = 1;
		}
'''
TESTS = {
    't0': 'if (xb.cpuFan != 0 && xb.cpuFan != 0xffffffff)\n\t\t\t\t',
    't1': 'if (xb.cpuFan != 0xffffffff && xb.cpuFan != 0)\n\t\t\t\t',
    't2': 'if (xb.cpuFan)\n\t\t\t\tif (xb.cpuFan != 0xffffffff)\n\t\t\t\t\t',
    't3': 'if (xb.cpuFan != 0xffffffff)\n\t\t\t\tif (xb.cpuFan)\n\t\t\t\t\t',
}
TAIL = '''else if (xb.cpuFan)
			''' + W + '''
		else if (smc[0x11] != 0x7f) {
			smc[0x11] = 0x7f;
			patched = 1;
		}
'''
A = []
for k, t in TESTS.items():
    log = t + L
    A.append((k + 'f', [(OLD, '''		int ok = 1;

		if (xb.cpuFan < 40 || xb.cpuFan > 100) {
			ok = 0;
			''' + log + '''
		}
		if (ok) {
			smc[0x11] = xb.cpuFan | 0x80;
			patched = 1;
		} ''' + TAIL)]))
    A.append((k + 'n', [(OLD, '''		if (xb.cpuFan >= 40 && xb.cpuFan <= 100) {
			smc[0x11] = xb.cpuFan | 0x80;
			patched = 1;
		} else {
			''' + log + '''
			if (xb.cpuFan)
				''' + W + '''
			else if (smc[0x11] != 0x7f) {
				smc[0x11] = 0x7f;
				patched = 1;
			}
		}
''')]))
AXES = [A]
