B=$1; P=$2
K2=' if (__builtin_constant_p(i + 35) && __builtin_constant_p(i + 36) && __builtin_constant_p(i + 37)) goto k55l;'
K1='if ((char *)__builtin_constant_p(i + 30) == (char *)1 && (char *)__builtin_constant_p(i + 31) == (char *)1) goto k55l;'
sh r.sh ${P}m1 $B "$K1$K2" "$K2 $K1"
sh r.sh ${P}m2 $B "$K2" ' if ((char *)__builtin_constant_p(i + 35) == (char *)1 && (char *)__builtin_constant_p(i + 36) == (char *)1 && (char *)__builtin_constant_p(i + 37) == (char *)1) goto k55l;'
sh r.sh ${P}m3 $B "$K1$K2" "$K1"
sh r.sh ${P}m4 $B 'goto k67l;' "goto k67l;$K2"
W='if (i + 1 == argc || ({__asm__ goto("" :::: w5x); 0;}) || !a || *a == '"'-'"')'
sh r.sh ${P}x1 $B "$W" 'if (({__asm__ goto("" :::: w5x); 0;}) || i + 1 == argc || !a || *a == '"'-'"')'
sh r.sh ${P}x2 $B "$W" 'if (i + 1 == argc || !a || ({__asm__ goto("" :::: w5x); 0;}) || *a == '"'-'"')'
sh r.sh ${P}x3 $B "$W" 'if (i + 1 == argc || !a || *a == '"'-'"' || ({__asm__ goto("" :::: w5x); 0;}))'
sh r.sh ${P}c1 $B 'AT(c12) if (arg == dummy || ({JMP(p0); 0;}))' 'AT(c12) if (({JMP(p0); 0;}) || arg == dummy)'
sh r.sh ${P}c2 $B 'AT(c12) if (arg == dummy || ({JMP(p0); 0;}))' 'AT(c12) if (arg == dummy || ({JMP(i0); 0;}))'
sh r.sh ${P}c3 $B 'AT(c12) if (arg == dummy || ({JMP(p0); 0;}))' 'AT(c12) if (arg == dummy || ({JMP(p0,i0); 0;}))'
