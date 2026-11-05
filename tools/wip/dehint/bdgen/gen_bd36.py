# patchSmcConfig, base gen_bd35's cpu written out: logs in the right order (cpu 298, gpu 348), but the cpu success arm is
# 1029 and has to be at most gpu's 732.  Spellings of the written-out range test and flag.
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
TAIL = '''		if (ok) {
			smc[0x11] = xb.cpuFan | 0x80;
			patched = 1;
		} else if (xb.cpuFan)
			''' + W + '''
		else if (smc[0x11] != 0x7f) {
			smc[0x11] = 0x7f;
			patched = 1;
		}
'''
LOGT = 'if (xb.cpuFan != 0 && xb.cpuFan != 0xffffffff)\n\t\t\t\t' + L
F = {
    'a': '''		int ok = 0;

		if (xb.cpuFan >= 40 && xb.cpuFan <= 100)
			ok = 1;
		else {
			''' + LOGT + '''
		}
''',
    'b': '''		int ok = xb.cpuFan >= 40 && xb.cpuFan <= 100;

		if (!ok) {
			''' + LOGT + '''
		}
''',
    'c': '''		int ok = 1;

		if (xb.cpuFan < 40)
			ok = 0;
		if (xb.cpuFan > 100)
			ok = 0;
		if (!ok) {
			''' + LOGT + '''
		}
''',
    'd': '''		int ok = 0;

		if (xb.cpuFan >= 40) {
			if (xb.cpuFan <= 100)
				ok = 1;
		}
		if (!ok) {
			''' + LOGT + '''
		}
''',
    'e': '''		int ok = 1;

		if (xb.cpuFan < 40) {
			ok = 0;
		} else if (xb.cpuFan > 100) {
			ok = 0;
		}
		if (!ok) {
			''' + LOGT + '''
		}
''',
    'g': '''		int ok = 1;

		if (xb.cpuFan - 40 > 60) {
			ok = 0;
			''' + LOGT + '''
		}
''',
    'h': '''		int ok = xb.cpuFan - 40 <= 60;

		if (!ok) {
			''' + LOGT + '''
		}
''',
}
AXES = [[(k, [(OLD, v + TAIL)]) for k, v in F.items()]]
