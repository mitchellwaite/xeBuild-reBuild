# error arm predicted 73% by OPCODE_POSITIVE on an inverted bit test; with/without separate post-loop tests
T = 'if (cinfo->hwFlags & 0x20)'
EA = r'''				if (cinfo->hwFlags & 0x20)
					sendAvatarData(arg, cinfo->kernel);
				else
					log_printf(0, "\n\n***** ERROR: cannot send avatar data when a HDD does not exist!\n");'''
EC = r'''				if (cinfo->hwFlags & 0x20)
					sendCompatData(arg);
				else
					log_printf(0, "\n\n***** ERROR: cannot send xbox compatibility data when a HDD does not exist!\n");'''
def inv(s, cond):
    l = s.split('\n')
    return '\n'.join(['\t\t\t\tif (%s)' % cond, l[3], '\t\t\t\telse', l[1]])
P = '\tif (!(mode && arg)) {'
A = '({ __asm__(""); 0; })'
VARS = []
for cn, c in (('n', '(int)(~cinfo->hwFlags & 0x20) > 0'), ('x', '(int)((cinfo->hwFlags ^ 0x20) & 0x20) > 0'), ('n1', '(int)(~cinfo->hwFlags & 0x20) >= 1')):
    VARS.append(('i' + cn, [(EA, inv(EA, c)), (EC, inv(EC, c))]))
    VARS.append(('i' + cn + '_sep', [(EA, inv(EA, c)), (EC, inv(EC, c)), (P, '\tif (!mode || %s || !arg) {' % A)]))
    VARS.append(('i' + cn + '_le', [(EA, inv(EA, c)), (EC, inv(EC, c)), (P, '\tif (mode <= 0 || %s || !arg) {' % A)]))
