# patchSmcConfig without nei and cb_hints: the cpu and gpu log blocks tie at 348.  iniRangeOk written out in the
# gpu section, without the -1 test its caller already made, makes the sections differ for real.
REMOVE = ['nei_smc', 'cb1', 'cb2', 'cb3', 'cb4']
FOCUS = ['_patchSmcConfig']
L = '''log_printf(0, "Ini value %d for %s is out of range (%d-%d), not using\\n", xb.gpuFan, "gpufan", 40, 100);'''
OLD = '''		if (iniRangeOk("gpufan", xb.gpuFan, 40, 100)) {
			smc[0x12] = xb.gpuFan | 0x80;
			patched = 1;
		} else if (xb.gpuFan)
			goto gpuwarn;
		else {
			smc[0x12] = 0x7f;
		}
'''
A = [
    ('w1', [(OLD, '''		if (xb.gpuFan >= 40 && xb.gpuFan <= 100) {
			smc[0x12] = xb.gpuFan | 0x80;
			patched = 1;
		} else {
			if (xb.gpuFan)
				''' + L + '''
			if (xb.gpuFan)
				goto gpuwarn;
			smc[0x12] = 0x7f;
		}
''')]),
    ('w2', [(OLD, '''		if (xb.gpuFan < 40 || xb.gpuFan > 100) {
			if (xb.gpuFan)
				''' + L + '''
			if (xb.gpuFan)
				goto gpuwarn;
			smc[0x12] = 0x7f;
		} else {
			smc[0x12] = xb.gpuFan | 0x80;
			patched = 1;
		}
''')]),
    ('w3', [(OLD, '''		if (xb.gpuFan >= 40 && xb.gpuFan <= 100) {
			smc[0x12] = xb.gpuFan | 0x80;
			patched = 1;
		} else if (xb.gpuFan) {
			''' + L + '''
			if (xb.gpuFan)
				goto gpuwarn;
			smc[0x12] = 0x7f;
		} else
			smc[0x12] = 0x7f;
''')]),
    ('w4', [(OLD, '''		int ok = 1;

		if (xb.gpuFan < 40 || xb.gpuFan > 100) {
			ok = 0;
			if (xb.gpuFan)
				''' + L + '''
		}
		if (ok) {
			smc[0x12] = xb.gpuFan | 0x80;
			patched = 1;
		} else if (xb.gpuFan)
			goto gpuwarn;
		else
			smc[0x12] = 0x7f;
''')]),
]
AXES = [A]
