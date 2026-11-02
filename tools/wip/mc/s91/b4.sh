B=$1
WB='if ((char *)__builtin_constant_p(i + 60) == (char *)1 && (char *)__builtin_constant_p(i + 61) == (char *)1 && (char *)__builtin_constant_p(i + 62) == (char *)1 && (char *)__builtin_constant_p(i + 63) == (char *)1 && (char *)__builtin_constant_p(i + 64) == (char *)1) goto wb3;'
K55='if ((char *)__builtin_constant_p(i + 30) == (char *)1 && (char *)__builtin_constant_p(i + 31) == (char *)1) goto k55l;'
K61='if ((char *)__builtin_constant_p(i + 300) == (char *)1 && (char *)__builtin_constant_p(i + 300 + 1) == (char *)1 && (char *)__builtin_constant_p(i + 300 + 2) == (char *)1) goto k61l;'
P=$2
sh r.sh ${P}1 $B "$WB" 'if ((char *)__builtin_constant_p(i + 60) == (char *)1 && (char *)__builtin_constant_p(i + 61) == (char *)1 && (char *)__builtin_constant_p(i + 62) == (char *)1) goto wb3;'
sh r.sh ${P}2 $B "$WB" 'if ((char *)__builtin_constant_p(i + 60) == (char *)1 && (char *)__builtin_constant_p(i + 61) == (char *)1 && (char *)__builtin_constant_p(i + 62) == (char *)1 && (char *)__builtin_constant_p(i + 63) == (char *)1) goto wb3;'
sh r.sh ${P}3 $B "$WB" ''
sh r.sh ${P}4 $B "$K55" "$K55 if (__builtin_constant_p(i + 35) && __builtin_constant_p(i + 36) && __builtin_constant_p(i + 37)) goto k55l;"
sh r.sh ${P}5 $B "$K55" "$K55 if (__builtin_constant_p(i + 35) && __builtin_constant_p(i + 36)) goto k55l;"
sh r.sh ${P}6 $B "$K61" "$K61 if (__builtin_constant_p(i + 305) && __builtin_constant_p(i + 306) && __builtin_constant_p(i + 307)) goto k61l;"
sh r.sh ${P}7 $B "$K61" "$K61 if (__builtin_constant_p(i + 305) && __builtin_constant_p(i + 306)) goto k61l;"
sh r.sh ${P}8 $B "$K61" "$K61 if (__builtin_constant_p(i + 305)) goto k61l;"
sh r.sh ${P}9 $B '{ einv: __attribute__((cold));' '{ einv: __attribute__((cold)); JMP(eout);'
