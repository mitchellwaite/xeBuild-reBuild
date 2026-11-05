"""base2: nested guards VRP folds (not FRE), in both spellings, per arm.  Measures entry; targets from irfqp (-3, -4: 12-13%; -1: 13%; -2: 22-27%; site 3: 52-53%)."""
BASE = 'tools/wip/dehint/drafts/image_read_attempt4_base2.c'
FOCUS = ['_parseDump']
LOGS = {
 -3: '''			log_printf(0, "***** WARNING: nanddump.bin has a bad LBA at block 0x%x (raw offset 0x%x), block LBA ignored\\n", blk, src - raw);
''',
 -6: '''			log_printf(0, "***** WARNING: nanddump.bin has a mixed controller LBA at block 0x%x (raw offset 0x%x), block ignored\\n", blk, src - raw);
''',
 -4: '''			log_printf(1, "ECD error at block 0x%x (raw offset 0x%x), block will be remapped\\n", blk, src - raw);
''',
 -1: '''			log_printf(1, "bad block at 0x%x (raw offset 0x%x), block ignored\\n", blk, src - raw);
''',
}
POS = {'ge0': 'blk >= 0', 'le': 'blk <= blocks', 'nem': 'blk != -1', 'ltb1': 'blk < blocks + 1', 'gem': 'blk >= -1', 'gtm': 'blk > -1'}
NEG = {'lt0': 'blk < 0', 'gt': 'blk > blocks', 'eqm': 'blk == -1', 'lem': 'blk <= -1', 'eqb': 'blk == blocks'}
AX = [('', [])]
for arm, log in LOGS.items():
    for k, c in NEG.items():
        AX.append(('%d.c.%s' % (arm, k), [(log, '			if (' + c + ')\n				continue;\n' + log)]))
    for k, c in POS.items():
        AX.append(('%d.g.%s' % (arm, k), [(log, '			if (!(' + c + '))\n				continue;\n' + log)]))
for k, c in POS.items():
    AX.append(('-2.%s' % k, [('''		if (dst == -2)
			continue;
''', '''		if (dst == -2) {
			if (''' + c + ''')
				continue;
		}
''')]))
    AX.append(('s3.%s' % k, [('''		if (dst != blk && !addRemap(dst, blk, blocks))
			return 0;
''', '''		if (dst != blk) {
			if (''' + c + ''') {
				if (!addRemap(dst, blk, blocks))
					return 0;
			}
		}
''')]))
AXES = [AX]
