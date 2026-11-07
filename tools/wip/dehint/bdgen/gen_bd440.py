"""Attempt 32: lab_none (loadConsoleBlFiles' cold label and its `nFiles <= 1` precheck) by the loop's exit count.
The not-entered return's frequency is the loop's PRED_LOOP_EXIT share (9% / n_exits); the console's -1 errors
jumping straight to a could-not-read label after the loop add exits at profile_estimate (vrp1 would thread the
`r = -1; break; if (r)` path there anyway).  Subsets of the -1 sites as `r = -1; goto bad;`, with and without the
precheck and label.  Runs on src as of ccf9746b."""
import itertools, os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bdrun

FOCUS = ['_loadConsoleBlFiles']
FN = 'int loadConsoleBlFiles(void)\n'

PRE_OLD = '''	if ((uint32_t)xb.nFiles <= 1)
		goto none;
	for (i = 1;'''
TAIL_OLD = '''		if (r) {
			log_printf(0, "\\n\\n**** could not read %s (%i) ****\\n\\n", e->name, r);
			return -1;
		}
	}
	return 0;
none: __attribute__((cold));
	return 0;
}'''

SITES = {
    'kv': ('''					log_printf(0, "\\n***** ERROR!: acquiring keyvault data failed!\\n");
					r = -1;
				}
				break;
			case 4:''', '''					log_printf(0, "\\n***** ERROR!: acquiring keyvault data failed!\\n");
					r = -1;
					goto bad;
				}
				break;
			case 4:'''),
    'kva': ('''					log_printf(0, "\\n***** ERROR!: acquiring keyvault data failed!\\n");
					r = -1;
				}
				break;
			case 23:''', '''					log_printf(0, "\\n***** ERROR!: acquiring keyvault data failed!\\n");
					r = -1;
					goto bad;
				}
				break;
			case 23:'''),
    'sz': ('''					r = -1;
					break;
				}
				appendAddonPatches(e);''', '''					r = -1;
					goto bad;
				}
				appendAddonPatches(e);'''),
    'cfg': ('''					log_printf(0, "\\n***** ERROR!: acquiring smc configuration data failed!\\n");
					r = -1;''', '''					log_printf(0, "\\n***** ERROR!: acquiring smc configuration data failed!\\n");
					r = -1;
					goto bad;'''),
    'ld': ('''					if (!e->offset)
						r = -1;''', '''					if (!e->offset) {
						r = -1;
						goto bad;
					}'''),
    'smc': ('''					log_printf(0, "\\n***** ERROR!: acquiring smc binary data failed!\\n");
					r = -1;''', '''					log_printf(0, "\\n***** ERROR!: acquiring smc binary data failed!\\n");
					r = -1;
					goto bad;'''),
}


def CASES(base):
    i, j = bdrun.fnspan(base, FN)
    fn = base[i:j]
    out = []
    names = list(SITES)
    for k in range(0, len(names) + 1):
        for sub in itertools.combinations(names, k):
            for pre in ('keep', 'none'):
                for intail in ('if', 'goto'):
                    if not sub and intail == 'goto':
                        continue
                    f = fn
                    for s in sub:
                        f = bdrun.sub(f, *SITES[s])
                    if sub:
                        tail = '''		if (r)
			GOTO
	}
	return 0;
bad:
	log_printf(0, "\\n\\n**** could not read %s (%i) ****\\n\\n", e->name, r);
	return -1;
LAB}'''
                        if intail == 'if':
                            tail = tail.replace('		if (r)\n			GOTO\n', '''		if (r) {
			log_printf(0, "\\n\\n**** could not read %s (%i) ****\\n\\n", e->name, r);
			return -1;
		}
''')
                        else:
                            tail = tail.replace('GOTO', 'goto bad;')
                    else:
                        tail = TAIL_OLD.replace('none: __attribute__((cold));\n	return 0;\n', 'LAB')
                    if pre == 'keep':
                        tail = tail.replace('LAB', 'none: __attribute__((cold));\n	return 0;\n')
                    else:
                        f = bdrun.sub(f, PRE_OLD, '	for (i = 1;')
                        tail = tail.replace('LAB', '')
                    f = bdrun.sub(f, TAIL_OLD, tail)
                    out.append(('%s %s %s' % ('+'.join(sub) or '-', pre, intail), base[:i] + f + base[j:]))
    return out
