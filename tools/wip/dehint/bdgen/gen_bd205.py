"""Attempt 9: findSmcConfig's scan loops with the found test in the loop condition (the forms attempt 3's
gen_bd59 and gen_bd83 didn't have), with the bound expects and the pin off or on.  smcConfigOk returns 0 or 1,
and the reference compares with 1 (`cmp eax,1`), so the forms keep `== 1` / `!= 1`.  Runs on src/build.c."""
import itertools

OLD = '''	for (i = 0; __builtin_expect(i + 0x200 <= size, 1); i += 0x200) {
		__asm__("" : : "S"(i + 0x200), "D"(buf));
		if ((found = smcConfigOk(buf + i)) == 1)
			break;
	}
	if (!found) {
		for (i = 0; __builtin_expect(i + 0x210 <= size, 1); i += 0x210)
			if ((found = smcConfigOk(buf + i)) == 1)
				break;
	}
'''
FORMS = {
    'brk': '''for (i = 0; @BND@(i + @N@ <= size); i += @N@) {
@PIN@		if ((found = smcConfigOk(buf + i)) == 1)
			break;
	}
''',
    'cond': '''for (i = 0; @BND@(i + @N@ <= size) && (found = smcConfigOk(buf + i)) != 1; i += @N@)
		;
''',
    'while': '''i = 0;
	while (@BND@(i + @N@ <= size) && (found = smcConfigOk(buf + i)) != 1)
		i += @N@;
''',
    'while2': '''i = 0;
	while (@BND@(i + @N@ <= size)) {
@PIN@		found = smcConfigOk(buf + i);
		if (found == 1)
			break;
		i += @N@;
	}
''',
    'for2': '''for (i = 0; @BND@(i + @N@ <= size); i += @N@) {
@PIN@		found = smcConfigOk(buf + i);
		if (found == 1)
			break;
	}
''',
}
GUARD = {'nf': 'if (!found) {\n\tLOOP2}\n', 'ne1': 'if (found != 1) {\n\tLOOP2}\n'}


def make(base, f1, f2, guard, e1, e2, pin):
    def loop(f, n, e):
        t = FORMS[f].replace('@N@', n).replace('@BND@', '__builtin_expect' if e else '')
        if e:
            t = t.replace('__builtin_expect(i + %s <= size)' % n, '__builtin_expect(i + %s <= size, 1)' % n)
        return t
    l1 = loop(f1, '0x200', e1).replace('@PIN@', '\t\t__asm__("" : : "S"(i + 0x200), "D"(buf));\n' if pin else '')
    if pin and '@PIN@' not in FORMS[f1]:
        return None
    l2 = loop(f2, '0x210', e2).replace('@PIN@', '')
    new = '\t' + l1 + '\t' + GUARD[guard].replace('LOOP2', l2)
    if OLD not in base:
        raise ValueError('findSmcConfig text not found')
    return base.replace(OLD, new)


def CASES(base):
    out = []
    for f1, f2, guard, e1, e2, pin in itertools.product(FORMS, FORMS, GUARD, [0, 1], [0, 1], [0, 1]):
        if f1 != f2 and (e1 or e2 or pin):
            continue
        lab = '%s %s %s e%d%d p%d' % (f1, f2, guard, e1, e2, pin)
        out.append((lab, lambda b, a=(f1, f2, guard, e1, e2, pin): make(b, *a)))
    return out


FOCUS = ['_extractSmcConfig']
