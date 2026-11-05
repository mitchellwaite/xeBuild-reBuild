"""extractSmcConfig: scan-loop forms with an explicit next, with the bound expects and the pin off in turn; second run, inside findSmcConfig."""
import itertools
LOOP1 = '''	for (i = 0; __builtin_expect(i + 0x200 <= size, 1); i += 0x200) {
		__asm__("" : : "S"(i + 0x200), "D"(buf));
		if ((found = smcConfigOk(buf + i)) == 1)
			break;
	}
'''
LOOP2 = '''		for (i = 0; __builtin_expect(i + 0x210 <= size, 1); i += 0x210)
			if ((found = smcConfigOk(buf + i)) == 1)
				break;
'''


def forms(step, ind, pin=False, exp=False):
    t = ind
    B = '(found = smcConfigOk(buf + i)) == 1'
    def cond(c):
        return '__builtin_expect(%s, 1)' % c if exp else c
    P = (t + '\t__asm__("" : : "S"(i + %s), "D"(buf));\n' % step) if pin else ''
    return {
        'for': t + 'for (i = 0; %s; i += %s) {\n' % (cond('i + %s <= size' % step), step) + P + t + '\tif (' + B + ')\n' + t + '\t\tbreak;\n' + t + '}\n',
        'next': t + 'for (i = 0; %s; i = next) {\n' % cond('(next = i + %s) <= size' % step) + P + t + '\tif (' + B + ')\n' + t + '\t\tbreak;\n' + t + '}\n',
        'next2': t + 'for (i = 0, next = %s; %s; i = next, next += %s) {\n' % (step, cond('next <= size'), step) + P + t + '\tif (' + B + ')\n' + t + '\t\tbreak;\n' + t + '}\n',
        'wh': t + 'i = 0;\n' + t + 'next = %s;\n' % step + t + 'while (%s) {\n' % cond('next <= size') + P + t + '\tif (' + B + ')\n' + t + '\t\tbreak;\n' + t + '\ti = next;\n' + t + '\tnext = i + %s;\n' % step + t + '}\n',
        'forever': t + 'i = 0;\n' + t + 'for (;;) {\n' + t + '\tnext = i + %s;\n' % step + t + '\tif (next > size)\n' + t + '\t\tbreak;\n' + P + t + '\tif (' + B + ')\n' + t + '\t\tbreak;\n' + t + '\ti = next;\n' + t + '}\n',
        'wh2': t + 'i = 0;\n' + t + 'while (%s) {\n' % cond('i + %s <= size' % step) + P + t + '\tfound = smcConfigOk(buf + i);\n' + t + '\tif (found == 1)\n' + t + '\t\tbreak;\n' + t + '\ti += %s;\n' % step + t + '}\n',
        'cont': t + 'for (i = 0; %s; i = next) {\n' % cond('(next = i + %s) <= size' % step) + P + t + '\tif (!(' + B + '))\n' + t + '\t\tcontinue;\n' + t + '\tbreak;\n' + t + '}\n',
        'contfor': t + 'for (i = 0; %s; i += %s) {\n' % (cond('i + %s <= size' % step), step) + P + t + '\tif ((found = smcConfigOk(buf + i)) != 1)\n' + t + '\t\tcontinue;\n' + t + '\tbreak;\n' + t + '}\n',
    }


def CASES(base):
    res = []
    OFFS = {'keep200': (True, True), 'off200': (False, False), 'pinonly': (False, True), 'exponly': (True, False)}
    for (lab, (pin, exp)), expb in itertools.product(OFFS.items(), (True, False)):
        f1 = forms('0x200', '\t', pin, exp)
        f2 = forms('0x210', '\t\t', False, expb)
        for a, b in itertools.product(f1, f2):
            def f(t, a=f1[a], b=f2[b]):
                t = t.replace(LOOP1, a).replace(LOOP2, b)
                return t.replace('	uint32_t i, j;\n	int found;\n', '	uint32_t i, j, next;\n	int found;\n')
            res.append(('%s,%s' % (lab, 'keep210' if expb else 'off210'), '%s/%s' % (a, b), f))
    return res
