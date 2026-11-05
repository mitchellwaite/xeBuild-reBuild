"""patchSmcConfig without no-early-inlining: a fan section as its own static function, called once.  With calls inside it isn't early
inlined, so its branches are predicted on their own, and the cpu and gpu sections really differ."""
REMOVE = ['nei_smc']
FOCUS = ['_patchSmcConfig']
W = 'log_printf(0, "***** WARNING: cpu fan speed %d override ignored, not between 40 and 100\\n", xb.cpuFan);'
CPU = '''	if (xb.cpuFan != 0xffffffff) {
		if (iniRangeOk("cpufan", xb.cpuFan, 40, 100)) {
			setFan(smc + 0x11, xb.cpuFan | 0x80);
			patched = 1;
		} else if (xb.cpuFan)
			''' + W + '''
		else if (smc[0x11] != 0x7f) {
			setFan(smc + 0x11, 0x7f);
			patched = 1;
		}
	}
'''
GW = 'log_printf(0, "***** WARNING: gpu fan speed override setting ignored, not between 40 and 100\\n");'
GPU = '''	if (xb.gpuFan != 0xffffffff) {
		if (iniRangeOk("gpufan", xb.gpuFan, 40, 100)) {
			setFan(smc + 0x12, xb.gpuFan | 0x80);
			patched = 1;
		} else if (xb.gpuFan)
			goto gpuwarn;
		else {
			setFan(smc + 0x12, 0x7f);
		}
	}
gpudone:
'''
GWT = '''gpuwarn:
	''' + GW + '''
	goto gpudone;
'''
HEAD = '''uint32_t patchSmcConfig(uint8_t *smc)
{'''
ATTR = '__attribute__((optimize("no-early-inlining")))\n'
def body(sec):
    return sec
CF = {
    'r': ('static uint32_t patchCpuFan(uint8_t *smc, uint32_t patched)\n{\n' + CPU + '	return patched;\n}\n\n', '	patched = patchCpuFan(smc, patched);\n'),
    'b': ('static int patchCpuFan(uint8_t *smc)\n{\n	int patched = 0;\n\n' + CPU + '	return patched;\n}\n\n', '	if (patchCpuFan(smc))\n		patched = 1;\n'),
    'p': ('static void patchCpuFan(uint8_t *smc, uint32_t *ppatched)\n{\n' + CPU.replace('patched = 1', '*ppatched = 1') + '}\n\n', '	patchCpuFan(smc, &patched);\n'),
}
GS = GPU.replace('goto gpuwarn;', GW).replace('gpudone:\n', '')
GF = {
    'r': ('static uint32_t patchGpuFan(uint8_t *smc, uint32_t patched)\n{\n' + GS + '	return patched;\n}\n\n', '	patched = patchGpuFan(smc, patched);\n'),
    'b': ('static int patchGpuFan(uint8_t *smc)\n{\n	int patched = 0;\n\n' + GS + '	return patched;\n}\n\n', '	if (patchGpuFan(smc))\n		patched = 1;\n'),
    'p': ('static void patchGpuFan(uint8_t *smc, uint32_t *ppatched)\n{\n' + GS.replace('patched = 1', '*ppatched = 1') + '}\n\n', '	patchGpuFan(smc, &patched);\n'),
    'gt': ('static uint32_t patchGpuFan(uint8_t *smc, uint32_t patched)\n{\n' + GPU.replace('gpudone:\n', '	return patched;\ngpuwarn:\n	' + GW + '\n	return patched;\n') + '}\n\n', '	patched = patchGpuFan(smc, patched);\n'),
}
A = [('', [])] + [('c' + k, [(CPU, c), (HEAD, d + HEAD)]) for k, (d, c) in CF.items()]
B = [('', [])] + [('g' + k, [(GPU, c), (GWT, ''), (HEAD, d + HEAD)]) for k, (d, c) in GF.items()]
AXES = [A, B]
