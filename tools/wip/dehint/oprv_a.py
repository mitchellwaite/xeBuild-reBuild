# oprv.py variants: parseOption's borderline shapes made natural, one at a time and together
# (against 98a0eba6's src/options.c).  Combine with +, e.g. `cpu+gpu+bool+vlen+m1`.
CPU_OLD = '''			xb.cpuTemp = myatou32(val, -1);
			ok = 0;
			if (xb.cpuTemp != -1) {
				log_printf(1, "Using CPUTEMP option, value %d\\n", xb.cpuTemp);
				ok = 1;
			}
			if (!ok)
				goto bad;
			return 1;
'''
CPU_NEW = '''			xb.cpuTemp = myatou32(val, -1);
			if (xb.cpuTemp == -1)
				goto bad;
			log_printf(1, "Using CPUTEMP option, value %d\\n", xb.cpuTemp);
			return 1;
'''
GPU_OLD = '''			xb.gpuFan = myatou32(val, -1);
			ok = 0;
			if (xb.gpuFan != -1) {
				log_printf(1, "Using GPUFAN option, value %d\\n", xb.gpuFan);
				ok = 1;
			}
			if (!ok)
				goto bad;
			return 1;
'''
GPU_NEW = '''			xb.gpuFan = myatou32(val, -1);
			if (xb.gpuFan == -1)
				goto bad;
			log_printf(1, "Using GPUFAN option, value %d\\n", xb.gpuFan);
			return 1;
'''
BOOL_OLD = '''	ok = 0;
	if (setBoolOption(opt, val) == 1) {
		log_printf(1, "\\n");
		ok = 1;
	} else if (val) {
'''
BOOL_END_OLD = '''	}
	if (ok)
		return 1;
'''
MAC_OLD = '''					xb.macid[0] = myatox8(val);
					val += 2;
					log_printf(1, "%02x", xb.macid[0]);
					macidRest(&xb.macid[1], val, 5);
'''


def boolf(test, sep):
    return [(BOOL_OLD, '\tif (%s) {\n\t\tlog_printf(1, "\\n");\n\t\treturn 1;\n\t}%s' % (test, sep)),
            (BOOL_END_OLD, '\t}\n')]


V = [
    ('src', []),
    ('cpu', [(CPU_OLD, CPU_NEW)]),
    ('gpu', [(GPU_OLD, GPU_NEW)]),
    ('bool', boolf('setBoolOption(opt, val) == 1', '\n\tif (val) {\n')),
    ('boolelse', boolf('setBoolOption(opt, val) == 1', ' else if (val) {\n')),
    ('booln', boolf('setBoolOption(opt, val)', '\n\tif (val) {\n')),
    ('vlen', [('\tif (val && vlen) {\n', '\tif (vlen) {\n')]),
    # macid: bytes 1..5 in a loop of their own
    ('m1', [(MAC_OLD, '''					xb.macid[0] = myatox8(val);
					val += 2;
					log_printf(1, "%02x", xb.macid[0]);
					for (i = 1; i < 6; i++) {
						log_printf(1, ":");
						xb.macid[i] = myatox8(val);
						val += 2;
						log_printf(1, "%02x", xb.macid[i]);
					}
''')]),
    # one loop, ":" before every byte but the first
    ('m2', [('''					log_printf(1, "Using MACID option address: ");
					xb.macid[0] = myatox8(val);
					val += 2;
					log_printf(1, "%02x", xb.macid[0]);
					macidRest(&xb.macid[1], val, 5);
''', '''					log_printf(1, "Using MACID option address: ");
					for (i = 0; i < 6; i++) {
						if (i)
							log_printf(1, ":");
						xb.macid[i] = myatox8(val);
						val += 2;
						log_printf(1, "%02x", xb.macid[i]);
					}
''')]),
    # the helper's indexing, written out
    ('m3', [(MAC_OLD, '''					xb.macid[0] = myatox8(val);
					val += 2;
					log_printf(1, "%02x", xb.macid[0]);
					for (i = 0; i < 5; i++) {
						log_printf(1, ":");
						xb.macid[i + 1] = myatox8(val + i * 2);
						log_printf(1, "%02x", xb.macid[i + 1]);
					}
''')]),
    ('m4', [(MAC_OLD, '''					xb.macid[0] = myatox8(val);
					log_printf(1, "%02x", xb.macid[0]);
					for (i = 1; i < 6; i++) {
						log_printf(1, ":");
						xb.macid[i] = myatox8(val + i * 2);
						log_printf(1, "%02x", xb.macid[i]);
					}
''')]),
]
