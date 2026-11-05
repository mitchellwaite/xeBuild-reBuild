"""extractSmcConfig: the scan as a static function (calls inside, so predicted on its own and inlined at ipa-inline), bound expects off in turn."""
import itertools
OLD = '''	found = 0;
	for (i = 0; __builtin_expect(i + 0x200 <= size, 1); i += 0x200) {
		__asm__("" : : "S"(i + 0x200), "D"(buf));
		if ((found = smcConfigOk(buf + i)) == 1)
			break;
	}
	if (!found) {
		for (i = 0; __builtin_expect(i + 0x210 <= size, 1); i += 0x210)
			if ((found = smcConfigOk(buf + i)) == 1)
				break;
		if (!found)
			goto notfound;
	}
'''
HEAD = 'int extractSmcConfig(struct fileent *e, uint8_t *buf, int size)\n{'


def body(e1, e2, pin):
    b1 = '__builtin_expect(i + 0x200 <= size, 1)' if e1 else 'i + 0x200 <= size'
    b2 = '__builtin_expect(i + 0x210 <= size, 1)' if e2 else 'i + 0x210 <= size'
    p = '		__asm__("" : : "S"(i + 0x200), "D"(buf));\n' if pin else ''
    return b1, b2, p


def forms(e1, e2, pin):
    b1, b2, p = body(e1, e2, pin)
    return {
        'ptr': ('''static int findSmcConfig(uint8_t *buf, int size, uint32_t *pos)
{
	uint32_t i;
	int found = 0;

	for (i = 0; %s; i += 0x200) {
%s		if ((found = smcConfigOk(buf + i)) == 1)
			break;
	}
	if (!found) {
		for (i = 0; %s; i += 0x210)
			if ((found = smcConfigOk(buf + i)) == 1)
				break;
	}
	*pos = i;
	return found;
}

''' % (b1, p, b2), '''	found = findSmcConfig(buf, size, &i);
	if (!found)
		goto notfound;
'''),
        'ptr2': ('''static int findSmcConfig(uint8_t *buf, int size, uint32_t *pos)
{
	uint32_t i;

	for (i = 0; %s; i += 0x200) {
%s		if (smcConfigOk(buf + i) == 1) {
			*pos = i;
			return 1;
		}
	}
	for (i = 0; %s; i += 0x210)
		if (smcConfigOk(buf + i) == 1) {
			*pos = i;
			return 1;
		}
	return 0;
}

''' % (b1, p, b2), '''	found = findSmcConfig(buf, size, &i);
	if (!found)
		goto notfound;
'''),
    }


def CASES(base):
    out = []
    for e1, e2, pin, nf in itertools.product((1, 0), (1, 0), (1, 0), (1, 0)):
        for k in ('ptr', 'ptr2'):
            d, c = forms(e1, e2, pin)[k]

            def f(t, d=d, c=c, nf=nf):
                t = t.replace(OLD, c).replace(HEAD, d + HEAD)
                if not nf:
                    t = t.replace('notfound: __attribute__((hot));\nnotfound2: __attribute__((hot));\n', 'notfound:\n')
                return t
            out.append(('', '%s e200=%d e210=%d pin=%d nf=%d' % (k, e1, e2, pin, nf), f))
    return out
