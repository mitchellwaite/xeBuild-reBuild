# attempt 2, on drafts/image_write.c: hot label lnp2 replaced by a dead test (add2 moved into the arms), other predictors
BASE = 'tools/wip/dehint/drafts/image_write.c'
A2 = '		if (x > first + 0x4000)\n			__asm__("");\n'
LNP = '''		if (!partial)
			npages = 32;
		else {
			/* imgAddFile's clone: keeps DOM2's threading from zeroing the npages guard edge */
			lnp2: __attribute__((hot));
		}
'''
c = 'x > first + 0x4000'
V = [('', [])]
for bn, body in (('e', '__asm__("")'), ('b', 'blocks++'), ('a', 'abort()'), ('o', 'off++')):
    if bn == 'o':
        pass
    d = '			if (%s)\n				%s;\n' % (c, body)
    V.append(('else' + bn, [(A2, ''), (LNP, '		if (!partial)\n			npages = 32;\n		else {\n' + d + '		}\n')]))
    V.append(('then' + bn, [(A2, ''), (LNP, '		if (!partial) {\n			npages = 32;\n' + d + '		}\n')]))
    V.append(('then2' + bn, [(A2, ''), (LNP, '		if (!partial) {\n' + d + '			npages = 32;\n		}\n')]))
    V.append(('pos' + bn, [(A2, ''), (LNP, '		if (partial) {\n' + d + '		} else\n			npages = 32;\n')]))
    V.append(('keep2then' + bn, [(LNP, '		if (!partial) {\n			npages = 32;\n' + d + '		}\n')]))
    V.append(('keep2else' + bn, [(LNP, '		if (!partial)\n			npages = 32;\n		else {\n' + d + '		}\n')]))
V.append(('plain', [(LNP, '		if (!partial)\n			npages = 32;\n')]))
V.append(('plainpos', [(LNP, '		if (partial) {\n		} else\n			npages = 32;\n')]))
AXES = [V]
