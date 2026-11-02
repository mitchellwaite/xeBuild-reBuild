"""loop (option-arm) asm-goto sites: name -> anchor statement in mode_client's option loop.
add(text, site, targets) puts '{ stmt JMP(t..); }' after the anchor."""
LS = {
 'u0': 'client_usage(0, NULL);',
 'nent': 'promptEnter = 0;',
 'rbs': 'log_printf(0, "shutdown superseded by reboot, ignoring -s in favor of -reboot\n");',
 'rbt': 'reboot = 2;\n\t\t} else if (E(!strnicmp(argv[i], "-bp"',
 'sig': 'log_printf(0, "reboot has already been set on command line, ignoring -s\n");',
 'sset': 'reboot = 1;',
 'keys': 'arg = dummy;\n\t\t} else if (!strnicmp(argv[i], "-ip"',
 'ip': 'log_printf(0, "setting forced IP to %s\n", ip);',
 'bp': 'mode = 11;', 'rb': 'mode = 8;', 'wb': 'mode = 9;', 'eb': 'mode = 10;', 'r': 'mode = 1;', 'w': 'mode = 2;',
 'e': 'mode = 4;', 'c': 'mode = 5;', 'i': 'mode = 12;', 'p': 'mode = 7;',
 'v': 'log_verbose_flag(argv[i][2]);',
 'u1': 'client_usage(1, argv[i]);\n\t}',
}
def add(t, site, tg):
    a = LS[site]; s = a.split('\n')[0]
    p = t.index(a, t.index('int mode_client(')); e = p + len(s)
    return t[:p] + '{ ' + s + ' JMP(%s); }' % ','.join(tg) + t[e:]
for _k in LS: LS[_k] = LS[_k].replace(chr(10) + '"', chr(92) + 'n"')
