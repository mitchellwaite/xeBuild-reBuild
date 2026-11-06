# mode_client attempt 6: clientEraseBlockI without hints / as a real call.
# Base: src/mode_client.c.  Use with mc2try.py.
import re

SRC = open(__file__.replace('tools\\wip\\dehint\\mc6v_ceb.py', 'src\\mode_client.c')
           .replace('tools/wip/dehint/mc6v_ceb.py', 'src/mode_client.c')).read()
i = SRC.find('static void clientEraseBlockI(')
j = SRC.find('\n}\n', i) + 3
CEBI = SRC[i:j]

NAT = '''static void clientEraseBlockI(const char *sblock)
{
	uint32_t block = myatoh32(sblock, -1);

	if (block != -1) {
		if (block < cinfo->nandSize / cinfo->blockSize) {
			log_printf(0, "erasing block 0x%x...", block);
			if (netEraseBlock(block, 1))
				log_printf(0, "Success!\\n");
			else
				log_printf(0, "\\n\\n***** ERROR: Failed to erase block 0x%x!\\n", block);
		} else
			log_printf(0, "\\n\\n***** ERROR: Block 0x%x is outside system area!\\n", block);
	} else
		log_printf(0, "\\n\\n***** ERROR: Invalid arguments specified, please provide hex only for offset!\\n");
}
'''
V = {
    'call': [(CEBI, ''), ('clientEraseBlockI(arg)', 'clientEraseBlock(arg)')],
    'nat': [(CEBI, NAT)],
    'nat_cold': [(CEBI, NAT.replace('\t} else\n\t\tlog_printf(0, "\\n\\n***** ERROR: Invalid', '\t} else {\n\t\teinv: __attribute__((cold));\n\t\tlog_printf(0, "\\n\\n***** ERROR: Invalid').replace('offset!\\n");\n}', 'offset!\\n");\n\t}\n}'))],
}
