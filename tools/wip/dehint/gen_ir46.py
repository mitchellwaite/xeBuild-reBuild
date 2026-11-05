"""detectController: pin_found / pin_lo with the b[513] byte kept in a local (the reference holds it in cl across the first sum and re-uses it in the
second test, so the author probably had a variable), and integer types of the sums.  IRA: r108 (found) l0 is the first potential spill, pri 83, cost 751."""
FOCUS = ['_detectController']
OLD = '''			int hi, lo;

			if (b[517] != 0xff || b[513] == 0xff)
				continue;
			hi = (b[514] & 0xf) * 256;
			lo = b[513];
			if (hi + lo == i) {
'''
OLD2 = '''				int lo2 = b[512];

				if (lo2 + (b[513] & 0xf) * 256 == i) {
					/* code-free: lo stays live over both tests: the
					   first sum takes hi's register (ebp), lo2 edx */
					__asm__("" : : "a"(lo));
'''
PF = '''		if (n > 1)
			__asm__("" : "+a"(found));
'''
SHAPES = {}
for ty in ('int', 'uint32_t'):
    SHAPES['k.' + ty] = ([(OLD, OLD.replace('int hi, lo', ty + ' hi, lo'))], 'lo', '(b[513] & 0xf) * 256')
    for mt in ('uint8_t', 'int', 'uint32_t'):
        for ord_ in ('a', 'b', 'c'):
            head = '''			%s hi, lo;
			%s m;

			if (b[517] != 0xff)
				continue;
			m = b[513];
			if (m == 0xff)
				continue;
''' % (ty, mt)
            if ord_ == 'a':
                body = 'hi = (b[514] & 0xf) * 256;\n lo = m;\n if (hi + lo == i) {\n'
            elif ord_ == 'b':
                body = 'lo = m;\n hi = (b[514] & 0xf) * 256;\n if (lo + hi == i) {\n'
            else:
                body = 'hi = (b[514] & 0xf) * 256;\n if (hi + m == i) {\n'
            SHAPES['m.%s.%s.%s' % (ty, mt, ord_)] = ([(OLD, head + body)], 'lo' if ord_ != 'c' else 'm', '(m & 0xf) * 256')
AX = []
for k, (ed, lovar, sec) in SHAPES.items():
    for pl in ('pk', 'p0'):
        e2 = '''				int lo2 = b[512];

				if (lo2 + %s == i) {
''' % sec
        if pl == 'pk':
            e2 += '					__asm__("" : : "a"(%s));\n' % lovar
        AX.append((k + '.' + pl, ed + [(OLD2, e2)]))
AXF = [('f0', [(PF, '')]), ('fk', [])]
AXES = [AX, AXF]
