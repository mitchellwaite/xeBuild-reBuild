"""getImageSmc from gen_ir155's ii.en.tt.g.a0 (2 loose, B only): spellings of what the bad arm's log reads and of addr's definition, and t's."""
FOCUS = ['_getImageSmc']
BASE = 'tools/wip/dehint/drafts/image_read_attempt9.c'
LOG = 'log_printf(1, "smc.bin should not be at 0x%x, trying 0x1000\\n", addr);\n addr = 0x1000;\n'
HEAD_OLD = '''	int addr = SWAP32(h->smcBootAddr);
	int size = SWAP32(h->smcBootSize);
'''
TL = 'unsigned t = addr;\n if (t != 0x1000) { if (t != 0x800) goto bad; }\n'
BADOLD = 'bad:\n' + LOG
ZOLD = 'if (!addr) { ' + LOG + ' }\n'
LB = {
 'la': LOG,
 'lt': 'log_printf(1, "smc.bin should not be at 0x%x, trying 0x1000\\n", t);\n addr = 0x1000;\n',
 'lu': 'log_printf(1, "smc.bin should not be at 0x%x, trying 0x1000\\n", (unsigned)addr);\n addr = 0x1000;\n',
}
HEADS = {
 'h0': (HEAD_OLD, ZOLD, TL),
 'h1': ('	unsigned t = SWAP32(h->smcBootAddr);\n	int size = SWAP32(h->smcBootSize);\n	int addr = t;\n', ZOLD, 'if (addr) t = addr; else t = 0x1000;\n if (t != 0x1000) { if (t != 0x800) goto bad; }\n'),
 'h2': ('	int addr, size;\n	addr = SWAP32(h->smcBootAddr);\n	size = SWAP32(h->smcBootSize);\n', ZOLD, TL),
 'h3': ('	uint32_t addr0 = SWAP32(h->smcBootAddr);\n	int size = SWAP32(h->smcBootSize);\n	int addr = addr0;\n', ZOLD, TL),
 'h4': (HEAD_OLD, ZOLD, 'unsigned t = addr;\n if (addr != 0x1000) { if (addr != 0x800) goto bad; }\n'),
 'h5': (HEAD_OLD, ZOLD, 'unsigned t = addr;\n if (t == 0x1000) goto bback; if (t != 0x800) goto bad;\n'),
 'h6': (HEAD_OLD, ZOLD, 'unsigned t = addr;\n if (t != 0x1000 && t != 0x800) goto bad;\n'),
}
AX = []
for kl, l in LB.items():
    for kh, (a, z, t) in HEADS.items():
        AX.append((kl + '.' + kh, [(HEAD_OLD, a), (ZOLD, z), (TL, t), (BADOLD, 'bad:\n' + l)]))
AXES = [AX]
