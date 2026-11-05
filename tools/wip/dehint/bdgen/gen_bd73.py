"""patchSmcConfig without no-early-inlining, cpu fan section as a helper (gen_bd72 cr, 8 loose lines): its success edge is 693, it must be at
most gpu's 571 (bb-reorder's key is 100 x that edge's frequency + the block's).  Forms of the helper with returns in the arms."""
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
SET1 = 'setFan(smc + 0x11, xb.cpuFan | 0x80);'
SET0 = 'setFan(smc + 0x11, 0x7f);'
RNG = 'iniRangeOk("cpufan", xb.cpuFan, 40, 100)'
H = {
    # returns 1 if it changed the config
    'ret1': '''	if (xb.cpuFan == 0xffffffff)
		return 0;
	if (%s) {
		%s
		return 1;
	}
	if (xb.cpuFan) {
		%s
		return 0;
	}
	if (smc[0x11] != 0x7f) {
		%s
		return 1;
	}
	return 0;
''' % (RNG, SET1, W, SET0),
    'ret2': '''	if (xb.cpuFan != 0xffffffff) {
		if (%s) {
			%s
			return 1;
		}
		if (xb.cpuFan)
			%s
		else if (smc[0x11] != 0x7f) {
			%s
			return 1;
		}
	}
	return 0;
''' % (RNG, SET1, W, SET0),
    'ret3': '''	if (xb.cpuFan != 0xffffffff) {
		if (%s) {
			%s
			return 1;
		} else if (xb.cpuFan)
			%s
		else if (smc[0x11] != 0x7f) {
			%s
			return 1;
		}
	}
	return 0;
''' % (RNG, SET1, W, SET0),
    'neg': '''	if (xb.cpuFan != 0xffffffff) {
		if (!%s) {
			if (xb.cpuFan) {
				%s
				return 0;
			}
			if (smc[0x11] == 0x7f)
				return 0;
			%s
			return 1;
		}
		%s
		return 1;
	}
	return 0;
''' % (RNG, W, SET0, SET1),
}
CALLS = {
    'if': '	if (patchCpuFan(smc))\n		patched = 1;\n',
    'or': '	patched |= patchCpuFan(smc);\n',
    'ifg': '	if (xb.cpuFan != 0xffffffff && patchCpuFan(smc))\n		patched = 1;\n',
}
A = []
for k, b in H.items():
    for c, cv in CALLS.items():
        for ty in ('int', 'uint32_t'):
            A.append(('%s-%s-%s' % (k, c, ty), [(CPU, cv), (HEAD, 'static %s patchCpuFan(uint8_t *smc)\n{\n' % ty + b + '}\n\n' + HEAD)]))
AXES = [A]
