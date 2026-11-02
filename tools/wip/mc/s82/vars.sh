K55='if ((char *)__builtin_constant_p(i + 30) == (char *)1 && (char *)__builtin_constant_p(i + 30 + 1) == (char *)1) goto k55l;'
U2='if (__builtin_constant_p(i + 320) && __builtin_constant_p(i + 321)) goto u2;'
WB3='if ((char *)__builtin_constant_p(i + 60) == (char *)1 && (char *)__builtin_constant_p(i + 61) == (char *)1) goto wb3;'
CU4='				client_usage(4, argv[i]); }
			start = b;'
CU4L='				{ wb4: client_usage(4, argv[i]); } }
			start = b;'
sh r.sh v1 b0.c "$K55" 'if (__builtin_constant_p(i + 30)) goto k55l;'
sh r.sh v2 b0.c "$K55" 'if (__builtin_constant_p(i + 30) && __builtin_constant_p(i + 31) && __builtin_constant_p(i + 32)) goto k55l;'
sh r.sh v3 b0.c "$U2" 'if (__builtin_constant_p(i + 320)) goto u2;'
sh r.sh v4 b0.c "$WB3" 'if (__builtin_constant_p(i + 60)) goto wb3;'
sh r.sh v5 b0.c "$CU4" "$CU4L" "$U2" "$U2 if (__builtin_constant_p(i + 340) && __builtin_constant_p(i + 341)) goto wb4;"
sh r.sh v6 b0.c "$CU4" "$CU4L" "$U2" "$U2 if (__builtin_constant_p(i + 340)) goto wb4;"
sh r.sh v7 b0.c "$CU4" "$CU4L" "$U2" "$U2 if (__builtin_constant_p(i + 340) && __builtin_constant_p(i + 341) && __builtin_constant_p(i + 342)) goto wb4;"
