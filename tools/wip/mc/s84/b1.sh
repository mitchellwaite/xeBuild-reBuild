R='if (({__asm__ goto("" :::: r5x); 0;}) || i + 1 == argc'
W='if (i + 1 == argc || ({__asm__ goto("" :::: w5x); 0;})'
K55='if ((char *)__builtin_constant_p(i + 30) == (char *)1 && (char *)__builtin_constant_p(i + 31) == (char *)1) goto k55l;'
K67='if ((char *)__builtin_constant_p(i + 40) == (char *)1 && (char *)__builtin_constant_p(i + 41) == (char *)1 && (char *)__builtin_constant_p(i + 42) == (char *)1) goto k67l;'
K61='if ((char *)__builtin_constant_p(i + 300) == (char *)1 && (char *)__builtin_constant_p(i + 300 + 1) == (char *)1 && (char *)__builtin_constant_p(i + 300 + 2) == (char *)1) goto k61l;'
WB='if ((char *)__builtin_constant_p(i + 60) == (char *)1 && (char *)__builtin_constant_p(i + 61) == (char *)1) goto wb3;'
U2='if (__builtin_constant_p(i + 320) && __builtin_constant_p(i + 321)) goto u2;'
EC='				client_usage(3, argv[i]);
			if (mode)
				client_usage(5, argv[i]);
			arg = argv[++i];
			log_printf(0, "setting avatar'
sh r.sh v01 h1.c "$R" 'if (i + 1 == argc || ({__asm__ goto("" :::: r5x); 0;})'
sh r.sh v02 h1.c "$R" 'if (i + 1 == argc || !a || ({__asm__ goto("" :::: r5x); 0;})'
sh r.sh v03 h1.c "$W" 'if (({__asm__ goto("" :::: w5x); 0;}) || i + 1 == argc'
sh r.sh v04 h1.c "$W" 'if (i + 1 == argc || !a || ({__asm__ goto("" :::: w5x); 0;})'
sh r.sh v05 h1.c "$EC" '				client_usage(3, argv[i]);
			if (mode) { e5x: client_usage(5, argv[i]); }
			arg = argv[++i];
			log_printf(0, "setting avatar' "if (!argv[i + 1] || i + 1 == argc || *argv[i + 1] == '-')
				client_usage(3, argv[i]);
			if (mode)
				client_usage(5, argv[i]);
			arg = argv[++i];
			log_printf(0, \"setting avatar" "if (({__asm__ goto(\"\" :::: e5x); 0;}) || !argv[i + 1] || i + 1 == argc || *argv[i + 1] == '-')
				client_usage(3, argv[i]);
			if (mode)
				client_usage(5, argv[i]);
			arg = argv[++i];
			log_printf(0, \"setting avatar"
sh r.sh v06 h1.c "$K55" 'if (__builtin_constant_p(i + 30)) goto k55l;'
sh r.sh v07 h1.c "$K55" 'if ((char *)__builtin_constant_p(i + 30) == (char *)1 && (char *)__builtin_constant_p(i + 31) == (char *)1 && (char *)__builtin_constant_p(i + 32) == (char *)1 && (char *)__builtin_constant_p(i + 33) == (char *)1) goto k55l;'
sh r.sh v08 h1.c "$K67" 'if ((char *)__builtin_constant_p(i + 40) == (char *)1 && (char *)__builtin_constant_p(i + 41) == (char *)1) goto k67l;'
sh r.sh v09 h1.c "$K67" 'if ((char *)__builtin_constant_p(i + 40) == (char *)1 && (char *)__builtin_constant_p(i + 41) == (char *)1 && (char *)__builtin_constant_p(i + 42) == (char *)1 && (char *)__builtin_constant_p(i + 43) == (char *)1) goto k67l;'
sh r.sh v10 h1.c "$K61" 'if ((char *)__builtin_constant_p(i + 300) == (char *)1 && (char *)__builtin_constant_p(i + 300 + 1) == (char *)1) goto k61l;'
sh r.sh v11 h1.c "$K61" 'if ((char *)__builtin_constant_p(i + 300) == (char *)1 && (char *)__builtin_constant_p(i + 300 + 1) == (char *)1 && (char *)__builtin_constant_p(i + 300 + 2) == (char *)1 && (char *)__builtin_constant_p(i + 303) == (char *)1) goto k61l;'
sh r.sh v12 h1.c "$WB" 'if ((char *)__builtin_constant_p(i + 60) == (char *)1 && (char *)__builtin_constant_p(i + 61) == (char *)1 && (char *)__builtin_constant_p(i + 62) == (char *)1 && (char *)__builtin_constant_p(i + 63) == (char *)1 && (char *)__builtin_constant_p(i + 64) == (char *)1) goto wb3;'
sh r.sh v13 h1.c "$U2" 'if (__builtin_constant_p(i + 320)) goto u2;'
sh r.sh v14 h1.c "$U2" 'if (__builtin_constant_p(i + 320) && __builtin_constant_p(i + 321) && __builtin_constant_p(i + 322)) goto u2;'
sh r.sh v15 h1.c "$K55" "$K55 $K55"
sh r.sh v16 h1.c "$K67" "$K67 $K67"
