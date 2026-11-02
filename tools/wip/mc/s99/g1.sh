F='AT(efail) log_printf(0, "\n\n***** ERROR: Failed to erase block 0x%x!\n", block); if (__builtin_constant_p(block + 910)) goto efail; }'
L='if (__builtin_constant_p(block + 910)) goto esucc;'
P='AT(efail) log_printf(0, "\n\n***** ERROR: Failed to erase block 0x%x!\n", block);'
sh r.sh a01 J1.c "$F" "$P fl1: if (__builtin_constant_p(block + 910)) goto fl1; }"
sh r.sh a02 J1.c "$F" "AT(efail) fl1: if (__builtin_constant_p(block + 910)) goto fl1; log_printf(0, \"\n\n***** ERROR: Failed to erase block 0x%x!\n\", block); }"
sh r.sh a03 J1.c "$F" "AT(efail) fl1: log_printf(0, \"\n\n***** ERROR: Failed to erase block 0x%x!\n\", block); if (__builtin_constant_p(block + 910)) goto fl1; }"
sh r.sh a04 J1.c "$L" ""
sh r.sh a05 J1.c "$L" "" "$F" "$P fl1: if (__builtin_constant_p(block + 910)) goto fl1; }"
sh r.sh a06 J1.c "$L" "if (__builtin_constant_p(block + 910)) goto efail;"
sh r.sh a07 J1.c "$F" "$P }" "$L" "if (__builtin_constant_p(block + 910)) goto efail;"
sh r.sh a08 J1.c "$F" "$P if (__builtin_constant_p(block + 910)) goto esucc; }"
sh r.sh a09 J1.c "$F" "$P if (__builtin_constant_p(block + 910)) goto esucc; }" "$L" ""
sh r.sh a10 J1.c "$F" "$P if (__builtin_constant_p(block + 910)) goto efail; if (__builtin_constant_p(block + 911)) goto efail; }"
