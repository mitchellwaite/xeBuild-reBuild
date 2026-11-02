B=b08.c
M='myatoh32(sblock, -1);



'
J='{ eout: log_printf(0, "\n\n***** ERROR: Block 0x%x is outside system area!\n", block); JUMP(efail); }'
F='{ AT(efail) log_printf(0, "\n\n***** ERROR: Failed to erase block 0x%x!\n", block); }
		} else
			{ eout'
sh r.sh v06 $B "$M" 'myatoh32(sblock, -1); if (__builtin_constant_p(block + 79)) goto eout;'
sh r.sh v07 $B "$M" 'myatoh32(sblock, -1); if (__builtin_constant_p(block + 79)) goto einv;'
sh r.sh v08 $B "$M" 'myatoh32(sblock, -1); if (__builtin_constant_p(block + 79)) goto eerase;'
sh r.sh v13 $B "$J" '{ eout: log_printf(0, "\n\n***** ERROR: Block 0x%x is outside system area!\n", block); JUMP(efail, einv); }'
sh r.sh v14 $B "$J" '{ eout: log_printf(0, "\n\n***** ERROR: Block 0x%x is outside system area!\n", block); JUMP(einv, efail); }'
sh r.sh v15 $B "$J" '{ eout: log_printf(0, "\n\n***** ERROR: Block 0x%x is outside system area!\n", block); JUMP(efail, esucc); }'
sh r.sh v16 $B "$J" '{ eout: log_printf(0, "\n\n***** ERROR: Block 0x%x is outside system area!\n", block); JUMP(esucc, efail); }'
sh r.sh v17 $B "$J" '{ eout: log_printf(0, "\n\n***** ERROR: Block 0x%x is outside system area!\n", block); }'
sh r.sh v18 $B "$F" '{ AT(efail) __attribute__((cold)); log_printf(0, "\n\n***** ERROR: Failed to erase block 0x%x!\n", block); }
		} else
			{ eout'
sh r.sh v21 $B "$F" '{ AT(efail) __attribute__((hot)); log_printf(0, "\n\n***** ERROR: Failed to erase block 0x%x!\n", block); }
		} else
			{ eout'
sh r.sh v22 $B "$J" '{ eout: log_printf(0, "\n\n***** ERROR: Block 0x%x is outside system area!\n", block); JUMP(efail, eerase); }'
sh r.sh v23 $B "$J" '{ eout: log_printf(0, "\n\n***** ERROR: Block 0x%x is outside system area!\n", block); if (__builtin_constant_p(block+5)) goto einv; JUMP(efail); }'
