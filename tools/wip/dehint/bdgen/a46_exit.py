LOG = r'''			log_printf(0, "\n\n**** could not read %s (%i) ****\n\n", e->name, r);'''
T = '''		if (r) {
''' + LOG + '''
			return -1;
		}
	}
	return 0;
}'''
D = '''	struct fileent *e;
	uint32_t i;

	for (i = 1; i < (uint32_t)xb.nFiles; i++) {
		uint32_t r = 0;

		e = &xb.files[i];'''
D2 = '''	struct fileent *e;
	uint32_t i;
	uint32_t r = 0;

	for (i = 1; i < (uint32_t)xb.nFiles; i++) {
		r = 0;
		e = &xb.files[i];'''


def tail(body):
    return [(D, D2), (T, body)]


V = {
 'logbrk_rr': tail('''		if (r) {
''' + LOG + '''
			break;
		}
	}
	return r ? -1 : 0;
}'''),
 'logbrk_if': tail('''		if (r) {
''' + LOG + '''
			break;
		}
	}
	if (r)
		return -1;
	return 0;
}'''),
 'icount': tail('''		if (r) {
''' + LOG + '''
			i = xb.nFiles;
		}
	}
	if (r)
		return -1;
	return 0;
}'''),
 'icount_rr': tail('''		if (r) {
''' + LOG + '''
			i = xb.nFiles;
		}
	}
	return r ? -1 : 0;
}'''),
 'cond_r': [(D, D2.replace('for (i = 1; i < (uint32_t)xb.nFiles; i++) {\n\t\tr = 0;', 'for (i = 1; !r && i < (uint32_t)xb.nFiles; i++) {')),
            (T, '''		if (r)
''' + LOG[1:] + '''
	}
	if (r)
		return -1;
	return 0;
}''')],
}
