# clientBinPatch without the hints: returns, scopes and result variables
import itertools, os, runpy
V0 = runpy.run_path(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'mc2v_bp.py'))['V']
B = V0['none']
WR = '''					if (netWriteBlocks(nand, rlen, start, count))
						log_printf(0, "Success! Completed patching NAND!\\n");
					else
						log_printf(0, "\\n\\n***** ERROR: Writing data to console failed!\\n");
'''
OPTS = {
    'ret_w': [(WR, WR + '\t\t\t\t\treturn;\n')],
    'ret_w2': [(WR, WR.replace('NAND!\\n");\n', 'NAND!\\n");\n\t\t\t\t\t\treturn;\n').replace('if (netWriteBlocks(nand, rlen, start, count))\n', 'if (netWriteBlocks(nand, rlen, start, count)) {\n').replace('\t\t\t\t\t\treturn;\n\t\t\t\t\telse', '\t\t\t\t\t\treturn;\n\t\t\t\t\t} else'))],
    'okvar': [(WR, '''					i = netWriteBlocks(nand, rlen, start, count);
					if (i)
						log_printf(0, "Success! Completed patching NAND!\\n");
					else
						log_printf(0, "\\n\\n***** ERROR: Writing data to console failed!\\n");
'''), ('	int rlen;\n', '	int rlen, i;\n')],
    'wr_not': [(WR, '''					if (!netWriteBlocks(nand, rlen, start, count))
						log_printf(0, "\\n\\n***** ERROR: Writing data to console failed!\\n");
					else
						log_printf(0, "Success! Completed patching NAND!\\n");
''')],
    'scope_nand': [('	int rlen;\n', ''), ('	uint8_t *nand;\n', ''),
                   ('				nand = netReadBlocks(&rlen, start, count);\n', '				{ int rlen; uint8_t *nand = netReadBlocks(&rlen, start, count);\n'),
                   ('''					log_printf(0, "\\n\\n***** ERROR: Reading data from console failed!\\n");
''', '''					log_printf(0, "\\n\\n***** ERROR: Reading data from console failed!\\n"); }
''')],
    'ret_r': [('''				if (nand && rlen) {
					log_printf(0, "Success!\\nPatching in binary data...");''', '''				if (!nand || !rlen) {
					log_printf(0, "\\n\\n***** ERROR: Reading data from console failed!\\n");
					return;
				}
				{
					log_printf(0, "Success!\\nPatching in binary data...");'''),
              ('''				} else
					log_printf(0, "\\n\\n***** ERROR: Reading data from console failed!\\n");
''', '				}\n')],
    'sw_if': runpy.run_path(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'mc2v_bp2.py'))['V']['sw_if'][-1:],
}
V = {}
keys = list(OPTS)
for n in (1, 2):
    for c in itertools.combinations(keys, n):
        if 'ret_w' in c and 'ret_w2' in c:
            continue
        if sum(k in ('ret_w', 'ret_w2', 'okvar', 'wr_not') for k in c) > 1:
            continue
        V['+'.join(c)] = B + sum((OPTS[k] for k in c), [])
