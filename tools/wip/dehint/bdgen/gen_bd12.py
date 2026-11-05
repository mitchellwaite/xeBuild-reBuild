"""patchSmcConfig with all its hints off: only two cold traces are swapped (gpu's before cpu's)"""
import os
REMOVE = ['nei_smc', 'cb1', 'cb2', 'cb3', 'cb4']
FOCUS = ['_patchSmcConfig']
CPU = '''	if (xb.cpuFan != 0xffffffff) {
		if (iniRangeOk("cpufan", xb.cpuFan, 40, 100)) {
			smc[0x11] = xb.cpuFan | 0x80;
			patched = 1;
		} else if (xb.cpuFan)
			log_printf(0, "***** WARNING: cpu fan speed %d override ignored, not between 40 and 100\\n", xb.cpuFan);
		else if (smc[0x11] != 0x7f) {
			smc[0x11] = 0x7f;
			patched = 1;
		}
	}
'''
GPU = '''	if (xb.gpuFan != 0xffffffff) {
		if (iniRangeOk("gpufan", xb.gpuFan, 40, 100)) {
			smc[0x12] = xb.gpuFan | 0x80;
			patched = 1;
		} else if (xb.gpuFan)
			goto gpuwarn;
		else {
			smc[0x12] = 0x7f;
		}
	}
gpudone:
'''
TAIL = '''gpuwarn:
	log_printf(0, "***** WARNING: gpu fan speed override setting ignored, not between 40 and 100\\n");
	goto gpudone;
'''
W = 'log_printf(0, "***** WARNING: cpu fan speed %d override ignored, not between 40 and 100\\n", xb.cpuFan);'
C = [
    ('', []),
    ('cgoto_', [(CPU, CPU.replace('else if (xb.cpuFan)\n\t\t\t' + W, 'else if (xb.cpuFan)\n\t\t\tgoto cpuwarn;')
                .replace('''		}
	}
''', '''		}
	}
cpudone:
''')), (TAIL, 'cpuwarn:\n\t' + W + '\n\tgoto cpudone;\n' + TAIL)]),
    ('cnest', [(CPU, '''	if (xb.cpuFan != 0xffffffff) {
		if (iniRangeOk("cpufan", xb.cpuFan, 40, 100)) {
			smc[0x11] = xb.cpuFan | 0x80;
			patched = 1;
		} else {
			if (xb.cpuFan)
				''' + W + '''
			else {
				if (smc[0x11] != 0x7f) {
					smc[0x11] = 0x7f;
					patched = 1;
				}
			}
		}
	}
''')]),
    ('ceq', [(CPU, '''	if (xb.cpuFan != 0xffffffff) {
		if (iniRangeOk("cpufan", xb.cpuFan, 40, 100)) {
			smc[0x11] = xb.cpuFan | 0x80;
			patched = 1;
		} else if (!xb.cpuFan) {
			if (smc[0x11] != 0x7f) {
				smc[0x11] = 0x7f;
				patched = 1;
			}
		} else
			''' + W + '''
	}
''')]),
    ('cand', [(CPU, '''	if (xb.cpuFan != 0xffffffff) {
		if (iniRangeOk("cpufan", xb.cpuFan, 40, 100)) {
			smc[0x11] = xb.cpuFan | 0x80;
			patched = 1;
		} else if (xb.cpuFan)
			''' + W + '''
		else if (smc[0x11] != 0x7f) {
			patched = 1;
			smc[0x11] = 0x7f;
		}
	}
''')]),
    ('cmask', [(CPU, '''	if (xb.cpuFan != 0xffffffff) {
		if (iniRangeOk("cpufan", xb.cpuFan, 40, 100)) {
			patched = 1;
			smc[0x11] = xb.cpuFan | 0x80;
		} else if (xb.cpuFan)
			''' + W + '''
		else if (smc[0x11] != 0x7f) {
			smc[0x11] = 0x7f;
			patched = 1;
		}
	}
''')]),
]
G = [
    ('', []),
    ('gnest', [(GPU, '''	if (xb.gpuFan != 0xffffffff) {
		if (iniRangeOk("gpufan", xb.gpuFan, 40, 100)) {
			smc[0x12] = xb.gpuFan | 0x80;
			patched = 1;
		} else {
			if (xb.gpuFan)
				goto gpuwarn;
			smc[0x12] = 0x7f;
		}
	}
gpudone:
''')]),
    ('geq', [(GPU, '''	if (xb.gpuFan != 0xffffffff) {
		if (iniRangeOk("gpufan", xb.gpuFan, 40, 100)) {
			smc[0x12] = xb.gpuFan | 0x80;
			patched = 1;
		} else if (!xb.gpuFan) {
			smc[0x12] = 0x7f;
		} else
			goto gpuwarn;
	}
gpudone:
''')]),
    ('gout', [(GPU, '''	if (xb.gpuFan == 0xffffffff)
		goto gpudone;
	if (iniRangeOk("gpufan", xb.gpuFan, 40, 100)) {
		smc[0x12] = xb.gpuFan | 0x80;
		patched = 1;
	} else if (xb.gpuFan)
		goto gpuwarn;
	else {
		smc[0x12] = 0x7f;
	}
gpudone:
''')]),
]
AXES = [C, G]
