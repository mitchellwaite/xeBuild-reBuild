B=b08.c
R='if (({__asm__ goto("" :::: r5x); 0;}) || i + 1 == argc || !a || *a == '"'-'"')'
sh r.sh h01 $B "$R" 'if (i + 1 == argc || ({__asm__ goto("" :::: r5x); 0;}) || !a || *a == '"'-'"')'
sh r.sh h02 $B "$R" 'if (i + 1 == argc || !a || *a == '"'-'"' || ({__asm__ goto("" :::: r5x); 0;}))'
sh r.sh h03 $B '(char *)__builtin_constant_p(i + 31) == (char *)1) goto k55l;' '(char *)__builtin_constant_p(i + 31) == (char *)1 && __builtin_constant_p(i + 32)) goto k55l;'
sh r.sh h04 $B '(char *)__builtin_constant_p(i + 42) == (char *)1) goto k67l;' '(char *)__builtin_constant_p(i + 42) == (char *)1 && __builtin_constant_p(i + 43)) goto k67l;'
sh r.sh h05 $B 'if (__builtin_constant_p(i + 320) && __builtin_constant_p(i + 321)) goto u2;' 'if (__builtin_constant_p(i + 320)) goto u2;'
sh r.sh h06 $B 'if (__builtin_constant_p(i + 320) && __builtin_constant_p(i + 321)) goto u2;' 'if (__builtin_constant_p(i + 320) && __builtin_constant_p(i + 321) && __builtin_constant_p(i + 322)) goto u2;'
sh r.sh h07 $B 'if (mode) { w5x: client_usage(5, argv[i]); }' 'if (mode) { w5x: client_usage(5, argv[i]); __asm__ goto ("" :::: wb3); }'
sh r.sh h08 $B 'client_usage(3, argv[i]);
			if (mode) { w5x:' '{ client_usage(3, argv[i]); __asm__ goto ("" :::: w5x); }
			if (mode) { w5x:'
