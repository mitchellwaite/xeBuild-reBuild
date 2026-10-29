SW = '\t\t\tswitch (mode) {'
MA = r'log_printf(0, "\n\n***** ERROR: cannot send avatar data when a HDD does not exist!\n")'
MC = r'log_printf(0, "\n\n***** ERROR: cannot send xbox compatibility data when a HDD does not exist!\n")'
VARS = [
 ('exp4', [(SW, '\t\t\tswitch (__builtin_expect(mode, 4)) {')]),
 ('exp1', [(SW, '\t\t\tswitch (__builtin_expect(mode, 1)) {')]),
 ('ul', [(SW, '\t\t\tswitch ((unsigned)mode) {')]),
 ('two', [(SW, '\t\t\tswitch (mode) { case 4: if (!(cinfo->hwFlags & 0x20)) { %s; goto done; } break; case 5: if (!(cinfo->hwFlags & 0x20)) { %s; goto done; } break; }\n' % (MA, MC) + SW),
          ('\tif (E(reboot))', 'done:\n\tif (E(reboot))')]),
]
