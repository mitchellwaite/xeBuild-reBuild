# mode_client attempt 5: the dead if (0) blocks' contents (dv, dz in mode_client, dy in
# clientEraseBlockI): __builtin_unreachable() and the empty asm replaced by ordinary
# statements (the block stays dead).  Base: src/mode_client.c.
DV = 'if (0) { dv: asm volatile("" : : : "memory");  __builtin_unreachable(); }'
DZ = 'if (0) { dz: asm volatile("" : : : "cc"); __builtin_unreachable(); }'
DY = 'if (0) { dy: asm volatile(""); if (__builtin_constant_p(block + 901)) goto ybk; __builtin_unreachable(); }'
BODY = {
    'ret': 'return 0;',
    'retm': 'return mode;',
    'fail': 'goto fail;',
    'dtg': 'goto dtg;',
    'none': ';',
    'asm_ret': None,
}
V = {}
for k, b in BODY.items():
    if b is None:
        V['dv_asmret'] = [(DV, 'if (0) { dv: asm volatile("" : : : "memory"); return 0; }')]
        V['dz_asmret'] = [(DZ, 'if (0) { dz: asm volatile("" : : : "cc"); return 0; }')]
        V['dv_ur'] = [(DV, 'if (0) { dv: __builtin_unreachable(); }')]
        V['dz_ur'] = [(DZ, 'if (0) { dz: __builtin_unreachable(); }')]
        continue
    V['dv_' + k] = [(DV, 'if (0) { dv: %s }' % b)]
    V['dz_' + k] = [(DZ, 'if (0) { dz: %s }' % b)]
    V['dvz_' + k] = [(DV, 'if (0) { dv: %s }' % b), (DZ, 'if (0) { dz: %s }' % b)]
for k, b in (('ret', 'return;'), ('ybk', 'goto ybk;'), ('none', ';')):
    V['dy_' + k] = [(DY, 'if (0) { dy: asm volatile(""); if (__builtin_constant_p(block + 901)) goto ybk; %s }' % b)]
    V['dy2_' + k] = [(DY, 'if (0) { dy: if (__builtin_constant_p(block + 901)) goto ybk; %s }' % b)]
V['dvz_ur'] = V['dv_ur'] + V['dz_ur']
V['dy_ur'] = [(DY, 'if (0) { dy: if (__builtin_constant_p(block + 901)) goto ybk; __builtin_unreachable(); }')]
V['all_ur'] = V['dvz_ur'] + V['dy_ur']
XA = '{ struct {} fkv; __asm__ ("" :: "X"(&fkv)); '
MA = '{ __asm__ ("" :: "m"(rko)); goto rkn2; }'
V['noX'] = [(XA, '{ ')]
V['noXs'] = [(XA, '{ struct {} fkv; ')]
V['noM'] = [(MA, '{ goto rkn2; }')]
V['noM2'] = [(MA, '{ goto rkn2; }'), ('struct {} rko; ', '')]
V['noXM'] = V['noX'] + V['noM2']
