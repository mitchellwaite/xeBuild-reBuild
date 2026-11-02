K55='if ((char *)__builtin_constant_p(i + 30) == (char *)1 && (char *)__builtin_constant_p(i + 30 + 1) == (char *)1) goto k55l;'
U2='if (__builtin_constant_p(i + 320)) goto u2;'
CU4='				client_usage(4, argv[i]); }
			start = b;'
CU4L='				{ wb4: client_usage(4, argv[i]); } }
			start = b;'
sh r.sh v8 b1.c "$K55" 'if (__builtin_constant_p(i + 30) && __builtin_constant_p(i + 31) && __builtin_constant_p(i + 32)) goto k55l;'
sh r.sh v9 b1.c "$CU4" "$CU4L" "$U2" "$U2 if (__builtin_constant_p(i + 340) && __builtin_constant_p(i + 341) && __builtin_constant_p(i + 342) && __builtin_constant_p(i + 343)) goto wb4;"
sh r.sh v10 b1.c "$CU4" "$CU4L" "$U2" "$U2 if ((char *)__builtin_constant_p(i + 340) == (char *)1 && (char *)__builtin_constant_p(i + 341) == (char *)1) goto wb4;"
sh r.sh v11 b1.c "$K55" 'if ((char *)__builtin_constant_p(i + 30) == (char *)1) goto k55l;'
sh r.sh v12 b1.c "$K55" "$K55 if (__builtin_constant_p(i + 33) && __builtin_constant_p(i + 34) && __builtin_constant_p(i + 35)) goto k55l;"
