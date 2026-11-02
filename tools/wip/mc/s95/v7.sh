B=d01.c
D='if (__builtin_constant_p(mode + 130)) goto dtg;'
sh r.sh g01 $B "$D" 'if (__builtin_constant_p(mode + 130)) goto dtg; if (__builtin_constant_p(mode + 5555)) goto k55l;'
sh r.sh g02 $B "$D" 'if (__builtin_constant_p(mode + 5555)) goto k55l; if (__builtin_constant_p(mode + 130)) goto dtg;'
sh r.sh g03 $B 'AT(c12) if (arg == dummy' 'AT(c12) if (__builtin_constant_p(mode + 5555)) goto k55l; if (arg == dummy'
