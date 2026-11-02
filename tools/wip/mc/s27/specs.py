IPEND = r'log_printf(0, "setting forced IP to %s\n", ip);'
S4 = 'sendAvatarData(arg, cinfo->kernel);'
H4 = r'log_printf(0, "\n\n***** ERROR: cannot send avatar data when a HDD does not exist!\n");'
H5 = r'log_printf(0, "\n\n***** ERROR: cannot send xbox compatibility data when a HDD does not exist!\n");'
LOOP1 = '\tif (NO_MODE_ARG(mode, arg))'
def J(*l): return 'JMP(%s);' % ','.join(l)
def br(stmt_anchor, jmp):
    """wrap a single-statement arm: 'stmt' -> '{ stmt jmp }'"""
    return [(stmt_anchor, '{ ', 'b'), (stmt_anchor, ' ' + jmp + ' }', 'a')]
F1 = br(H4, J('u2'))
def pre(anchor, jmp): return [(anchor, jmp + ' ', 'b')]
C = {1: 'netDumpNand(arg);', 2: 'clientWrite(arg);', 3: 'clientKeys();', 8: 'clientReadBlocks(arg, start, count);',
     9: 'clientWriteBlocks(arg, start);', 10: 'clientEraseBlock(arg);', 11: 'clientBinPatch(arg, start);'}
G3 = F1 + pre(C[3], J('hdd5', 's5'))
LAB = {'lr': 'if (!strnicmp(argv[i], "-r", 2))', 'lw': 'if (!strnicmp(argv[i], "-w", 2))',
       'le': 'if (E(!strnicmp(argv[i], "-e", 2)))', 'lc': 'if (E(!strnicmp(argv[i], "-c", 2)))',
       'li': 'if (!strnicmp(argv[i], "-i", 2))', 'lp': 'if (!strnicmp(argv[i], "-p", 2))',
       'lv': 'if (!strnicmp(argv[i], "-v", 2))'}
def labs(*ls): return [(LAB[l], l + ': ', 'b') for l in ls]
IPMID = 'ip = argv[++i];'
