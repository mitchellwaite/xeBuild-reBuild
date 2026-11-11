# oprv.py variants, second round: structural respellings of parseOption's borderline slots
# (against 98a0eba6's src/options.c).  Combine with +.
import os

exec(open(os.path.join(os.path.dirname(__file__), 'oprv_a.py')).read())

TAIL_OLD = '''			xb.bootFlags |= 0x2000000;
			return 1;
		}
	}
	if (ok)
		return 1;
	if (val && vlen) {
		log_printf(1, "\\n\\n***** ERROR: unknown option '%s' with value '%s' provided on the command line!\\n", opt, val);
		return 0;
	}
	log_printf(1, "\\n\\n***** ERROR: unknown or incomplete option '%s' provided on the command line!\\n", opt);
	return 0;
'''
UNK = 'log_printf(1, "\\n\\n***** ERROR: unknown option \'%s\' with value \'%s\' provided on the command line!\\n", opt, val);'
INC = 'log_printf(1, "\\n\\n***** ERROR: unknown or incomplete option \'%s\' provided on the command line!\\n", opt);'


def tail(body):
    return [(TAIL_OLD, '''			xb.bootFlags |= 0x2000000;
			return 1;
		}
''' + body)]


V += [
    # the with-value message inside the val block: no redundant test
    ('d4', tail('''		if (vlen) {
			%s
			return 0;
		}
	}
	if (ok)
		return 1;
	%s
	return 0;
''' % (UNK, INC))),
    ('d4p', tail('''		if (vlen > 0) {
			%s
			return 0;
		}
	}
	if (ok)
		return 1;
	%s
	return 0;
''' % (UNK, INC))),
    # nested ifs for the same test (the author's habit)
    ('d7', tail('''	}
	if (ok)
		return 1;
	if (val) {
		if (vlen) {
			%s
			return 0;
		}
	}
	%s
	return 0;
''' % (UNK, INC))),
    ('d3', [('\tif (val && vlen) {\n', '\tif (vlen && val) {\n')]),
    # one return for both messages
    ('d6', tail('''	}
	if (ok)
		return 1;
	if (vlen)
		%s
	else
		%s
	return 0;
''' % (UNK, INC))),
    # the bool arm returns; the value block ends in the with-value message
    ('b4', [(BOOL_OLD, '''	if (setBoolOption(opt, val) == 1) {
		log_printf(1, "\\n");
		return 1;
	}
	if (val) {
''')] + tail('''		if (vlen) {
			%s
			return 0;
		}
	}
	%s
	return 0;
''' % (UNK, INC))),
    # ok as the bool result, tested again after the value options (attempt 22's c2)
    ('b5', [(BOOL_OLD, '''	ok = setBoolOption(opt, val) == 1;
	if (ok)
		log_printf(1, "\\n");
	else if (val) {
''')]),
    ('b5d4', [(BOOL_OLD, '''	ok = setBoolOption(opt, val) == 1;
	if (ok)
		log_printf(1, "\\n");
	else if (val) {
''')] + tail('''		if (vlen) {
			%s
			return 0;
		}
	}
	if (ok)
		return 1;
	%s
	return 0;
''' % (UNK, INC))),
    # the success at the end, the messages inside the not-bool arm
    ('b6', [(BOOL_OLD, '''	if (setBoolOption(opt, val) != 1) {
		if (val) {
''')] + tail('''		}
		if (val && vlen) {
			%s
			return 0;
		}
		%s
		return 0;
	}
	log_printf(1, "\\n");
	return 1;
''' % (UNK, INC))),
]
