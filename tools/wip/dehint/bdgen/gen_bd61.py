"""checkBl's cb_hint: PRED_CALL needs a call with side effects, so a getter (pure) does nothing.  A helper with an out parameter."""
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
SETFAN = '''/* one fan speed byte of the smc config */
static void setFan(uint8_t *p, uint8_t v)
{
	*p = v;
}

'''
BASE_E = [
    (ARM1, '			setFan(smc + 0x11, xb.cpuFan | 0x80);\n'),
    (ARM2, '			setFan(smc + 0x11, 0x7f);\n'),
    (ARM3, '			setFan(smc + 0x12, xb.gpuFan | 0x80);\n'),
    (ARM4, '			setFan(smc + 0x12, 0x7f);\n'),
    (CB, SETFAN),
    ('	uint32_t patched = 0;\n	int i, dead;\n', '	uint32_t patched = 0;\n	int i;\n'),
]
MM = '''	cb_hint(&dead);
	m = bl[0];
'''
HM = {
    'out': ('static void blMagic(const uint8_t *bl, int *m)\n{\n	*m = bl[0];\n}\n\n', 'blMagic(bl, &m);\n'),
    'outr': ('static int blMagic(const uint8_t *bl, int *m)\n{\n	*m = bl[0];\n	return *m;\n}\n\n', 'blMagic(bl, &m);\n'),
}
HEAD = '__attribute__((optimize("no-early-inlining")))\nint checkBl('
A2 = []
for k, (h, c) in HM.items():
    A2.append((k, BASE_E + [(MM, '\t' + c), ('	int m, dead;\n', '	int m;\n'), (HEAD, h + HEAD)]))
AXES = [A2]
