# imgAdd: forms of partial/npages without the "g"(t) pin (and optionally without the lnp2 label)
BASE = 'tools/wip/dehint/drafts/image_write.c'
PIN = '''			/* no code: the slot order of t and partial (dead in every clone) */
			__asm__("" :: "g"(t));
'''
OLD = '''		partial = type != 0 && type != '0' && len < 0x4000;
		if (len % 512)
			npages = (len + 512) / 512;
		else
			npages = len / 512;
		if (!partial)
			npages = 32;
		else {
			/* imgAddFile's clone: keeps DOM2's threading from zeroing the npages guard edge */
			lnp2: __attribute__((hot));
		}
'''
NP = '''		if (len % 512)
			npages = (len + 512) / 512;
		else
			npages = len / 512;
'''
LBL = '''		else {
			lnp2: __attribute__((hot));
		}
'''
def forms(lbl):
    L = LBL if lbl else ''
    return {
        'A': f"		partial = type != 0 && type != '0' && len < 0x4000;\n{NP}		if (!partial)\n			npages = 32;\n{L}",
        'B': f"		partial = type != 0 && type != '0';\n		if (len >= 0x4000)\n			partial = 0;\n{NP}		if (!partial)\n			npages = 32;\n{L}",
        'C': f"		partial = type != 0 && type != '0';\n{NP}		if (!partial || len >= 0x4000)\n			npages = 32;\n{L}",
        'D': f"{NP}		if (type == 0 || type == '0' || len >= 0x4000)\n			npages = 32;\n{L}",
        'E': f"		partial = len < 0x4000;\n		if (type == 0 || type == '0')\n			partial = 0;\n{NP}		if (!partial)\n			npages = 32;\n{L}",
        'F': f"		partial = len < 0x4000 && type != 0 && type != '0';\n{NP}		if (!partial)\n			npages = 32;\n{L}",
        'G': f"		partial = (type != 0 && type != '0') ? len < 0x4000 : 0;\n{NP}		if (!partial)\n			npages = 32;\n{L}",
        'H': f"		partial = type && type != '0' && len < 0x4000;\n		npages = 32;\n		if (partial) {{\n			if (len % 512)\n				npages = (len + 512) / 512;\n			else\n				npages = len / 512;\n		}}\n",
        'I': f"		partial = type != '0' && type != 0 && len < 0x4000;\n{NP}		if (!partial)\n			npages = 32;\n{L}",
        'J': f"		partial = 1;\n		if (type == 0 || type == '0' || len >= 0x4000)\n			partial = 0;\n{NP}		if (!partial)\n			npages = 32;\n{L}",
        'K': f"		if (type != 0 && type != '0' && len < 0x4000)\n			partial = 1;\n		else\n			partial = 0;\n{NP}		if (!partial)\n			npages = 32;\n{L}",
        'M': f"		{{ int nz = type != 0 && type != '0'; int small = len < 0x4000; partial = nz && small; }}\n{NP}		if (!partial)\n			npages = 32;\n{L}",
    }
axis = []
for k, v in forms(True).items():
    axis.append((k + 'L', [(OLD, v)]))
for k, v in forms(False).items():
    axis.append((k, [(OLD, v)]))
AXES = [[('', [(PIN, '')]), ('pin', [])], axis]
