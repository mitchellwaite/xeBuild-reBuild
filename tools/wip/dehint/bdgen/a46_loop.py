LOG = r'''			log_printf(0, "\n\n**** could not read %s (%i) ****\n\n", e->name, r);'''
H = '''	for (i = 1; i < (uint32_t)xb.nFiles; i++) {
		uint32_t r = 0;

		e = &xb.files[i];
		if (strnicmp(e->name, "none", 4) || e->crc) {'''
T = '''		if (r) {
''' + LOG + '''
			return -1;
		}
	}
	return 0;
}'''
D = '''	struct fileent *e;
	uint32_t i;

	for (i = 1; i < (uint32_t)xb.nFiles; i++) {'''
V = {
 'brk': [(D, '''	struct fileent *e;
	uint32_t i;
	uint32_t r = 0;

	for (i = 1; i < (uint32_t)xb.nFiles; i++) {'''),
         ('''		uint32_t r = 0;

		e = &xb.files[i];''', '''		r = 0;
		e = &xb.files[i];'''),
         (T, '''		if (r)
			break;
	}
	if (r) {
''' + LOG[1:] + '''
		return -1;
	}
	return 0;
}''')],
 'while': [(H, H.replace('for (i = 1; i < (uint32_t)xb.nFiles; i++) {', 'i = 1;\n\twhile (i < (uint32_t)xb.nFiles) {')),
           (T, T.replace('''			return -1;
		}
	}''', '''			return -1;
		}
		i++;
	}'''))],
 'rne': [(T, T.replace('if (r) {', 'if (r != 0) {'))],
}
