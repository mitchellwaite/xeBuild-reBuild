"""parseOption's two expects: shapes of the setBoolOption test and of the unknown-option tail.
python opend.py [extra trick names]"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import optlib, optricks

SB = 'if (__builtin_expect(setBoolOption(opt, val) == 1, 0)) {'
SBV = {
    'exp': SB,
    'eq1': 'if (setBoolOption(opt, val) == 1) {',
    'nz': 'if (setBoolOption(opt, val)) {',
}
TAIL = '''		}
	}
	if (__builtin_expect(vlen, 0)) {
		log_printf(1, "\\n\\n***** ERROR: unknown option '%s' with value '%s' provided on the command line!\\n", opt, val);
		return 0;
	}
'''
UNK = '''log_printf(1, "\\n\\n***** ERROR: unknown option '%s' with value '%s' provided on the command line!\\n", opt, val);
'''
TV = {
    'exp': TAIL,
    'vlen': TAIL.replace('__builtin_expect(vlen, 0)', 'vlen'),
    'val': TAIL.replace('__builtin_expect(vlen, 0)', 'val'),
    'inval': '''		}
		log_printf(1, "\\n\\n***** ERROR: unknown option '%s' with value '%s' provided on the command line!\\n", opt, val);
		return 0;
	}
''',
    'inval_vlen': '''		}
		if (vlen) {
			log_printf(1, "\\n\\n***** ERROR: unknown option '%s' with value '%s' provided on the command line!\\n", opt, val);
			return 0;
		}
	}
''',
    'else': '''		}
	}
	if (vlen)
		log_printf(1, "\\n\\n***** ERROR: unknown option '%s' with value '%s' provided on the command line!\\n", opt, val);
	else
		log_printf(1, "\\n\\n***** ERROR: unknown or incomplete option '%s' provided on the command line!\\n", opt);
	return 0;
	log_printf(1, "\\n\\n***** ERROR: unknown or incomplete option '%s' provided on the command line!\\n", opt);
	return 0;
''',
}
INC = '''	log_printf(1, "\\n\\n***** ERROR: unknown or incomplete option '%s' provided on the command line!\\n", opt);
	return 0;
'''


def main():
    extra = sys.argv[1].split(',') if len(sys.argv) > 1 else []
    b, got = optricks.apply(optricks.base(), extra)
    for sn, s in SBV.items():
        for tn, t in TV.items():
            x = b.replace(SB, s).replace(TAIL, t)
            if tn == 'else':
                x = x.replace(t + INC, t[:t.rfind('\tlog_printf(1, "\\n\\n***** ERROR: unknown or incomplete')])
            r = optlib.score_text(x, optricks.flags_for(got))
            print('%-4s %-10s %s' % (sn, tn, optlib.fmt(r)[:120]), flush=True)


main()
