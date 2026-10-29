# structural: fewer/merged switch edges, if-chains, helpers
A4 = r'''			case 4:
				if (cinfo->hwFlags & 0x20)
					sendAvatarData(arg, cinfo->kernel);
				else
					log_printf(0, "\n\n***** ERROR: cannot send avatar data when a HDD does not exist!\n");
				break;
			case 5:
				if (cinfo->hwFlags & 0x20)
					sendCompatData(arg);
				else
					log_printf(0, "\n\n***** ERROR: cannot send xbox compatibility data when a HDD does not exist!\n");
				break;
'''
MA = r'log_printf(0, "\n\n***** ERROR: cannot send avatar data when a HDD does not exist!\n")'
MC = r'log_printf(0, "\n\n***** ERROR: cannot send xbox compatibility data when a HDD does not exist!\n")'
merged = r'''			case 4:
			case 5:
				if (cinfo->hwFlags & 0x20) {
					if (mode == 4) sendAvatarData(arg, cinfo->kernel);
					else sendCompatData(arg);
				} else {
					if (mode == 4) %s;
					else %s;
				}
				break;
''' % (MA, MC)
merged2 = r'''			case 4:
			case 5:
				if (mode == 4) {
					if (cinfo->hwFlags & 0x20) sendAvatarData(arg, cinfo->kernel);
					else %s;
				} else {
					if (cinfo->hwFlags & 0x20) sendCompatData(arg);
					else %s;
				}
				break;
''' % (MA, MC)
rng = merged2.replace('case 4:\n\t\t\tcase 5:', 'case 4 ... 5:')
SW = '\t\t\tswitch (mode) {'
pre = r'''			if (mode == 4) {
				if (cinfo->hwFlags & 0x20) sendAvatarData(arg, cinfo->kernel);
				else %s;
			} else if (mode == 5) {
				if (cinfo->hwFlags & 0x20) sendCompatData(arg);
				else %s;
			} else
''' % (MA, MC)
hdd = r'''			case 4:
			case 5:
				if (!(cinfo->hwFlags & 0x20)) {
					if (mode == 4) %s;
					else %s;
					break;
				}
				if (mode == 4) sendAvatarData(arg, cinfo->kernel);
				else sendCompatData(arg);
				break;
''' % (MA, MC)
outer = r'''			switch (mode) {
			case 4:
				if (cinfo->hwFlags & 0x20) sendAvatarData(arg, cinfo->kernel);
				else %s;
				break;
			case 5:
				if (cinfo->hwFlags & 0x20) sendCompatData(arg);
				else %s;
				break;
			default:
			switch (mode) {''' % (MA, MC)
VARS = [
 ('merged', [(A4, merged)]),
 ('merged2', [(A4, merged2)]),
 ('range', [(A4, rng)]),
 ('pre45', [(A4, ''), (SW, pre + SW)]),
 ('hdd45', [(A4, hdd)]),
 ('outer', [(A4, ''), (SW, outer), ('\t\t\t\tbreak;\n\t\t\t}\n\t\t} else\n\t\t\tgoto fail;', '\t\t\t\tbreak;\n\t\t\t}\n\t\t\t}\n\t\t} else\n\t\t\tgoto fail;')]),
]
