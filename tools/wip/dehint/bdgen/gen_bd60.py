"""cb_hint is a call that survives to profile_estimate under no-early-inlining (PRED_CALL on its edge).  A real helper doing the
arm's work is the same call: fan-byte setter in patchSmcConfig, magic byte reader in checkBl."""
CB = '''static void cb_hint(int *p)
{
	*p = 1;
}

'''
ARM1 = '''			cb_hint(&dead);
			smc[0x11] = xb.cpuFan | 0x80;
'''
ARM2 = '''			cb_hint(&dead);
			smc[0x11] = 0x7f;
'''
ARM3 = '''			cb_hint(&dead);
			smc[0x12] = xb.gpuFan | 0x80;
'''
ARM4 = '''			cb_hint(&dead);
			smc[0x12] = 0x7f;
'''
HS = {
    'p': ('''static void setFan(uint8_t *p, uint32_t v)
{
	*p = v;
}

''', 'setFan(smc + 0x%x, %s);'),
    'o': ('''static void setFan(uint8_t *smc, int off, uint32_t v)
{
	smc[off] = v;
}

''', 'setFan(smc, 0x%x, %s);'),
    'pu8': ('''static void setFan(uint8_t *p, uint8_t v)
{
	*p = v;
}

''', 'setFan(smc + 0x%x, %s);'),
}
A1 = []
for k, (h, c) in HS.items():
    A1.append((k, [
        (ARM1, '\t\t\t' + c % (0x11, 'xb.cpuFan | 0x80') + '\n'),
        (ARM2, '\t\t\t' + c % (0x11, '0x7f') + '\n'),
        (ARM3, '\t\t\t' + c % (0x12, 'xb.gpuFan | 0x80') + '\n'),
        (ARM4, '\t\t\t' + c % (0x12, '0x7f') + '\n'),
        (CB, h),
        ('	uint32_t patched = 0;\n	int i, dead;\n', '	uint32_t patched = 0;\n	int i;\n'),
    ]))
MM = '''	cb_hint(&dead);
	m = bl[0];
'''
HM = {
    'gi': ('static int blMagic(const uint8_t *bl)\n{\n	return bl[0];\n}\n\n', 'm = blMagic(bl);\n'),
    'gu': ('static uint8_t blMagic(const uint8_t *bl)\n{\n	return bl[0];\n}\n\n', 'm = blMagic(bl);\n'),
}
HEAD = '__attribute__((optimize("no-early-inlining")))\nint checkBl('
A2 = [('', [('	int m, dead;\n', '	int m, dead;\n')])]
for k, (h, c) in HM.items():
    A2.append((k, [(MM, '\t' + c), ('	int m, dead;\n', '	int m;\n'), (HEAD, h + HEAD)]))
AXES = [A1, A2]
