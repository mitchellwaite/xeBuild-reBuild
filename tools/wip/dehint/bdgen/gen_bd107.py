"""loadBl with vol_fail off: what the shared `fail` block is.  Each of its three sources goes to the label, or writes -1 itself and breaks or returns; the label block sits after the switch,
or at the first source's arm, or the -1 store goes in a helper."""
import itertools

C23 = '''			log_printf(1, "\\n\\n***** ERROR: patch size 0x%x is not a multiple of 4!\\n", e->size);
			goto fail;
'''
C2 = '''		if (!e->offset)
			goto fail;
		break;
'''
T = '''			if (__builtin_expect(*pr != 0, 0))
				goto fail;
			break;
'''
END = '''	return;
	/* one -1 block for the patch size, SMC and (xb.type <= BUILD_DEVGL16) signature
	   failures: the asm keeps it a block of its own (else the -1 is appended
	   to the size log, which crossjump can't then share) */
fail:
	__asm__ __volatile__("");
	*pr = -1;
}
'''
LOG = '			log_printf(1, "\\n\\n***** ERROR: patch size 0x%x is not a multiple of 4!\\n", e->size);\n'


def CASES(base):
    out = []
    forms = ('goto', 'brk', 'ret')
    for a, b, c, tl in itertools.product(forms, forms, forms, ('ret', 'last')):
        t = base
        n = 0
        if a == 'goto':
            n += 1
        else:
            t = t.replace(C23, LOG + '			*pr = -1;\n			' + ('break' if a == 'brk' else 'return') + ';\n')
        if b == 'goto':
            n += 1
        else:
            t = t.replace(C2, '		if (!e->offset)\n			*pr = -1;\n		break;\n' if b == 'brk' else '		if (!e->offset) {\n			*pr = -1;\n			return;\n		}\n		break;\n')
        if c == 'goto':
            n += 1
        else:
            t = t.replace(T, '			if (__builtin_expect(*pr != 0, 0))\n				*pr = -1;\n			break;\n' if c == 'brk' else '			if (__builtin_expect(*pr != 0, 0)) {\n				*pr = -1;\n				return;\n			}\n			break;\n')
        if n == 0:
            e2 = '	return;\n}\n'
        elif tl == 'ret':
            e2 = '	return;\nfail:\n	*pr = -1;\n}\n'
        else:
            e2 = '	if (0) {\nfail:\n		*pr = -1;\n	}\n}\n'
        t = t.replace(END, e2)
        out.append(('%s %s %s %s' % (a, b, c, tl), t))
    return out
