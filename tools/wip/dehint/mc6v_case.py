# mode_client attempt 6: switch cases with a second real predecessor (shared bodies), the
# structural change attempt 5 named as the only way to replace the case-head feeds.
# Base: src/mode_client.c.  Use with mc2try.py.  Each shape alone and with the feeds into
# the shared heads removed.
C45_OLD = '''			case 4:
				AT(t4)  if (cinfo->hwFlags & 0x20)
					s4: { sendAvatarData(arg, cinfo->kernel); }
				else
					{  { AT(hdd4) { hc4: __attribute__((cold)); } log_printf(0, "\\n\\n***** ERROR: cannot send avatar data when a HDD does not exist!\\n"); } }
				break;
			case 5:
				AT(t5)  if (cinfo->hwFlags & 0x20)
					{ JMP(s4, c12); AT(s5)JMP(dsp);  { sendCompatData(arg); } }
				else
					{ AT(hdd5) { hdd5_c: __attribute__((cold)); } log_printf(0, "\\n\\n***** ERROR: cannot send xbox compatibility data when a HDD does not exist!\\n"); }
				break;
'''
AV = 'log_printf(0, "\\n\\n***** ERROR: cannot send avatar data when a HDD does not exist!\\n");'
CO = 'log_printf(0, "\\n\\n***** ERROR: cannot send xbox compatibility data when a HDD does not exist!\\n");'
HDD4 = '{ AT(hdd4) { hc4: __attribute__((cold)); } ' + AV + ' }'
HDD5 = '{ AT(hdd5) { hdd5_c: __attribute__((cold)); } ' + CO + ' }'
S5 = '{ JMP(s4, c12); AT(s5)JMP(dsp);  { sendCompatData(arg); } }'

def c45(head4, head5, inner):
    return '\t\t\tcase 4:\n%s\t\t\tcase 5:\n%s' % (head4, head5) + inner + '\t\t\t\tbreak;\n'

# A: one HDD test, mode picks the call / message
A = ('\t\t\t\tif (cinfo->hwFlags & 0x20) {\n'
     '\t\t\t\t\tif (mode == 4)\n\t\t\t\t\t\ts4: { sendAvatarData(arg, cinfo->kernel); }\n'
     '\t\t\t\t\telse\n\t\t\t\t\t\t' + S5 + '\n'
     '\t\t\t\t} else if (mode == 4)\n\t\t\t\t\t' + HDD4 + '\n'
     '\t\t\t\telse\n\t\t\t\t\t' + HDD5 + '\n')
# B: mode first inside the shared case
B = ('\t\t\t\tif (!(cinfo->hwFlags & 0x20)) {\n'
     '\t\t\t\t\tif (mode == 4)\n\t\t\t\t\t\t' + HDD4 + '\n'
     '\t\t\t\t\telse\n\t\t\t\t\t\t' + HDD5 + '\n'
     '\t\t\t\t} else if (mode == 4)\n\t\t\t\t\ts4: { sendAvatarData(arg, cinfo->kernel); }\n'
     '\t\t\t\telse\n\t\t\t\t\t' + S5 + '\n')
# C: mode == 5 tests
C = ('\t\t\t\tif (cinfo->hwFlags & 0x20) {\n'
     '\t\t\t\t\tif (mode == 5)\n\t\t\t\t\t\t' + S5 + '\n'
     '\t\t\t\t\telse\n\t\t\t\t\t\ts4: { sendAvatarData(arg, cinfo->kernel); }\n'
     '\t\t\t\t} else if (mode == 5)\n\t\t\t\t\t' + HDD5 + '\n'
     '\t\t\t\telse\n\t\t\t\t\t' + HDD4 + '\n')
# D: HDD test first, error message shared through a goto (case 5 jumps into case 4's
# message? no: messages differ), so: case 4 falls into a shared HDD check via goto
D = ('\t\t\tcase 4:\n\t\t\t\tAT(t4)  if (cinfo->hwFlags & 0x20)\n\t\t\t\t\ts4: { sendAvatarData(arg, cinfo->kernel); }\n'
     '\t\t\t\telse\n\t\t\t\t\t{  ' + HDD4 + ' }\n\t\t\t\tbreak;\n'
     '\t\t\tcase 5:\n\t\t\t\tAT(t5)  if (cinfo->hwFlags & 0x20)\n\t\t\t\t\t' + S5 + '\n'
     '\t\t\t\telse\n\t\t\t\t\t' + HDD5 + '\n\t\t\t\tbreak;\n')

T5FEED = 'if (__builtin_constant_p(mode + 3000) && __builtin_constant_p(mode + 53000) && __builtin_constant_p(mode + 103000) && __builtin_constant_p(mode + 153000)) goto t5;'
T4FEED = 'if (__builtin_constant_p(mode + 930) && __builtin_constant_p(mode + 931) && __builtin_constant_p(mode + 932) && __builtin_constant_p(mode + 933)) goto t4;'

V = {}
for nm, inner in (('A', A), ('B', B), ('C', C)):
    for hn, h4, h5 in (('t4', '\t\t\t\tAT(t4)\n', ''), ('t5', '', '\t\t\t\tAT(t5)\n'),
                       ('t45', '\t\t\t\tAT(t4)\n', '\t\t\t\tAT(t5)\n')):
        new = c45(h4, h5, inner)
        base = [(C45_OLD, new)]
        rm = []
        if 't4' not in hn:
            rm.append((T4FEED, ''))
        if 't5' not in hn:
            rm.append((T5FEED, ''))
        V['%s_%s' % (nm, hn)] = base + rm
        if 't4' in hn:
            V['%s_%s_-t4' % (nm, hn)] = base + rm + [(T4FEED, '')]
        if 't5' in hn:
            V['%s_%s_-t5' % (nm, hn)] = base + rm + [(T5FEED, '')]
        if hn == 't45':
            V['%s_%s_-t4t5' % (nm, hn)] = base + [(T4FEED, ''), (T5FEED, '')]
V['D'] = [(C45_OLD, D)]

# cases 7 / 12 sharing the dummy test
C712_7 = '''			case 7:
				AT(c7)  if (arg == dummy)
					clientPatches(NULL);
				else
					{ AT(p1) clientPatches(arg); }
				break;
'''
C712_12 = '''			case 12:
				AT(c12) if (arg == dummy)
					clientInfo(NULL);
				else
					{ AT(i1) clientInfo(arg); }
				break;
'''
for nm, a7, a12 in (
        ('P', '''			case 7:
				AT(c7)  if (arg == dummy)
					arg = NULL;
				{ AT(p1) clientPatches(arg); }
				break;
''', '''			case 12:
				AT(c12) if (arg == dummy)
					arg = NULL;
				{ AT(i1) clientInfo(arg); }
				break;
'''),
        ('Q', '''			case 7:
				AT(c7)  { AT(p1) clientPatches(arg == dummy ? NULL : arg); }
				break;
''', '''			case 12:
				AT(c12) { AT(i1) clientInfo(arg == dummy ? NULL : arg); }
				break;
''')):
    V[nm + '7'] = [(C712_7, a7)]
    V[nm + '12'] = [(C712_12, a12)]
    V[nm + '7_12'] = [(C712_7, a7), (C712_12, a12)]
