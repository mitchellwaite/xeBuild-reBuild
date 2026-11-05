"""parseDump's dead test (blk >= 0): the dst tests as switches, whole chain or in part."""
FOCUS = ['_parseDump', '_loadDump']
BASE = 'tools/wip/dehint/drafts/image_read_attempt8.c'
src = open(BASE, newline='').read().replace('\r\n', '\n')
i = src.index('		/* blk >= 0 is always true (a dead test, VRP folds it).')
j = src.index('		if (dst != blk) {\n			if (blk >= blocks - 32)')
OLD = src[i:j]
L1 = 'log_printf(1, "bad block at 0x%x (raw offset 0x%x), block ignored\\n", blk, src - raw);\n if (!addRemap(blk, dst, blocks)) return 0;\n goto next;\n'
L3 = 'log_printf(0, "***** WARNING: nanddump.bin has a bad LBA at block 0x%x (raw offset 0x%x), block LBA ignored\\n", blk, src - raw);\n continue;\n'
L6 = 'log_printf(0, "***** WARNING: nanddump.bin has a mixed controller LBA at block 0x%x (raw offset 0x%x), block ignored\\n", blk, src - raw);\n log_printf(0, "               this is likely caused by previously using jaspersb on a jasper type console!\\n", blk, src - raw);\n continue;\n'
L4 = 'log_printf(1, "ECD error at block 0x%x (raw offset 0x%x), block will be remapped\\n", blk, src - raw);\n if (!addRemap(blk, -1, blocks)) return 0;\n dst = blk;\n'
def ifs(*ks):
    m = {-1: L1, -3: L3, -6: L6, -4: L4}
    return ''.join('if (dst == %d) { %s }\n' % (k, m[k]) for k in ks)
ALL = ifs(-1, -3, -6, -4)
F = {
 'plain': 'if (dst == -2) continue;\n' + ALL,
 's2': 'switch (dst) { case -2: continue; }\n' + ALL,
 's2d': 'switch (dst) { case -2: continue; default: break; }\n' + ALL,
 's1': 'if (dst == -2) continue;\n switch (dst) { case -1: ' + L1 + ' }\n' + ifs(-3, -6, -4),
 's21': 'switch (dst) { case -2: continue; case -1: ' + L1 + ' }\n' + ifs(-3, -6, -4),
 's213': 'switch (dst) { case -2: continue; case -1: ' + L1 + ' case -3: ' + L3 + ' }\n' + ifs(-6, -4),
 'all': 'switch (dst) { case -2: continue; case -1: ' + L1 + ' case -3: ' + L3 + ' case -6: ' + L6 + ' case -4: ' + L4 + ' }\n',
 'all2': 'switch (dst) { case -2: continue; case -1: ' + L1 + ' case -3: ' + L3 + ' case -4: ' + L4 + ' break; case -6: ' + L6 + ' }\n',
 'rest': 'if (dst == -2) continue;\n switch (dst) { case -1: ' + L1 + ' case -3: ' + L3 + ' case -6: ' + L6 + ' case -4: ' + L4 + ' }\n',
 's4': 'if (dst == -2) continue;\n' + ifs(-1, -3, -6) + ' switch (dst) { case -4: ' + L4 + ' }\n',
 's3': 'if (dst == -2) continue;\n' + ifs(-1) + ' switch (dst) { case -3: ' + L3 + ' }\n' + ifs(-6, -4),
 's6': 'if (dst == -2) continue;\n' + ifs(-1, -3) + ' switch (dst) { case -6: ' + L6 + ' }\n' + ifs(-4),
 # a second use of dst's comparison, so -2's test has another shape at profile time
 'cl': 'int erased = dst == -2; if (erased) continue;\n' + ALL,
 'cn': 'if (dst < 0) { if (dst == -2) continue; ' + ALL + ' }\n',
 'cm': 'if (dst + 2 == 0) continue;\n' + ALL,
 'cg': 'if (dst != -2) { ' + ALL + ' } else continue;\n',
}
AXES = [[(k, [(OLD, v)]) for k, v in F.items()]]
