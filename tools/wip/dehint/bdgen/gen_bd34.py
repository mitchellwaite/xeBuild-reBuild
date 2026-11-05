# patchSmcConfig: iniRangeOk written out in the gpu section, keeping both of its log tests (the reference has
# the 0 and -1 range test), in several spellings; cpu with the helper or written out likewise.
REMOVE = ['nei_smc', 'cb1', 'cb2', 'cb3', 'cb4']
FOCUS = ['_patchSmcConfig']
L = '''log_printf(0, "Ini value %%d for %%s is out of range (%%d-%%d), not using\\n", xb.%sFan, "%sfan", 40, 100);'''
OLDG = '''		if (iniRangeOk("gpufan", xb.gpuFan, 40, 100)) {
			smc[0x12] = xb.gpuFan | 0x80;
			patched = 1;
		} else if (xb.gpuFan)
			goto gpuwarn;
		else {
			smc[0x12] = 0x7f;
		}
'''
TESTS = {
    't0': 'if (xb.gpuFan != 0 && xb.gpuFan != 0xffffffff)\n\t\t\t\t',
    't1': 'if (xb.gpuFan != 0xffffffff && xb.gpuFan != 0)\n\t\t\t\t',
    't2': 'if (xb.gpuFan)\n\t\t\t\tif (xb.gpuFan != 0xffffffff)\n\t\t\t\t\t',
    't3': 'if (xb.gpuFan != 0xffffffff)\n\t\t\t\tif (xb.gpuFan)\n\t\t\t\t\t',
    't4': 'if (xb.gpuFan - 1 < 0xfffffffe)\n\t\t\t\t',
}
A = []
for k, t in TESTS.items():
    log = t + L % ('gpu', 'gpu')
    A.append((k + 'f', [(OLDG, '''		int ok = 1;

		if (xb.gpuFan < 40 || xb.gpuFan > 100) {
			ok = 0;
			''' + log + '''
		}
		if (ok) {
			smc[0x12] = xb.gpuFan | 0x80;
			patched = 1;
		} else if (xb.gpuFan)
			goto gpuwarn;
		else
			smc[0x12] = 0x7f;
''')]))
    A.append((k + 'n', [(OLDG, '''		if (xb.gpuFan >= 40 && xb.gpuFan <= 100) {
			smc[0x12] = xb.gpuFan | 0x80;
			patched = 1;
		} else {
			''' + log + '''
			if (xb.gpuFan)
				goto gpuwarn;
			smc[0x12] = 0x7f;
		}
''')]))
    A.append((k + 'i', [(OLDG, '''		if (xb.gpuFan < 40 || xb.gpuFan > 100) {
			''' + log + '''
			if (xb.gpuFan)
				goto gpuwarn;
			smc[0x12] = 0x7f;
		} else {
			smc[0x12] = xb.gpuFan | 0x80;
			patched = 1;
		}
''')]))
AXES = [A]
