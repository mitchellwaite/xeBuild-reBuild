R='} else { k55l: if (!strnicmp(argv[i], "-r", 2)) {'
S='esucc:  log_printf(0, "Success!\n"); }'
X='esucc: __asm__ goto ("" :::: einv); log_printf(0, "Success!\n"); }'
sh r.sh b01 x1.c "$R" '} else { k55l: if (!strnicmp(argv[i], "-r", 2) && !__builtin_constant_p(i + 5555)) {'
sh r.sh b02 x1.c 'log_printf(0, "setting read filename to %s\n", arg);' 'log_printf(0, "setting read filename to %s\n", arg); __asm__ goto("" :::: k61l);'
sh r.sh b03 n2.c "$R" '} else { k55l: if (!__builtin_constant_p(i + 5555) && !strnicmp(argv[i], "-r", 2)) {'
sh r.sh b04 n2.c "$R" '} else { k55l: if (!strnicmp(argv[i], "-r", 2) && !__builtin_constant_p(i + 5555) && !__builtin_constant_p(i + 5556)) {'
sh r.sh b05 n2.c "$R" '} else { k55l: if (!strnicmp(argv[i], "-r", 2) && !(__builtin_constant_p(i + 5555) && __builtin_constant_p(i + 5556))) {'
sh r.sh b06 n2.c 'log_printf(0, "setting read filename to %s\n", arg);' 'log_printf(0, "setting read filename to %s\n", arg); if (__builtin_constant_p(i + 5555)) goto k61l;'
sh r.sh b07 n2.c 'arg = argv[++i];
			log_printf(0, "setting read filename' 'if (__builtin_constant_p(i + 5555)) goto k61l; arg = argv[++i];
			log_printf(0, "setting read filename'
sh r.sh b08 n2.c 'mode = 1;
		} else { k61l:' 'mode = 1; if (__builtin_constant_p(i + 5555)) goto k61l;
		} else { k61l:'
