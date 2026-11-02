H5='log_printf(0, "\n\n***** ERROR: cannot send xbox compatibility data when a HDD does not exist!\n"); }'
H4='log_printf(0, "\n\n***** ERROR: cannot send avatar data when a HDD does not exist!\n"); }'
for B in b06 b01; do
sh r.sh ${B}h1 $B.c "$H5" 'log_printf(0, "\n\n***** ERROR: cannot send xbox compatibility data when a HDD does not exist!\n"); JMP(i0); }'
sh r.sh ${B}h2 $B.c "$H5" 'JMP(i0); log_printf(0, "\n\n***** ERROR: cannot send xbox compatibility data when a HDD does not exist!\n"); }'
sh r.sh ${B}h3 $B.c "$H4" 'log_printf(0, "\n\n***** ERROR: cannot send avatar data when a HDD does not exist!\n"); JMP(i0); }'
sh r.sh ${B}h4 $B.c "$H5" 'log_printf(0, "\n\n***** ERROR: cannot send xbox compatibility data when a HDD does not exist!\n"); JMP(i1); }'
sh r.sh ${B}h5 $B.c "$H5" 'log_printf(0, "\n\n***** ERROR: cannot send xbox compatibility data when a HDD does not exist!\n"); if (__builtin_constant_p(mode + 4646)) goto i0; }'
done
