"""patchCpuFan's repeated test: only in the caller, or only in the function."""
CALL = '''	if (xb.cpuFan != 0xffffffff) {
		if (patchCpuFan(smc))
			patched = 1;
	}
'''
FN = '''	if (xb.cpuFan != 0xffffffff) {
		if (iniRangeOk("cpufan", xb.cpuFan, 40, 100)) {
			smc[0x11] = xb.cpuFan | 0x80;
			return 1;
		}
		if (xb.cpuFan)
			log_printf(0, "***** WARNING: cpu fan speed %d override ignored, not between 40 and 100\n", xb.cpuFan);
		else if (smc[0x11] != 0x7f) {
			smc[0x11] = 0x7f;
			return 1;
		}
	}
	return 0;
'''
FN2 = '''	if (iniRangeOk("cpufan", xb.cpuFan, 40, 100)) {
		smc[0x11] = xb.cpuFan | 0x80;
		return 1;
	}
	if (xb.cpuFan)
		log_printf(0, "***** WARNING: cpu fan speed %d override ignored, not between 40 and 100\n", xb.cpuFan);
	else if (smc[0x11] != 0x7f) {
		smc[0x11] = 0x7f;
		return 1;
	}
	return 0;
'''
FN3 = '''	if (xb.cpuFan == 0xffffffff)
		return 0;
''' + FN2
def CASES(base):
    return [
      ('caller only', base.replace(FN, FN2)),
      ('fn only', base.replace(CALL, '	if (patchCpuFan(smc))\n		patched = 1;\n')),
      ('fn early', base.replace(CALL, '	if (patchCpuFan(smc))\n		patched = 1;\n').replace(FN, FN3)),
      ('both early', base.replace(FN, FN3)),
    ]
