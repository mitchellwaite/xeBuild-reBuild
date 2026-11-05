"""patchSmcConfig landing: no no-early-inlining, cpu section in patchCpuFan (ret3), setFan written back as plain stores, caller's guard nested."""
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
HEAD = '''uint32_t patchSmcConfig(uint8_t *smc)
{'''
FN = '''/* the cpu fan setting; returns 1 if it changed the config */
static int patchCpuFan(uint8_t *smc)
{
	if (xb.cpuFan != 0xffffffff) {
		if (iniRangeOk("cpufan", xb.cpuFan, 40, 100)) {
			smc[0x11] = xb.cpuFan | 0x80;
			return 1;
		}
		if (xb.cpuFan)
			''' + W + '''
		else if (smc[0x11] != 0x7f) {
			smc[0x11] = 0x7f;
			return 1;
		}
	}
	return 0;
}

'''
SETFAN = '''/* one fan speed byte of the smc config */
static void setFan(uint8_t *p, uint8_t v)
{
	*p = v;
}

'''
CALL = {
    'and': '	if (xb.cpuFan != 0xffffffff && patchCpuFan(smc))\n		patched = 1;\n',
    'nest': '	if (xb.cpuFan != 0xffffffff) {\n		if (patchCpuFan(smc))\n			patched = 1;\n	}\n',
}
A = [(k, [(CPU, v), (HEAD, FN + HEAD)]) for k, v in CALL.items()]
B = [
    ('keep', []),
    ('plain', [('			setFan(smc + 0x12, xb.gpuFan | 0x80);\n', '			smc[0x12] = xb.gpuFan | 0x80;\n'),
               ('			setFan(smc + 0x12, 0x7f);\n', '			smc[0x12] = 0x7f;\n'),
               (SETFAN, '')]),
]
AXES = [A, B]
