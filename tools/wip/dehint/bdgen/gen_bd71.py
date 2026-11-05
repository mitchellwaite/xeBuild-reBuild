"""patchSmcConfig without no-early-inlining: bb-reorder's round 3 pops cpu's log before gpu's (a heap tie, keys equal).  Insertion
order follows edge order, so polarity of each test in both fan sections."""
REMOVE = ['nei_smc']
FOCUS = ['_patchSmcConfig']
W = 'log_printf(0, "***** WARNING: cpu fan speed %d override ignored, not between 40 and 100\\n", xb.cpuFan);'
CPU = '''		if (iniRangeOk("cpufan", xb.cpuFan, 40, 100)) {
			setFan(smc + 0x11, xb.cpuFan | 0x80);
			patched = 1;
		} else if (xb.cpuFan)
			''' + W + '''
		else if (smc[0x11] != 0x7f) {
			setFan(smc + 0x11, 0x7f);
			patched = 1;
		}
'''
OK = '''			setFan(smc + 0x11, xb.cpuFan | 0x80);
			patched = 1;
'''
ZERO = '''if (smc[0x11] != 0x7f) {
				setFan(smc + 0x11, 0x7f);
				patched = 1;
			}
'''
C = {
    'o': CPU,
    'z': '''		if (iniRangeOk("cpufan", xb.cpuFan, 40, 100)) {
''' + OK + '''		} else if (!xb.cpuFan) {
			''' + ZERO + '''		} else
			''' + W + '\n',
    'r': '''		if (!iniRangeOk("cpufan", xb.cpuFan, 40, 100)) {
			if (xb.cpuFan)
				''' + W + '''
			else ''' + ZERO + '''		} else {
''' + OK + '''		}
''',
    'rz': '''		if (!iniRangeOk("cpufan", xb.cpuFan, 40, 100)) {
			if (!xb.cpuFan) {
				''' + ZERO + '''			} else
				''' + W + '''
		} else {
''' + OK + '''		}
''',
    'e': '''		if (iniRangeOk("cpufan", xb.cpuFan, 40, 100)) {
''' + OK + '''		} else if (xb.cpuFan)
			''' + W + '''
		else if (smc[0x11] == 0x7f)
			;
		else {
			setFan(smc + 0x11, 0x7f);
			patched = 1;
		}
''',
    'g': '''		if (iniRangeOk("cpufan", xb.cpuFan, 40, 100)) {
''' + OK + '''		} else if (xb.cpuFan)
			goto cpuwarn;
		else if (smc[0x11] != 0x7f) {
			setFan(smc + 0x11, 0x7f);
			patched = 1;
		}
''',
}
GPU = '''		if (iniRangeOk("gpufan", xb.gpuFan, 40, 100)) {
			setFan(smc + 0x12, xb.gpuFan | 0x80);
			patched = 1;
		} else if (xb.gpuFan)
			goto gpuwarn;
		else {
			setFan(smc + 0x12, 0x7f);
		}
'''
G = {
    'o': GPU,
    'z': '''		if (iniRangeOk("gpufan", xb.gpuFan, 40, 100)) {
			setFan(smc + 0x12, xb.gpuFan | 0x80);
			patched = 1;
		} else if (!xb.gpuFan)
			setFan(smc + 0x12, 0x7f);
		else
			goto gpuwarn;
''',
    'r': '''		if (!iniRangeOk("gpufan", xb.gpuFan, 40, 100)) {
			if (xb.gpuFan)
				goto gpuwarn;
			setFan(smc + 0x12, 0x7f);
		} else {
			setFan(smc + 0x12, xb.gpuFan | 0x80);
			patched = 1;
		}
''',
}
AXES = [[('c' + k, [(CPU, v)]) for k, v in C.items() if k != 'g'], [('g' + k, [(GPU, v)]) for k, v in G.items()]]
