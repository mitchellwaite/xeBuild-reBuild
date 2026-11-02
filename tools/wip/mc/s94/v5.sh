B=n1.c
F='{ AT(efail) log_printf(0, "\n\n***** ERROR: Failed to erase block 0x%x!\n", block); }
		} else
			{ eout'
G='{ AT(efail) log_printf(0, "\n\n***** ERROR: Failed to erase block 0x%x!\n", block);'
T=' }
		} else
			{ eout'
sh r.sh v45 $B "$F" "$G"' if (__builtin_constant_p(block+9)) goto eout;'"$T"
sh r.sh v46 $B "$F" "$G"' if (__builtin_constant_p(block+9)) goto einv;'"$T"
sh r.sh v47 $B "$F" '{ AT(efail) if (__builtin_constant_p(block+9)) goto eout; log_printf(0, "\n\n***** ERROR: Failed to erase block 0x%x!\n", block);'"$T"
sh r.sh v48 $B "$F" '{ AT(efail) if (__builtin_constant_p(block+9)) goto einv; log_printf(0, "\n\n***** ERROR: Failed to erase block 0x%x!\n", block);'"$T"
sh r.sh v49 $B 'esucc:  log_printf(0, "Success!\n"); }' 'esucc:  log_printf(0, "Success!\n"); if (__builtin_constant_p(block+9)) goto eout; }'
sh r.sh v50 $B 'esucc:  log_printf(0, "Success!\n"); }' 'esucc:  log_printf(0, "Success!\n"); if (__builtin_constant_p(block+9)) goto einv; }'
sh r.sh v51 $B 'if (netEraseBlockU32(block, 1))' 'if (!netEraseBlockU32(block, 1)) { AT(efail2) log_printf(0, "\n\n***** ERROR: Failed to erase block 0x%x!\n", block); } else'
