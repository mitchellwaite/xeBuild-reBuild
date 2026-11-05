"""extractSmcConfig: each scan loop predicted on its own, by one helper with a step or by two; no bound expects, no pin."""
A0 = '''static int findSmcConfig(uint8_t *buf, int size, uint32_t *pos)
{
	uint32_t i;
	int found = 0;

	for (i = 0; __builtin_expect(i + 0x200 <= size, 1); i += 0x200) {
		__asm__("" : : "S"(i + 0x200), "D"(buf));
		if ((found = smcConfigOk(buf + i)) == 1)
			break;
	}
	if (!found) {
		for (i = 0; __builtin_expect(i + 0x210 <= size, 1); i += 0x210)
			if ((found = smcConfigOk(buf + i)) == 1)
				break;
	}
	*pos = i;
	return found;
}

'''
CALL = '''	found = findSmcConfig(buf, size, &i);
	if (!found)
		goto notfound;
'''
STEP = '''static int scanSmcConfig(uint8_t *buf, int size, uint32_t step, uint32_t *pos)
{
	uint32_t i;
	int found = 0;

	for (i = 0; i + step <= size; i += step)
		if ((found = smcConfigOk(buf + i)) == 1)
			break;
	*pos = i;
	return found;
}

'''
STEP2 = STEP.replace('''	*pos = i;
	return found;
''', '''	*pos = i;
	return found == 1;
''')
RET = '''static int scanSmcConfig(uint8_t *buf, int size, uint32_t step, uint32_t *pos)
{
	uint32_t i;

	for (i = 0; i + step <= size; i += step)
		if (smcConfigOk(buf + i) == 1) {
			*pos = i;
			return 1;
		}
	return 0;
}

'''
TWO = (STEP.replace('scanSmcConfig', 'scanSmcEcc').replace(', uint32_t step', '').replace('step', '0x210') +
       STEP.replace('scanSmcConfig', 'scanSmcPlain').replace(', uint32_t step', '').replace('step', '0x200'))
C1 = '''	found = scanSmcConfig(buf, size, 0x200, &i);
	if (!found) {
		found = scanSmcConfig(buf, size, 0x210, &i);
		if (!found)
			goto notfound;
	}
'''
C2 = '''	if (!scanSmcConfig(buf, size, 0x200, &i) && !scanSmcConfig(buf, size, 0x210, &i))
		goto notfound;
'''
C3 = '''	found = scanSmcPlain(buf, size, &i);
	if (!found) {
		found = scanSmcEcc(buf, size, &i);
		if (!found)
			goto notfound;
	}
'''
AXES = [[
    ('step-c1', [(A0, STEP), (CALL, C1)]),
    ('step-c2', [(A0, STEP), (CALL, C2)]),
    ('step2-c1', [(A0, STEP2), (CALL, C1)]),
    ('ret-c1', [(A0, RET), (CALL, C1)]),
    ('ret-c2', [(A0, RET), (CALL, C2)]),
    ('two', [(A0, TWO), (CALL, C3)]),
]]
FOCUS = ['_extractSmcConfig']
