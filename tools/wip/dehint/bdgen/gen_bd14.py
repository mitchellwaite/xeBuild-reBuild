"""loadConsoleBlFiles, case 2 without the dead expect: the two error blocks tie at the same
frequency and need the config one first"""
REMOVE = ['exp_t2']
FOCUS = ['_loadConsoleBlFiles']
Q = '''					e->offset = smcSetLoad(e->size);
					if (!e->offset)
						r = -1;
				} else {
					log_printf(0, "\\n***** ERROR!: acquiring smc binary data failed!\\n");
					r = -1;
				}
'''
Q2 = '''					r = extractSmcConfig(e, xb.files[xb.nFlashFiles].data, xb.files[xb.nFlashFiles].size);
				} else {
					log_printf(0, "\\n***** ERROR!: acquiring smc configuration data failed!\\n");
					r = -1;
				}
'''
A = [
    ('', []),
    ('oz', [(Q, Q.replace('if (!e->offset)', 'if (e->offset == 0)'))]),
    ('rfirst', [(Q, '''					e->offset = smcSetLoad(e->size);
					if (!e->offset)
						r = -1;
				} else {
					r = -1;
					log_printf(0, "\\n***** ERROR!: acquiring smc binary data failed!\\n");
				}
''')]),
    ('tern', [(Q, '''					e->offset = smcSetLoad(e->size);
					r = e->offset ? 0 : -1;
				} else {
					log_printf(0, "\\n***** ERROR!: acquiring smc binary data failed!\\n");
					r = -1;
				}
''')]),
    ('rbreak', [(Q, '''					e->offset = smcSetLoad(e->size);
					if (!e->offset)
						r = -1;
					break;
				}
				log_printf(0, "\\n***** ERROR!: acquiring smc binary data failed!\\n");
				r = -1;
''')]),
    ('fail', [(Q, '''					e->offset = smcSetLoad(e->size);
					if (e->offset)
						break;
				} else
					log_printf(0, "\\n***** ERROR!: acquiring smc binary data failed!\\n");
				r = -1;
''')]),
    ('fail2', [(Q, '''					e->offset = smcSetLoad(e->size);
					if (!e->offset)
						goto smcfail;
				} else {
					log_printf(0, "\\n***** ERROR!: acquiring smc binary data failed!\\n");
smcfail:
					r = -1;
				}
''')]),
]
B = [
    ('', []),
    ('crfirst', [(Q2, Q2.replace('''log_printf(0, "\\n***** ERROR!: acquiring smc configuration data failed!\\n");
					r = -1;''', '''r = -1;
					log_printf(0, "\\n***** ERROR!: acquiring smc configuration data failed!\\n");'''))]),
    ('crbreak', [(Q2, '''					r = extractSmcConfig(e, xb.files[xb.nFlashFiles].data, xb.files[xb.nFlashFiles].size);
					break;
				}
				log_printf(0, "\\n***** ERROR!: acquiring smc configuration data failed!\\n");
				r = -1;
''')]),
]
AXES = [A, B]
