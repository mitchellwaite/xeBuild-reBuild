"""patchSmcConfig: cpu section written out (near miss of gen_bd35): success arm 1029 must be at most 732.  The flag's test gets a
predictor (`ok == 1` gets PRED_OPCODE_NONEQUAL: 28%), or there is no flag, or the arm order changes."""
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
TAIL = '''		if (@@) {
			smc[0x11] = xb.cpuFan | 0x80;
			patched = 1;
		} else if (xb.cpuFan)
			''' + W + '''
		else if (smc[0x11] != 0x7f) {
			smc[0x11] = 0x7f;
			patched = 1;
		}
'''
RTAIL = '''		if (@@) {
			if (xb.cpuFan)
				''' + W + '''
			else if (smc[0x11] != 0x7f) {
				smc[0x11] = 0x7f;
				patched = 1;
			}
		} else {
			smc[0x11] = xb.cpuFan | 0x80;
			patched = 1;
		}
'''
LOGT = 'if (xb.cpuFan != 0 && xb.cpuFan != 0xffffffff)\n\t\t\t\t' + L
HEADS = {
    'a': '''		int ok = 1;

		if (xb.cpuFan < 40 || xb.cpuFan > 100) {
			ok = 0;
			''' + LOGT + '''
		}
''',
    'b': '''		int ok = 0;

		if (xb.cpuFan >= 40 && xb.cpuFan <= 100)
			ok = 1;
		else {
			''' + LOGT + '''
		}
''',
}
V = {}
for h, hv in HEADS.items():
    for t in ('ok', 'ok == 1', 'ok != 0', 'ok > 0', 'ok >= 1'):
        V[h + '[' + t + ']'] = hv + TAIL.replace('@@', t)
    for t in ('!ok', 'ok != 1', 'ok == 0', 'ok <= 0', 'ok < 1'):
        V[h + 'r[' + t + ']'] = hv + RTAIL.replace('@@', t)
V['noflag'] = '''		if (xb.cpuFan >= 40 && xb.cpuFan <= 100) {
			smc[0x11] = xb.cpuFan | 0x80;
			patched = 1;
		} else {
			''' + LOGT + '''
			if (xb.cpuFan)
				''' + W + '''
			else if (smc[0x11] != 0x7f) {
				smc[0x11] = 0x7f;
				patched = 1;
			}
		}
'''
V['noflagr'] = '''		if (xb.cpuFan < 40 || xb.cpuFan > 100) {
			''' + LOGT + '''
			if (xb.cpuFan)
				''' + W + '''
			else if (smc[0x11] != 0x7f) {
				smc[0x11] = 0x7f;
				patched = 1;
			}
		} else {
			smc[0x11] = xb.cpuFan | 0x80;
			patched = 1;
		}
'''
AXES = [[(k, [(OLD, v)]) for k, v in V.items()]]
