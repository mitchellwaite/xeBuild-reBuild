"""checkBl: -3 must not be a constant argument of the return PHI at profile_estimate, or
PRED_NEGATIVE_RETURN puts the size error at 1.7%: reach the return through a test on a value"""
REMOVE = ['lit_chk', 'lab_size']
FOCUS = ['_checkBl']
SZ = 'log_printf(0, "\\n\\n***** ERROR: BL size (0x%x) is bigger than the file (0x%x) read in!\\n", blsize, size);'
BAD = 'log_printf(0, "\\n\\n***** ERROR: BL crc check failed! calculated: %08x expected: %08x\\n", c, crc);'
MAG = 'log_printf(0, "\\n\\n***** ERROR: BL magic check %c%c for type %d failed!\\n", bl[0], bl[1], type);'
H = '''	if (blsize > size) {
		''' + SZ + '''
		return -3;
	}
	cb_hint(&dead);
	m = bl[0];
'''
T = '''	return 0;
bad:
	''' + BAD + '''
	return -2;
magic:
	''' + MAG + '''
	return -1;
}
'''
DECL = ('int m, dead;', 'int m, dead, r;')
TG = '''	return 0;
bad:
	''' + BAD + '''
	return -2;
toobig:
	''' + SZ + '''
	r = -3;
	goto chk;
magic:
	''' + MAG + '''
	return -1;
}
'''
TF = T
shapes = []
for cb in (0, 1):
    C = '\tcb_hint(&dead);\n' if cb else ''
    tag = '+cb' if cb else ''
    shapes += [
        ('flag' + tag, [DECL, (H, '''	r = 0;
	if (blsize > size) {
		''' + SZ + '''
		r = -3;
	}
	if (r)
		return r;
''' + C + '''	m = bl[0];
''')]),
        ('flagnz' + tag, [DECL, (H, '''	r = 0;
	if (blsize > size) {
		''' + SZ + '''
		r = -3;
	}
	if (r != 0)
		return r;
''' + C + '''	m = bl[0];
''')]),
        ('flaglt' + tag, [DECL, (H, '''	r = 0;
	if (blsize > size) {
		''' + SZ + '''
		r = -3;
	}
	if (r < 0)
		return r;
''' + C + '''	m = bl[0];
''')]),
        ('flagelse' + tag, [DECL, (H, '''	if (blsize > size) {
		''' + SZ + '''
		r = -3;
	} else
		r = 0;
	if (r)
		return r;
''' + C + '''	m = bl[0];
''')]),
        ('flagret' + tag, [DECL, (H, '''	r = 0;
	if (blsize > size) {
		''' + SZ + '''
		r = -3;
	}
	if (r)
		goto out;
''' + C + '''	m = bl[0];
'''), (T, '''	return 0;
bad:
	''' + BAD + '''
	return -2;
magic:
	''' + MAG + '''
	return -1;
out:
	return r;
}
''')]),
    ]
AXES = [shapes, [
    ('', []),
    ('nocrc', [('__builtin_expect(crc != c, 0)', 'crc != c')]),
]]
