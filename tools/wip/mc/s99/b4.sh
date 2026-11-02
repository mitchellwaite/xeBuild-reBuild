B=b08.c
sh r.sh d01 $B 'esucc:  log_printf' 'esucc:  __asm__ goto ("" :::: eout); log_printf'
sh r.sh d02 $B 'esucc:  log_printf' 'esucc:  if (__builtin_constant_p(block + 88)) goto eout; log_printf'
sh r.sh d03 $B 'goto einv; log_printf(0, "erasing' 'goto einv; if (__builtin_constant_p(block + 88)) goto eout; log_printf(0, "erasing'
sh r.sh d04 $B 'if (__builtin_constant_p(block + 77)) goto einv;' 'if (__builtin_constant_p(block + 88)) goto eout; if (__builtin_constant_p(block + 77)) goto einv;'
sh r.sh d05 $B 'eout: log_printf' 'eout: if (__builtin_constant_p(block + 88)) goto einv; log_printf'
sh r.sh d06 $B 'AT(efail) log_printf' 'AT(efail) if (__builtin_constant_p(block + 88)) goto eout; else log_printf'
sh r.sh d07 $B 'JUMP(efail); }' 'JUMP(efail); if (__builtin_constant_p(block + 88)) goto einv; }'
sh r.sh d08 $B 'if (__builtin_constant_p(block + 77)) goto einv;' 'if (__builtin_constant_p(block + 77)) goto einv; if (__builtin_constant_p(block + 78)) goto einv;'
