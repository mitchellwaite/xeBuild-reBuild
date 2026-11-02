B=b06.c
S='esucc:  log_printf(0, "Success!\n"); }'
sh r.sh d11 $B "$S" 'esucc:  log_printf(0, "Success!\n"); if (__builtin_constant_p(block+9) && __builtin_constant_p(block+10)) goto eout; }'
sh r.sh d12 $B "$S" 'esucc:  log_printf(0, "Success!\n"); if (__builtin_constant_p(block+9) && __builtin_constant_p(block+10) && __builtin_constant_p(block+11)) goto eout; }'
sh r.sh d13 $B "$S" 'esucc:  log_printf(0, "Success!\n"); if (__builtin_constant_p(block+9) && __builtin_constant_p(block+10) && __builtin_constant_p(block+11) && __builtin_constant_p(block+12)) goto eout; }'
sh r.sh d14 $B "$S" 'esucc: if (__builtin_constant_p(block+9)) goto eout; log_printf(0, "Success!\n"); }'
sh r.sh d15 $B "$S" 'esucc:  log_printf(0, "Success!\n"); if (__builtin_constant_p(block+9)) goto eout; if (__builtin_constant_p(block+19)) goto einv; }'
sh r.sh d16 $B "$S" 'esucc:  log_printf(0, "Success!\n"); if (__builtin_constant_p(block+9)) goto eerase; }'
