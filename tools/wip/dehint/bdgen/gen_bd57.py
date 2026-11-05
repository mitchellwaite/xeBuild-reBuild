"""patchSmcConfig, all five off: the cpu and gpu log blocks tie at 348 and cpu comes first.  Make the gpu section really differ:
a goto over it (PRED_GOTO raises the whole section), other arms as gotos."""
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
GPU_ARMS = '''		if (iniRangeOk("gpufan", xb.gpuFan, 40, 100)) {
			smc[0x12] = xb.gpuFan | 0x80;
			patched = 1;
		} else if (xb.gpuFan)
			goto gpuwarn;
		else {
			smc[0x12] = 0x7f;
		}
'''
G = {
    'base': GPU,
    'skip': '''	if (xb.gpuFan == 0xffffffff)
		goto gpudone;
''' + GPU_ARMS.replace('\t\t', '\t', 1) + 'gpudone:\n',
    'okgoto': '''	if (xb.gpuFan != 0xffffffff) {
		if (!iniRangeOk("gpufan", xb.gpuFan, 40, 100)) {
			if (xb.gpuFan)
				goto gpuwarn;
			smc[0x12] = 0x7f;
		} else {
			smc[0x12] = xb.gpuFan | 0x80;
			patched = 1;
		}
	}
gpudone:
''',
    'okgoto2': '''	if (xb.gpuFan == 0xffffffff)
		goto gpudone;
	if (!iniRangeOk("gpufan", xb.gpuFan, 40, 100)) {
		if (xb.gpuFan)
			goto gpuwarn;
		smc[0x12] = 0x7f;
	} else {
		smc[0x12] = xb.gpuFan | 0x80;
		patched = 1;
	}
gpudone:
''',
    'okearly': '''	if (xb.gpuFan == 0xffffffff)
		goto gpudone;
	if (iniRangeOk("gpufan", xb.gpuFan, 40, 100)) {
		smc[0x12] = xb.gpuFan | 0x80;
		patched = 1;
		goto gpudone;
	}
	if (xb.gpuFan)
		goto gpuwarn;
	smc[0x12] = 0x7f;
gpudone:
''',
    'zero': '''	if (xb.gpuFan != 0xffffffff) {
		if (iniRangeOk("gpufan", xb.gpuFan, 40, 100)) {
			smc[0x12] = xb.gpuFan | 0x80;
			patched = 1;
		} else if (!xb.gpuFan)
			smc[0x12] = 0x7f;
		else
			goto gpuwarn;
	}
gpudone:
''',
    'zeroskip': '''	if (xb.gpuFan == 0xffffffff)
		goto gpudone;
	if (iniRangeOk("gpufan", xb.gpuFan, 40, 100)) {
		smc[0x12] = xb.gpuFan | 0x80;
		patched = 1;
	} else if (!xb.gpuFan)
		smc[0x12] = 0x7f;
	else
		goto gpuwarn;
gpudone:
''',
}
C = {
    'base': CPU,
    'skip': '''	if (xb.cpuFan == 0xffffffff)
		goto cpudone;
	if (iniRangeOk("cpufan", xb.cpuFan, 40, 100)) {
		smc[0x11] = xb.cpuFan | 0x80;
		patched = 1;
	} else if (xb.cpuFan)
		log_printf(0, "***** WARNING: cpu fan speed %d override ignored, not between 40 and 100\\n", xb.cpuFan);
	else if (smc[0x11] != 0x7f) {
		smc[0x11] = 0x7f;
		patched = 1;
	}
cpudone:
''',
}
AXES = [[('g' + k, [(GPU, v)]) for k, v in G.items()], [('c' + k, [(CPU, v)]) for k, v in C.items()]]
