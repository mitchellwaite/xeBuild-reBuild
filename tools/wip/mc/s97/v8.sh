B=d01.c
P='clientPatches(NULL); JUMP(i0);'
sh r.sh h01 $B "$P" 'clientPatches(NULL); if (__builtin_constant_p(mode + 4646)) goto i0;'
sh r.sh h02 $B "$P" 'clientPatches(NULL); JMP(i0);'
sh r.sh h03 $B "$P" 'if (__builtin_constant_p(mode + 4646)) goto i0; clientPatches(NULL);'
sh r.sh h04 $B "$P" 'clientPatches(NULL); if (__builtin_constant_p(mode + 4646) && __builtin_constant_p(mode + 4647)) goto i0;'
sh r.sh h05 $B 'AT(p1) clientPatches(arg); }' 'AT(p1) clientPatches(arg); if (__builtin_constant_p(mode + 4646)) goto i0; }'
