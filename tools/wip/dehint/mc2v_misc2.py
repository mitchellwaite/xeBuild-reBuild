# mode_client: c5's pin gone; simplify the fkbo / rok empty-struct asms
C5 = ('__asm__ goto ("" :: "a"(cinfo) :: s4, c12);', 'JMP(s4, c12);')
FX = ('__asm__ ("" :: "X"(&fko), "X"(&fkv)); ', '__asm__ ("" :: "X"(&fkv)); ')
RM = ('__asm__ ("" :: "m"(rko), "m"(rkv2)); ', '__asm__ ("" :: "m"(rko)); ')
V = {
    'c5': [C5],
    'c5_fx_rm': [C5, FX, RM],
    'c5_fx_rm_decl': [C5, FX, RM, ('{ struct {} fko; { struct {} fkv;', '{ { struct {} fkv;'),
                      ('{ struct {} rkv2; __asm__', '{ __asm__')],
    'c5_fx_rm_decl2': [C5, FX, RM, ('{ struct {} fko; { struct {} fkv;', '{ struct {} fkv; {'),
                       ('{ struct {} rkv2; __asm__', '{ __asm__'), ('{ struct {} rkv0; __asm__ goto', '{ __asm__ goto')],
    'c5_rkv0': [C5, ('{ struct {} rkv0; __asm__ goto', '{ __asm__ goto')],
}
V['all'] = V['c5_fx_rm_decl'] + [('{ struct {} rkv0; __asm__ goto', '{ __asm__ goto')]
