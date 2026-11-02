B=n2.c
R='} else { k55l: if (!strnicmp(argv[i], "-r", 2)) {'
W='} else { k61l: if (!strnicmp(argv[i], "-w", 2)) {'
U3='client_usage(3, argv[i]);
			if (mode) { r5x:'
sh r.sh a01 $B "$R" '} else { k55l: if (E(!strnicmp(argv[i], "-r", 2))) {'
sh r.sh a02 $B "$W" '} else { k61l: if (E(!strnicmp(argv[i], "-w", 2))) {'
sh r.sh a03 $B "$R" '} else { k55l: if (__builtin_expect(!strnicmp(argv[i], "-r", 2), 0)) {'
sh r.sh a04 $B "$W" '} else { k61l: __attribute__((cold)); if (!strnicmp(argv[i], "-w", 2)) {'
sh r.sh a05 $B "$R" '} else { k55l: __attribute__((cold)); if (!strnicmp(argv[i], "-r", 2)) {'
sh r.sh a06 $B "$R" '} else { k55l: __attribute__((hot)); if (!strnicmp(argv[i], "-r", 2)) {'
sh r.sh a07 $B "$U3" 'client_usage(3, argv[i]);
			if (mode) { r5x: __asm__ goto("" :::: k61l);'
sh r.sh a08 $B "$U3" '{ __asm__ goto("" :::: k61l); client_usage(3, argv[i]); }
			if (mode) { r5x:'
sh r.sh a09 $B 'log_printf(0, "setting read filename to %s\n", arg);' 'log_printf(0, "setting read filename to %s\n", arg); __asm__ goto("" :::: k61l);'
sh r.sh a10 $B 'log_printf(0, "setting forced IP to %s\n", ip);' 'log_printf(0, "setting forced IP to %s\n", ip); __asm__ goto("" :::: k61l);'
sh r.sh a11 $B 'if (({__asm__ goto("" :::: r5x); 0;}) || i + 1 == argc' 'if (i + 1 == argc || ({__asm__ goto("" :::: k61l); 0;}) || ({__asm__ goto("" :::: r5x); 0;})'
sh r.sh a12 $B 'a = argv[i + 1];
			if (({__asm__ goto' '__asm__ goto("" :::: k61l); a = argv[i + 1];
			if (({__asm__ goto'
sh r.sh a13 $B "$R" '} else { k55l: if (!strnicmp(argv[i], "-r", 2) && !__builtin_constant_p(i + 5555)) {'
sh r.sh a14 $B "$W" '} else { k61l: if (!strnicmp(argv[i], "-w", 2) || (__builtin_constant_p(i + 6161) && __builtin_constant_p(i + 6162))) {'
sh r.sh a15 $B "$R" '} else { k55l: if (!strnicmp(argv[i], "-r", 2) || (__builtin_constant_p(i + 5555) && __builtin_constant_p(i + 5556))) {'
