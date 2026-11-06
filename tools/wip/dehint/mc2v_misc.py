# mode_client: operand-only removals that mc1 had no slot for
C5 = '__asm__ goto ("" :: "a"(cinfo) :: s4, c12);'
V = {
    'c5_noa': [(C5, 'JMP(s4, c12);')],
    'c5_noa_c12': [(C5, 'JMP(s4);')],
    'c5_noa_s4c12': [(C5, 'JMP(c12, s4);')],
    'c5_rdi': [(C5, '__asm__ goto ("" :: "r"(cinfo) :: s4, c12);')],
    'c5_g': [(C5, '__asm__ goto ("" :: "g"(cinfo) :: s4, c12);')],
    'fk_X1': [('__asm__ ("" :: "X"(&fko), "X"(&fkv)); ', '__asm__ ("" :: "X"(&fko)); ')],
    'fk_X2': [('__asm__ ("" :: "X"(&fko), "X"(&fkv)); ', '__asm__ ("" :: "X"(&fkv)); ')],
    'rk_m1': [('__asm__ ("" :: "m"(rko), "m"(rkv2)); ', '__asm__ ("" :: "m"(rko)); ')],
    'rk_m2': [('__asm__ ("" :: "m"(rko), "m"(rkv2)); ', '__asm__ ("" :: "m"(rkv2)); ')],
    'rk_m_v': [('__asm__ ("" :: "m"(rko), "m"(rkv2)); ', '__asm__ volatile ("" :: "m"(rko), "m"(rkv2)); ')],
    'bp_a_r': [('__asm__("" :: "a"(i + 1));', '__asm__("" :: "r"(i + 1));')],
}
